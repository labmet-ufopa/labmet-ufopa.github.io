// Menu em telas pequenas
const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');

if (toggle && nav) {
  const setOpen = (open) => {
    nav.dataset.open = String(open);
    toggle.setAttribute('aria-expanded', String(open));
  };
  toggle.addEventListener('click', () => setOpen(nav.dataset.open !== 'true'));
  nav.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });
}

const ano = document.querySelector('#ano');
if (ano) ano.textContent = new Date().getFullYear();
