(function () {
  document.addEventListener('click', function (ev) {
    var target = ev.target;
    // allow clicking the image or its link wrapper
    var anchor = null;
    if (target.classList && target.classList.contains('doc-thumb')) {
      anchor = target.closest('a.doc-thumb-link');
    } else if (target.classList && target.classList.contains('doc-thumb-link')) {
      anchor = target;
    } else if (target.closest) {
      anchor = target.closest('a.doc-thumb-link');
    }
    if (!anchor) return;
    ev.preventDefault();
    var url = anchor.getAttribute('data-full') || anchor.getAttribute('href');
    if (!url) return;

    // create overlay
    var overlay = document.createElement('div');
    overlay.className = 'projadb-lightbox-overlay';
    var close = document.createElement('div');
    close.className = 'projadb-lightbox-close';
    close.innerHTML = '&times;';
    close.addEventListener('click', function () { document.body.removeChild(overlay); });
    overlay.appendChild(close);
    var content = document.createElement('div');
    content.className = 'projadb-lightbox-content';
    var img = document.createElement('img');
    img.src = url;
    content.appendChild(img);
    overlay.appendChild(content);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        document.body.removeChild(overlay);
      }
    });
    document.body.appendChild(overlay);
  });
})();
