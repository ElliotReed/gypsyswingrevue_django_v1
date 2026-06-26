

function getPreviousElement(elements, index, maxIndex) {
  let previousElement;
  if (index == 0) {
    previousElement = elements[maxIndex];
  } else {
    previousElement = elements[index - 1];
  }
  return previousElement
}

function getNextIndex(index, maxIndex) {
  if (index == maxIndex) {
    return 0;
  }
  return index + 1;
}

function changeShownElement(elements, durationInMilliseconds) {
  let index = 1;
  const maxIndex = elements.length - 1;

  setInterval(() => {
    const currentElement = elements[index];
    const previousElement = getPreviousElement(elements, index, maxIndex);

    // if already opaque (first element) don't reshow
    if (currentElement.style.opacity != 1) {
      currentElement.classList.add('show');
    }
    currentElement.classList.remove('hide');
    previousElement.classList.add('hide');
    previousElement.classList.remove('show');

    index = getNextIndex(index, maxIndex);
  }, durationInMilliseconds)
}

export function initViewer(viewerId, viewDurationInMilliseconds) {
  const viewer = document.getElementById(viewerId);
  const viewerChildren = viewer.children;

  changeShownElement(viewerChildren, viewDurationInMilliseconds);
}