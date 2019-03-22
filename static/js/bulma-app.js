document.addEventListener('DOMContentLoaded', () => {
  const $navbarBurgers = document.getElementsByClassName('navbar-burger');

  if ($navbarBurgers.length > 0) {
    const $nav = $navbarBurgers[0];
    $nav.addEventListener('click', () => {
      const target = $nav.dataset.target;
      const $target = document.getElementById(target);

      $nav.classList.toggle('is-active');
      $target.classList.toggle('is-active');
    });
  }
});