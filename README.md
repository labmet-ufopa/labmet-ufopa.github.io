# LabMet UFOPA

Site do Laboratório de Instrumentação Meteorológica Multidisciplinar (LabMet) da Universidade Federal do Oeste do Pará, em Santarém (PA).

Publicado em <https://labmet-ufopa.github.io/> pelo GitHub Pages, a partir da branch `main`.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Apresentação, projetos em andamento e notícias |
| `carbonara.html` | Projeto CarbonARA-Brazil |
| `radiossondas.html` | Projeto de rastreamento de radiossondas |
| `produtos.html` | Ferramentas desenvolvidas no laboratório |
| `publicacoes.html` | Artigos dos professores, lidos de `data/publicacoes.json` |
| `equipe.html` | Professores do laboratório, colaboradores e estudantes |
| `contato.html` | Endereço e contatos |

Os estilos ficam em `assets/css/style.css` e as imagens em `assets/img/`.

Os links para o CSS e os scripts terminam com `?v=` e uma data (por exemplo, `style.css?v=20260929c`). Ao alterar `style.css` ou um arquivo em `assets/js/`, troque esse valor em todas as páginas, inclusive as de `en/`. Assim os navegadores baixam a versão nova, em vez de usar a antiga guardada em cache junto com o HTML novo.

## Versão em inglês

O português é o idioma principal. A versão em inglês fica em `en/`, com os mesmos nomes de arquivo (`en/index.html`, `en/carbonara.html` etc.). O seletor com as bandeiras, no canto superior direito, leva à mesma página no outro idioma.

Ao mudar o texto de uma página, atualize também a página correspondente em `en/`. Nas páginas em inglês, os caminhos para `assets/` e `data/` começam com `../`.

## Como editar

O site é HTML estático, sem etapa de build. O cabeçalho e o rodapé se repetem em cada página, então uma mudança no menu precisa ser feita em todos os arquivos `.html`.

Para ver localmente:

```sh
python3 -m http.server 8000
```

Depois abra <http://localhost:8000>.

Para incluir uma notícia, copie um item `<li>` da lista `noticias` em `index.html` e troque a data, o link e o título.

## Publicações

A lista vem da base aberta [OpenAlex](https://openalex.org/). Para atualizar:

```sh
python3 scripts/atualizar_publicacoes.py
```

O script grava `data/publicacoes.json`. No início dele ficam a lista de professores, o ano inicial e os DOIs excluídos (artigos fora dos temas do laboratório, duplicados ou retratados). Para incluir um professor, acrescente o identificador de autor dele na OpenAlex.

## Fotos

As imagens ficam em `assets/img/fotos/` e o crédito aparece na legenda de cada uma.

- Arquivos sem prefixo: Assessoria de Comunicação da Ufopa, publicados nas notícias do portal da universidade.
- `assets/img/equipe/`: retratos do portal público do SIGAA/Ufopa e da página pessoal do professor.
- Arquivos com prefixo `esa-`: página do projeto CarbonARA no portal de clima da Agência Espacial Europeia. Os termos de uso do portal pedem autorização por escrito para reprodução, então o uso aqui deve ser confirmado com a coordenação do projeto.

## Fontes das informações

- [Relação de laboratórios do IEG](https://ieg.ufopa.edu.br/ieg/laboratorios-2/)
- [Projetos de pesquisa no SIGAA/Ufopa](https://sigaa.ufopa.edu.br/sigaa/public/pesquisa/consulta_projetos.jsf), projeto PIIE970-2023
- [CarbonARA na Agência Espacial Europeia](https://climate.esa.int/en/supporting-the-paris-agreement/CarbonARA/)
- [Notícias da Ufopa](https://www.ufopa.edu.br/ufopa/comunica/noticias/) sobre o CarbonARA-Brazil
