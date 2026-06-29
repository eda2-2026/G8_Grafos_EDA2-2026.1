# Buscador de Drinks — Grafo de Ingredientes (BFS)

Número da Lista: Trabalho 4<br>
Conteúdo da Disciplina: Grafos<br>

## Alunos

| Matrícula | Aluno |
| -- | -- |
| 231026385 | Igor Veras Daniel |
| 231026483 | Maria Eduarda de Amorim Galdino |


## Link do Vídeo
[Assistir ao vídeo](<LINK_DO_VIDEO>)

## Sobre
Sistema de busca de drinks em linha de comando que modela ingredientes e
drinks como um **grafo bipartido** e usa **Busca em Largura (BFS)** para
responder a três perguntas: qual a receita de um drink, quais drinks dá
pra fazer com os ingredientes disponíveis, e quais outros drinks estão
"relacionados" a um drink — ou seja, alcançáveis passando por
ingredientes em comum.

O grafo tem dois tipos de nó, `drink` e `ingredient`, e uma aresta liga
um drink a cada ingrediente que ele usa. Ingredientes compartilhados
entre receitas (como limão, presente em quase todas as do dataset)
geram um único nó com várias arestas — é justamente essa estrutura que
torna o BFS interessante: navegar de um drink para outro nunca é um
salto direto, é sempre uma travessia pelo grafo.

O trabalho foi dividido em duas partes: dados e estrutura do grafo de
um lado, e algoritmo de busca + interface de linha de comando do
outro.

## Screenshots

### Receita de um drink
![Screenshot 1](img/receita.png)
### Drinks relacionados
![Screenshot 2](img/relacionados.png)


## Instalação
Linguagem: Python 3.10+<br>
Framework: Nenhum (apenas biblioteca padrão)<br>
```bash
git clone https://github.com/eda2-2026/G8_Grafos_EDA2-2026.1.git
python3 main.py receita "Mojito"
```
## Uso
O programa funciona por subcomandos, sem menu interativo:
```
$ python3 main.py --help
usage: drinkgraph [-h] [--data DATA] {receita,posso-fazer,relacionados} ...

Busca de drinks em um grafo de ingredientes.

positional arguments:
  {receita,posso-fazer,relacionados}
    receita             Mostra a receita de um drink
    posso-fazer         Lista drinks possíveis com os ingredientes informados
    relacionados        Lista drinks relacionados via ingredientes compartilhados
```
**[1] Receita** — faz um BFS de profundidade 1 a partir do nó do drink;
os vizinhos encontrados já são os ingredientes da receita.
```
$ python3 main.py receita "Mojito"
Receita de Mojito:
  - rum
  - hortelã
  - limão
  - açúcar
  - água com gás
```
**[2] Posso fazer** — dado os ingredientes disponíveis, retorna os
drinks cuja receita está totalmente contida nesse conjunto.
```
$ python3 main.py posso-fazer "rum,limão,açúcar"
Você pode fazer:
  - Daiquiri
```
**[3] Relacionados** — faz um BFS com profundidade configurável a
partir do drink, filtrando só os nós do tipo `drink` no resultado. É
aqui que o efeito dos ingredientes compartilhados fica mais visível:
com profundidade 2, basta um ingrediente em comum (como o limão) pra
conectar dois drinks.
```
$ python3 main.py relacionados "Mojito" --profundidade 2
Drinks relacionados a Mojito:
  - Caipirinha
  - Cuba Libre
  - Daiquiri
  - Gin Tônica
```
> A ordem exata dos itens pode variar entre execuções, já que os
> vizinhos de cada nó são guardados em um `set`.
---
## Outros
Estrutura de arquivos:
```
drinkgraph_project/
├── main.py                # ponto de entrada da CLI
├── data/
│   └── drinks.json        # dataset de drinks e ingredientes
├── drinkgraph/
│   ├── graph.py           # estrutura do grafo bipartido
│   ├── loader.py          # leitura do JSON e construção do grafo
│   ├── search.py          # BFS genérico + funções de busca específicas
│   └── cli.py             # interface de linha de comando (argparse)
├── tests/
│   ├── test_graph.py
│   └── test_search.py
└── README.md
```
O nó de cada drink/ingrediente é identificado pelo nome normalizado em
minúsculas, o que evita duplicar nós quando o mesmo ingrediente aparece
com grafias diferentes (ex.: "Limão" e "limão"). O dataset usa uma
lista fixa de 5 drinks para facilitar testes e reprodutibilidade, mas
pode ser facilmente expandido editando `data/drinks.json`.