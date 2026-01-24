(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const isHomePage = document.querySelector('.profile') !== null;
    if (!isHomePage) return;

    document.addEventListener('click', function (e) {
      const ripple = document.createElement('div');
      ripple.className = 'ripple';

      const size = 40;
      ripple.style.width = size + 'px';
      ripple.style.height = size + 'px';
      ripple.style.left = e.clientX - size / 2 + 'px';
      ripple.style.top = e.clientY - size / 2 + 'px';

      document.body.appendChild(ripple);

      setTimeout(function () {
        ripple.remove();
      }, 800);
    });
  });
})();
