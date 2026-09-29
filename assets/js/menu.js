// Menu recolhível nas telas pequenas
(function () {
  const botao = document.querySelector('.menu-botao');
  const menu = document.getElementById('menu-principal');
  if (!botao || !menu) return;

  function abrir(sim) {
    botao.setAttribute('aria-expanded', String(sim));
    menu.classList.toggle('aberto', sim);
  }

  botao.hidden = false;
  botao.addEventListener('click', () => abrir(botao.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && botao.getAttribute('aria-expanded') === 'true') {
      abrir(false);
      botao.focus();
    }
  });
})();
