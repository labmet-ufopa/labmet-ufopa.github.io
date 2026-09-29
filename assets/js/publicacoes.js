// Lista de publicações, a partir de data/publicacoes.json
(function () {
  const lista = document.querySelector('#publicacoes');
  const contagem = document.querySelector('#contagem');
  const botoes = document.querySelector('#filtros-professor');
  const busca = document.querySelector('#busca');
  const MAX_AUTORES = 8;

  let publicacoes = [];
  let professor = '';

  function criar(tag, classe, texto) {
    const el = document.createElement(tag);
    if (classe) el.className = classe;
    if (texto !== undefined) el.textContent = texto;
    return el;
  }

  function semAcento(s) {
    return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  }

  function autores(pub) {
    const p = criar('p', 'pub-autores');
    let visiveis = pub.autores;
    let cortou = false;
    if (pub.autores.length > MAX_AUTORES) {
      // mantém os primeiros e todos os que são do laboratório
      visiveis = pub.autores.filter((a, i) => i < 3 || a.lab);
      cortou = true;
    }
    visiveis.forEach((a, i) => {
      if (i > 0) p.append(', ');
      const anterior = visiveis[i - 1];
      if (cortou && i > 0 && pub.autores.indexOf(a) - pub.autores.indexOf(anterior) > 1) p.append('… ');
      p.append(a.lab ? criar('strong', '', a.nome) : a.nome);
    });
    if (cortou && pub.autores.indexOf(visiveis[visiveis.length - 1]) < pub.autores.length - 1) p.append(' et al.');
    return p;
  }

  function item(pub) {
    const li = criar('li');
    const a = criar('a', 'pub-titulo', pub.titulo);
    a.href = 'https://doi.org/' + pub.doi;
    li.append(a, autores(pub));
    const meta = criar('p', 'pub-meta');
    meta.append(criar('em', '', pub.periodico), ', ' + pub.ano);
    if (pub.acesso_aberto) meta.append(criar('span', 'selo', 'Acesso aberto'));
    li.append(meta);
    return li;
  }

  function mostrar() {
    const termo = semAcento(busca.value.trim());
    const filtradas = publicacoes.filter((p) => {
      if (professor && !p.professores.includes(professor)) return false;
      if (!termo) return true;
      const texto = semAcento([p.titulo, p.periodico, p.ano, p.autores.map((a) => a.nome).join(' ')].join(' '));
      return texto.includes(termo);
    });

    lista.replaceChildren();
    let grupo = null;
    let ano = null;
    filtradas.forEach((p) => {
      if (p.ano !== ano) {
        ano = p.ano;
        const bloco = criar('section', 'ano-grupo');
        bloco.append(criar('h2', '', String(ano)));
        grupo = criar('ul', 'lista-pub');
        bloco.append(grupo);
        lista.append(bloco);
      }
      grupo.append(item(p));
    });

    contagem.textContent = filtradas.length === 0
      ? 'Nenhuma publicação encontrada com esse filtro.'
      : filtradas.length + (filtradas.length === 1 ? ' publicação' : ' publicações');
  }

  function montarFiltros() {
    const nomes = [...new Set(publicacoes.flatMap((p) => p.professores))].sort();
    [['', 'Todos']].concat(nomes.map((n) => [n, n])).forEach(([valor, rotulo]) => {
      const b = criar('button', 'filtro', rotulo);
      b.type = 'button';
      b.setAttribute('aria-pressed', String(valor === professor));
      b.addEventListener('click', () => {
        professor = valor;
        botoes.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        mostrar();
      });
      botoes.append(b);
    });
  }

  fetch('data/publicacoes.json')
    .then((r) => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then((dados) => {
      publicacoes = dados.publicacoes;
      const quando = document.querySelector('#atualizado');
      if (quando && dados.atualizado_em) {
        const [a, m, d] = dados.atualizado_em.split('-');
        quando.textContent = d + '/' + m + '/' + a;
      }
      montarFiltros();
      busca.addEventListener('input', mostrar);
      mostrar();
    })
    .catch(() => {
      contagem.textContent = 'Não foi possível carregar a lista de publicações. Recarregue a página para tentar de novo.';
    });
})();
