# G8_Grafos_EDA2-2026.1

Grafo bipartido de drinks e ingredientes, com BFS pra descobrir receitas,
o que dá pra fazer com os ingredientes que você tem, e drinks relacionados.

## Estrutura

```
drinkgraph_project/
├── data/
│   └── drinks.json        # dataset de exemplo (5 drinks)
├── drinkgraph/
│   ├── graph.py            # [Pessoa A] estrutura do grafo
│   ├── loader.py           # [Pessoa A] lê o JSON e constrói o grafo
│   ├── search.py           # [Pessoa B] BFS + funções de busca
│   └── cli.py               # [Pessoa B] interface de linha de comando
├── tests/
│   ├── test_graph.py        # testes da Pessoa A
│   └── test_search.py       # testes da Pessoa B
├── main.py                  # ponto de entrada da CLI
└── conftest.py               # vazio, só pra o pytest achar o pacote
```

Nenhuma dependência externa é necessária pro código em si (só a
biblioteca padrão do Python). Pra rodar os testes, instale o `pytest`:

```bash
pip install pytest
```

## Como rodar

```bash
python main.py receita "Mojito"
python main.py posso-fazer "rum,limão,açúcar"
python main.py relacionados "Mojito" --profundidade 2
```

## Como rodar os testes

```bash
pytest
```

Os testes de `test_graph.py` já devem passar de cara. Os de
`test_search.py` testam o BFS genérico (que já está implementado) e têm
um gabarito comentado pras três funções que ainda faltam implementar.

## O que falta implementar

Em `drinkgraph/search.py`, três funções estão com `NotImplementedError`:

- `receita_do_drink(graph, nome_drink)`
- `o_que_posso_fazer(graph, ingredientes_disponiveis)`
- `drinks_relacionados(graph, nome_drink, profundidade)`

Cada uma tem uma dica no docstring de como usar `bfs()` e os métodos do
`Graph` pra implementar. Depois de implementar, descomentem/ajustem os
testes correspondentes em `tests/test_search.py`.

## Divisão de tarefas

**Pessoa A — dados e grafo**
- `drinkgraph/graph.py`, `drinkgraph/loader.py`
- Ampliar `data/drinks.json` com mais drinks reais
- `tests/test_graph.py`

**Pessoa B — algoritmo e CLI**
- Implementar as 3 funções em `drinkgraph/search.py`
- `drinkgraph/cli.py` (já está funcional, mas sintam-se livres pra
  melhorar a formatação da saída, adicionar comandos, etc.)
- `tests/test_search.py`

O contrato entre os dois lados é a classe `Graph` (`add_node`,
`add_edge`, `neighbors`, `get_node`, `has_node`, `nodes_by_type`,
`find_id`). Se alguém precisar mudar essa interface, é melhor avisar o
outro antes.
