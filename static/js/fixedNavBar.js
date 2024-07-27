const navbar = document.querySelector('#navLink');
const titleBar = document.querySelector('#navTitleBar');
const titleBarHeight = titleBar.offsetHeight;
const navbarHeight = navbar.offsetHeight;

window.addEventListener('scroll', () => {
  const scrollPos = window.scrollY;
  
  if (scrollPos > titleBarHeight) {
    navbar.classList.add('fixed');
    document.body.style.paddingTop = `${navbarHeight}px`;
  } else {
    navbar.classList.remove('fixed');
    document.body.style.paddingTop = 0;
  }
});