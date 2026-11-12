document.querySelectorAll('[data-portrait-video]').forEach((cover) => {
  cover.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
      return;
    }

    const player = document.createElement('iframe');
    player.id = cover.id;
    player.title = cover.getAttribute('aria-label').replace(/^Play /, '');
    player.src = `https://www.youtube-nocookie.com/embed${cover.pathname}?playsinline=1&autoplay=1`;
    player.referrerPolicy = 'strict-origin-when-cross-origin';
    player.allow = 'autoplay; encrypted-media; picture-in-picture';
    player.allowFullscreen = true;

    event.preventDefault();
    cover.replaceWith(player);
    player.focus();
  });
});
