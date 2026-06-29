"""
RESPONSÁVEL: Pessoa A

Estrutura de dados do grafo. É bipartido: nós do tipo "ingredient" e nós
do tipo "drink". Uma aresta drink-ingrediente significa "esse drink usa
esse ingrediente".

Esse arquivo é o "contrato" entre as duas partes do projeto: a Pessoa B
só deve depender dos métodos públicos abaixo (add_node, add_edge,
neighbors, get_node, has_node, nodes_by_type, find_id). Se precisar de
um método novo, combinem antes de mudar a interface.
"""

from typing import Optional


class Graph:
    def __init__(self):
        # node_id -> {"type": "drink"|"ingredient", "name": str, "data": dict}
        self._nodes: dict[str, dict] = {}
        # node_id -> set de node_ids vizinhos (grafo não direcionado)
        self._adj: dict[str, set] = {}

    @staticmethod
    def _make_id(name: str, node_type: str) -> str:
        """Gera um id estável a partir do nome (ignora maiúsculas/espaços nas pontas)."""
        return f"{node_type}:{name.strip().lower()}"

    def add_node(self, name: str, node_type: str, data: Optional[dict] = None) -> str:
        """
        Adiciona um nó (ou retorna o id existente, se o nó já existir).
        node_type deve ser "drink" ou "ingredient".
        """
        node_id = self._make_id(name, node_type)
        if node_id not in self._nodes:
            self._nodes[node_id] = {
                "type": node_type,
                "name": name.strip(),
                "data": data or {},
            }
            self._adj[node_id] = set()
        return node_id

    def add_edge(self, node_a: str, node_b: str) -> None:
        """Cria uma aresta não direcionada entre dois nós já existentes."""
        if node_a not in self._nodes:
            raise KeyError(f"Nó não encontrado: {node_a}")
        if node_b not in self._nodes:
            raise KeyError(f"Nó não encontrado: {node_b}")
        self._adj[node_a].add(node_b)
        self._adj[node_b].add(node_a)

    def neighbors(self, node_id: str) -> set:
        """Retorna o conjunto de ids vizinhos de um nó."""
        return self._adj.get(node_id, set())

    def get_node(self, node_id: str) -> Optional[dict]:
        """Retorna os dados de um nó ({"type", "name", "data"}) ou None."""
        return self._nodes.get(node_id)

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def find_id(self, name: str, node_type: str) -> Optional[str]:
        """Acha o node_id a partir do nome + tipo (case-insensitive)."""
        candidate = self._make_id(name, node_type)
        return candidate if candidate in self._nodes else None

    def nodes_by_type(self, node_type: str) -> list[str]:
        """Lista todos os node_ids de um tipo ('drink' ou 'ingredient')."""
        return [nid for nid, n in self._nodes.items() if n["type"] == node_type]

    def degree(self, node_id: str) -> int:
        """Retorna o grau (número de arestas) de um nó."""
        if node_id not in self._nodes:
            raise KeyError(f"Nó não encontrado: {node_id}")
        return len(self._adj[node_id])

    def all_nodes(self) -> list[str]:
        """Retorna todos os node_ids do grafo."""
        return list(self._nodes.keys())

    def all_edges(self) -> list[tuple[str, str]]:
        """
        Retorna todas as arestas como lista de tuplas (node_a, node_b).
        Cada aresta aparece apenas uma vez (a < b lexicograficamente).
        """
        seen: set[tuple] = set()
        edges = []
        for node_a, vizinhos in self._adj.items():
            for node_b in vizinhos:
                par = (min(node_a, node_b), max(node_a, node_b))
                if par not in seen:
                    seen.add(par)
                    edges.append(par)
        return edges

    def is_connected(self) -> bool:
        """
        Verifica se o grafo é conexo (todos os nós são alcançáveis a partir
        de qualquer nó). Retorna True para grafos vazios.
        """
        if not self._nodes:
            return True
        start = next(iter(self._nodes))
        visitados = {start}
        fila = [start]
        while fila:
            atual = fila.pop()
            for vizinho in self._adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return len(visitados) == len(self._nodes)

    def ingredientes_mais_usados(self, top_n: int = 10) -> list[tuple[str, int]]:
        """
        Retorna os top_n ingredientes mais usados (por grau/quantidade de drinks),
        como lista de tuplas (nome_ingrediente, quantidade_de_drinks).
        """
        contagens = [
            (self._nodes[nid]["name"], len(self._adj[nid]))
            for nid in self.nodes_by_type("ingredient")
        ]
        return sorted(contagens, key=lambda x: -x[1])[:top_n]

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self) -> str:
        n_drinks = len(self.nodes_by_type("drink"))
        n_ing = len(self.nodes_by_type("ingredient"))
        n_edges = len(self.all_edges())
        return f"Graph(drinks={n_drinks}, ingredients={n_ing}, arestas={n_edges})"