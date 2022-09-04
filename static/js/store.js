const audioTrackList = document.querySelectorAll('[data-album]');

const titleButtons = document.querySelectorAll('[data-title]');

const audioPlayers = document.querySelectorAll('[data-track]');

const iconTransform = 'rotate(90deg)';
const SHOW_CLASS = 'show-player';

titleButtons.forEach(
  titleButton=> titleButton.addEventListener('click', toggleAudioPlayer)
  );

function toggleAudioPlayer(e) {
  const titleButton = e.target;
  const icon = titleButton.querySelector('i');
  const audioPlayer = e.target.nextElementSibling;
  const isCurrentPlayer = audioPlayer?.classList.contains('show-player');
  hideAllPLayers();
  resetAllIconsPosition();

  if (isCurrentPlayer) return;

  if (audioPlayer) {
      icon.style.transform = iconTransform;
      audioPlayer.classList.add('show-player');
  }
}

function hideAllPLayers() {
  audioPlayers.forEach(audioPlayer => {
    if (audioPlayer.classList.contains(SHOW_CLASS) ){
      audioPlayer.classList.remove('show-player');
    }
  });
}

function resetAllIconsPosition() {
  titleButtons.forEach(titleButton => {
  const icon = titleButton.querySelector('i');
    if (icon && icon.style.transform == iconTransform) {
      icon.style.transform = 'rotate(0deg)';
    }
  })
}