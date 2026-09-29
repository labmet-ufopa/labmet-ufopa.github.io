# LabMet UFOPA

Site do Laboratório de Instrumentação Meteorológica Multidisciplinar (LabMet) da Universidade Federal do Oeste do Pará, em Santarém (PA).

Publicado em <https://labmet-ufopa.github.io/> pelo GitHub Pages, a partir da branch `main`.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Apresentação, projetos em andamento e notícias |
| `carbonara.html` | Projeto CarbonARA-Brazil |
| `radiossondas.html` | Projeto de rastreamento de radiossondas |
| `equipe.html` | Coordenação, docentes colaboradores e estudantes |
| `contato.html` | Endereço e contatos |

Os estilos ficam em `assets/css/style.css` e as imagens em `assets/img/`.

## Como editar

O site é HTML estático, sem etapa de build. O cabeçalho e o rodapé se repetem em cada página, então uma mudança no menu precisa ser feita nos cinco arquivos.

Para ver localmente:

```sh
python3 -m http.server 8000
```

Depois abra <http://localhost:8000>.

Para incluir uma notícia, copie um item `<li>` da lista `noticias` em `index.html` e troque a data, o link e o título.

## Fotos

As imagens ficam em `assets/img/fotos/` e o crédito aparece na legenda de cada uma.

- Arquivos sem prefixo: Assessoria de Comunicação da Ufopa, publicados nas notícias do portal da universidade.
- Arquivos com prefixo `esa-`: página do projeto CarbonARA no portal de clima da Agência Espacial Europeia. Os termos de uso do portal pedem autorização por escrito para reprodução, então o uso aqui deve ser confirmado com a coordenação do projeto.

## Fontes das informações

- [Relação de laboratórios do IEG](https://ieg.ufopa.edu.br/ieg/laboratorios-2/)
- [Projetos de pesquisa no SIGAA/Ufopa](https://sigaa.ufopa.edu.br/sigaa/public/pesquisa/consulta_projetos.jsf), projeto PIIE970-2023
- [CarbonARA na Agência Espacial Europeia](https://climate.esa.int/en/supporting-the-paris-agreement/CarbonARA/)
- [Notícias da Ufopa](https://www.ufopa.edu.br/ufopa/comunica/noticias/) sobre o CarbonARA-Brazil
