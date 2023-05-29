function toggleMenu(theId) {
  const menu = document.getElementById(theId);
  menu.classList.toggle('show');
  if (menu.classList.contains('show')) {
    setTimeout(() => {
      document.addEventListener('click', () => {
        menu.classList.remove('show');
      }, { once: true });
    }, 50); // timeout to not immediately close
  }
}

function highlight(div) {
  const prev = div.style;
  div.style.transition = 'background-color 0.5s';
  div.style.backgroundColor = 'yellow';
  setTimeout(() => {
    div.style.transition = 'background-color 4s';
    div.style.backgroundColor = 'unset';
  }, 500);
  setTimeout(() => div.style = prev, 600);
}
