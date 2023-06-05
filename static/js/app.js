const mainScroll = document.querySelector('[data-main-scroll]');
const siteHeader = document.querySelector('[data-site-header]');


function scrollFunction() {
  const top = mainScroll.scrollTop;
  if (siteHeader.clientWidth < 900 && top > 100) {
    siteHeader.style.fontSize = ".76rem";
  }
  else {
    siteHeader.style.fontSize = "1rem";
  }
}

mainScroll.onscroll = () => scrollFunction();