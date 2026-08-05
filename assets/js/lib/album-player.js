function formatTime(timeInSeconds) {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = String(Math.floor(timeInSeconds) % 60).padStart(2, '0');
  return `${minutes}:${seconds}`;
}
class AudioController {
  constructor({ onLoaded, onTimeUpdate, onEnded } = {}) {
    this.audio = new Audio();

    this.onLoaded = onLoaded;
    this.onTimeUpdate = onTimeUpdate;
    this.onEnded = onEnded;

    this.audio.addEventListener('loadeddata', () => {
      this.onLoaded?.(this.audio.duration, this.audio.currentTime);
    });
    this.audio.addEventListener('timeupdate', () => {
      this.onTimeUpdate?.(this.audio.currentTime);
    });
    this.audio.addEventListener('ended', () => {
      this.onEnded?.();
    });
  }

  loadSrc(src) {
    this.audio.src = src;
  }

  play() {
    this.audio.play();
  }

  pause() {
    this.audio.pause();
  }

  get isPlaying() {
    return !this.audio.paused;
  }

  get duration() {
    return this.audio.duration || 0;
  }

  get currentTime() {
    return this.audio.currentTime;
  }

  seekTo(time) {
    const clamped = Math.max(0, Math.min(time, this.duration || time));
    console.log("clamped: ", clamped)
    this.audio.currentTime = clamped;
  }

  seekToBeginning() {
    this.audio.currentTime = 0;
  }
}

class Record {
  constructor(element, { slideMs = 1000, degPerSec = 180 } = {}) {
    this.element = element;
    this.slideMs = slideMs;
    this.degPerSec = degPerSec;

    this.x = 0;
    this.angle = 0;

    this.spinning = false;
    this.sliding = null;

    this.rafId = null;
    this.lastTime = null;

    this.element.style.transformOrigin = 'center';
    this._render();
  }

  slideOut() {
    this._startSlide(1);
  }

  slideIn() {
    this._startSlide(0);
  }

  spin() {
    if (this.spinning) return;
    this.spinning = true;
    this.lastTime = null;
    this._ensureLoop();
  }

  stopSpin() {
    this.spinning = false;
  }

  _startSlide(target) {
    this.sliding = { from: this.x, to: target, startTime: null };
    this._ensureLoop();
  }

  _ensureLoop() {
    if (this.rafId == null) {
      this.rafId = requestAnimationFrame((t) => this._tick(t));
    }
  }

  _tick(time) {
    let stillActive = false;

    if (this.sliding) {
      if (this.sliding.startTime == null) this.sliding.startTime = time;
      const elapsed = time - this.sliding.startTime;
      const t = Math.min(elapsed / this.slideMs, 1);
      const eased = this._easeInOut(t);
      this.x = this.sliding.from + (this.sliding.to - this.sliding.from) * eased;
      if (t >= 1) {
        this.x = this.sliding.to;
        this.sliding = null;
      } else {
        stillActive = true;
      }
    }

    if (this.spinning) {
      if (this.lastTime != null) {
        const dt = (time - this.lastTime) / 1000;
        this.angle = (this.angle + this.degPerSec * dt) % 360;
      }
      stillActive = true;
    }
    this.lastTime = time;

    this._render();

    if (stillActive) {
      this.rafId = requestAnimationFrame((t) => this._tick(t));
    } else {
      this.rafId = null;
    }
  }

  _render() {
    const tx = this.x * 50;
    this.element.style.transform = `translateX(${tx}%) rotate(${this.angle}deg)`;
  }

  _easeInOut(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }
}

/* -------------------------------------------------------------------------
   AlbumPlayer
   Glue for one album: its AudioController, its Record, and its own scoped
   UI elements (looked up inside its root via data-component, not globally).
   ------------------------------------------------------------------------- */
class AlbumPlayer {
  constructor(rootElement) {
    this.id = rootElement.dataset.id;
    this.root = rootElement;

    const recordElement = rootElement.querySelector('[data-component="record"]');

    this.playPauseButton = rootElement.querySelector('[data-component="play-pause-button"]');
    this.previousButton = rootElement.querySelector('[data-component="previous-button"]');
    this.nextButton = rootElement.querySelector('[data-component="next-button"]');
    this.repeatButton = rootElement.querySelector('[data-component="repeat-button"]');

    this.progressBar = rootElement.querySelector('[data-component="progress-bar"]');
    this.progressFill = rootElement.querySelector('[data-component="progress-fill"]');
    this.currentTimeElement = rootElement.querySelector('[data-component="current-time"]');
    this.durationElement = rootElement.querySelector('[data-component="duration"]');

    this.currentTitleElement = rootElement.querySelector('[data-component="current-title"]');

    // only tracks with an actual preview src are part of the playable
    // sequence — others exist in the DOM (e.g. disabled) but are skipped
    this.trackButtons = Array.from(rootElement
      .querySelectorAll('[data-component="track-button"]'));
    this.tracks = this.trackButtons.filter((button) => Boolean(button.dataset.src));

    this.currentTrackIndex = -1;
    this.albumMode = false; // true when playing the album sequence, false for a single chosen track
    this.repeatEnabled = false;

    this.record = new Record(recordElement);
    this.audio = new AudioController({
      onLoaded: (duration) => this._showDuration(duration),
      onTimeUpdate: (time) => this._showCurrentTime(time),
      onEnded: () => this._handleEnded(),
    });

    // set by PlayerManager for cross-player coordination
    this.onPlay = null;
    this.onStop = null;

    this._bindControls();
    this._bindTrackButtons();
  }

