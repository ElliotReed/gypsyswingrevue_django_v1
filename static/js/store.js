const ICON_TRANSFORM = 'rotate(90deg)';
const SHOW_PLAYER_CLASS = 'show-player';

const audioTrackList = document.querySelectorAll('[data-album]');
const titleButtons = document.querySelectorAll('[data-title]');
const audioPlayers = document.querySelectorAll('[data-track]');

titleButtons.forEach(
  titleButton=> titleButton.addEventListener('click', toggleAudioPlayer)
  );

function toggleAudioPlayer(e) {
  const titleButton = e.target;
  const icon = titleButton.querySelector('i');
  const audioPlayer = e.target.nextElementSibling;
  const isCurrentPlayer = audioPlayer?.classList.contains(SHOW_PLAYER_CLASS);
  hideAllPLayers();
  resetAllIconsPosition();

  if (isCurrentPlayer) return; // has been reset, we're done!

  if (audioPlayer) {
      icon.style.transform = ICON_TRANSFORM;
      audioPlayer.classList.add(SHOW_PLAYER_CLASS);
  }
}

function hideAllPLayers() {
  audioPlayers.forEach(audioPlayer => {
    if (audioPlayer.classList.contains(SHOW_PLAYER_CLASS)) {
      audioPlayer.classList.remove(SHOW_PLAYER_CLASS);
    }
  });
}

function resetAllIconsPosition() {
  titleButtons.forEach(titleButton => {
  const icon = titleButton.querySelector('i');
    if (icon && icon.style.transform == ICON_TRANSFORM) {
      icon.style.transform = 'rotate(0deg)';
    }
  })
}