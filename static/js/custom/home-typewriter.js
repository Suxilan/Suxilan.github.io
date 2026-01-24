(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const subtitleElement = document.querySelector('.profile_inner > span');
    if (!subtitleElement) return;

    const text = subtitleElement.textContent.trim();
    if (!text) return;

    subtitleElement.textContent = '';

    let i = 0;
    function typeWriter() {
      if (i < text.length) {
        subtitleElement.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    }

    setTimeout(typeWriter, 500);
  });
})();
