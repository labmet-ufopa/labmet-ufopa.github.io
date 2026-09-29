"""Inclui o seletor de idioma e os links hreflang nas páginas em português."""
import glob

BASE = 'https://labmet-ufopa.github.io/'

for f in sorted(glob.glob('*.html')):
    s = open(f).read()
    if 'class="idiomas"' in s:
        continue
    old = '      <a class="ufopa-instituto" href="https://ieg.ufopa.edu.br/">Instituto de Engenharia e Geociências</a>\n'
    assert old in s, f
    s = s.replace(old, f'''      <div class="barra-direita">
        <a class="ufopa-instituto" href="https://ieg.ufopa.edu.br/">Instituto de Engenharia e Geociências</a>
        <nav class="idiomas" aria-label="Idioma">
          <a href="{f}" hreflang="pt-BR" lang="pt-BR" aria-current="true" title="Português (Brasil)"><img src="assets/img/bandeira-br.svg" alt="" width="24" height="16"><span>PT</span></a>
          <a href="en/{f}" hreflang="en" lang="en" title="English"><img src="assets/img/bandeira-uk.svg" alt="" width="24" height="16"><span>EN</span></a>
        </nav>
      </div>
''')
    pg = '' if f == 'index.html' else f
    s = s.replace('  <link rel="icon"', f'''  <link rel="alternate" hreflang="pt-BR" href="{BASE}{pg}">
  <link rel="alternate" hreflang="en" href="{BASE}en/{pg}">
  <link rel="alternate" hreflang="x-default" href="{BASE}{pg}">
  <link rel="icon"''', 1)
    open(f, 'w').write(s)
