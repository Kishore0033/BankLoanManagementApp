const links = document.querySelectorAll('#navLink a');

links.forEach(link => {
  link.addEventListener('click', () => {
    // remove active class from all links
    links.forEach(link => {
      link.classList.remove('active');
    });
    
    // add active class to clicked link
    link.classList.add('active');
  });
});
