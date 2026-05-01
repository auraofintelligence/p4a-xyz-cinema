const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
navToggle?.addEventListener('click', () => {
  const open = nav?.classList.toggle('is-open') ?? false;
  navToggle.setAttribute('aria-expanded', String(open));
});

const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('is-visible');
  });
}, { threshold: 0.12 });
reveals.forEach((el) => observer.observe(el));

const path = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('[data-nav] a').forEach((link) => {
  const href = link.getAttribute('href')?.split('/').pop() || 'index.html';
  if (href === path) link.setAttribute('aria-current', 'page');
});