  _bindControls() {
    this.playPauseButton?.addEventListener('click', () => this.toggle());
    this.previousButton?.addEventListener('click', () => this.previous());
    this.nextButton?.addEventListener('click', () => this.next());

    this.repeatButton?.addEventListener('click', () => {
      this.repeatEnabled = !this.repeatEnabled;
      this.repeatButton.classList.toggle('is-active', this.repeatEnabled);
    });

    this.progressBar?.addEventListener('click', (event) => {
      const rect = this.progressBar.getBoundingClientRect();
      const ratio = (event.clientX - rect.left) / rect.width;
      this.audio.seekTo(ratio * this.audio.duration);
    });
  }

  _bindTrackButtons() {
    this.tracks.forEach((trackButton, index) => {
      trackButton.addEventListener('click', () => this.playTrackAt(index, { albumMode: false }));
    });
  }

  loadTrack(src, { title } = {}) {
    this.audio.loadSrc(src);
    if (title !== undefined && this.currentTitleElement) this.currentTitleElement.textContent = title;
  }

  playTrackAt(index, { albumMode = this.albumMode } = {}) {
    if (index < 0 || index >= this.tracks.length) return;
    this.currentTrackIndex = index;
    this.albumMode = albumMode;
    const trackButton = this.tracks[index];
    this.loadTrack(trackButton.dataset.src, { title: trackButton.dataset.title });
    this.play();
  }

  next() {
    if (this.tracks.length === 0) return;
    const nextIndex = (this.currentTrackIndex + 1) % this.tracks.length;
    this.playTrackAt(nextIndex, { albumMode: true });
  }

  previous() {
    if (this.tracks.length === 0) return;
    const previousIndex = (this.currentTrackIndex - 1 + this.tracks.length) % this.tracks.length;
    this.playTrackAt(previousIndex, { albumMode: true });
  }

  play() {
    // nothing loaded yet — the main play button starts the album sequence
    // from the first available preview
    if (this.currentTrackIndex === -1) {
      if (this.tracks.length === 0) return; // no previews available at all
      this.playTrackAt(0, { albumMode: true });
      return;
    }

    this.audio.play();
    this.record.slideOut();
    this.record.spin();
    this.playPauseButton?.classList.add('is-playing');
    this.onPlay?.(this.id);
  }

  // user hit pause — stop spinning, stay slid out
  pause() {
    this.audio.pause();
    this.record.stopSpin();
    this.playPauseButton?.classList.remove('is-playing');
  }

  // full stop — track ended with nothing to continue to, or another
  // album became active. stops spinning AND retracts the record.
  stop() {
    this.audio.pause();
    this.audio.seekToBeginning();
    this.record.stopSpin();
    this.record.slideIn();
    this.playPauseButton?.classList.remove('is-playing');
    this._resetProgress();
    this.onStop?.(this.id);
  }

  toggle() {
    this.audio.isPlaying ? this.pause() : this.play();
  }

  _handleEnded() {
    // the record always retracts at a track's end — it slides back out
    // immediately below if playback continues to another track
    this.record.stopSpin();
    this.record.slideIn();
    this.playPauseButton?.classList.remove('is-playing');
    this._resetProgress();

    if (this.repeatEnabled) {
      if (this.albumMode) {
        this.next(); // loop the whole album's sequence
      } else {
        this.playTrackAt(this.currentTrackIndex, { albumMode: false }); // loop this one track
      }
      return;
    }

    if (this.albumMode) {
      const isLastTrack = this.currentTrackIndex === this.tracks.length - 1;
      if (!isLastTrack) {
        this.next();
        return;
      }
    }

    this.onStop?.(this.id);
  }

  _showCurrentTime(time) {
    if (this.currentTimeElement) {
      this.currentTimeElement.textContent = formatTime(time);
    }
    this._updateProgressFill(time, this.audio.duration);
  }

  _showDuration(duration) {
    if (this.durationElement) {
      this.durationElement.textContent = formatTime(duration);
    }
  }

  _updateProgressFill(currentTime, duration) {
    if (!this.progressFill || !duration) return;
    const percent = (currentTime / duration) * 100;
    this.progressFill.style.width = `${percent}%`;
  }

  _resetProgress() {
    if (this.progressFill) this.progressFill.style.width = '0%';
    if (this.currentTimeElement) this.currentTimeElement.textContent = formatTime(0);
  }
}

/* -------------------------------------------------------------------------
   PlayerManager
   Only place that knows about *all* players. Jukebox behavior: starting
   one stops any other that's currently playing.
   ------------------------------------------------------------------------- */
class PlayerManager {
  constructor() {
    this.players = new Map(); // id -> AlbumPlayer
    this.activeId = null;
  }

  register(rootElement) {
    const player = new AlbumPlayer(rootElement);
    player.onPlay = (id) => this._handlePlay(id);
    player.onStop = (id) => {
      if (this.activeId === id) this.activeId = null;
    };
    this.players.set(player.id, player);
    return player;
  }

  _handlePlay(playingId) {
    if (this.activeId && this.activeId !== playingId) {
      this.players.get(this.activeId)?.stop();
    }
    this.activeId = playingId;
  }

  get(id) {
    return this.players.get(id);
  }

  stopAll() {
    this.players.forEach((p) => p.stop());
  }
}

// initialize
const manager = new PlayerManager();

document.querySelectorAll("[data-component='player']").forEach((rootElement) => {
  manager.register(rootElement);
});