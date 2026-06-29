from collections import deque
from typing import Optional


def bfs(graph, start_id: str, max_depth: Optional[int] = None) -> dict:
    if not graph.has_node(start_id):
        raise KeyError(f"Nó não encontrado: {start_id}")

    visitados = {start_id: {"distancia": 0, "pai": None}}
    fila = deque([start_id])

    while fila:
        atual = fila.popleft()
        dist_atual = visitados[atual]["distancia"]

        if max_depth is not None and dist_atual >= max_depth:
            continue

        for vizinho in graph.neighbors(atual):
            if vizinho not in visitados:
                visitados[vizinho] = {"distancia": dist_atual + 1, "pai": atual}
                fila.append(vizinho)

    return visitados


def reconstruir_caminho(bfs_result: dict, target_id: str) -> Optional[list]:
    """Reconstrói o caminho do início até target_id usando os ponteiros de pai do BFS."""
    if target_id not in bfs_result:
        return None
    caminho = []
    node = target_id
    while node is not None:
        caminho.append(node)
        node = bfs_result[node]["pai"]
    return list(reversed(caminho))



def receita_do_drink(graph, nome_drink: str) -> Optional[list[str]]:
    drink_id = graph.find_id(nome_drink, "drink")
    if drink_id is None:
        return None

    bfs_result = bfs(graph, drink_id, max_depth=1)
    ingredientes = [
        graph.get_node(node_id)["name"]
        for node_id, meta in bfs_result.items()
        if meta["distancia"] == 1
        and graph.get_node(node_id)["type"] == "ingredient"
    ]
    return sorted(ingredientes, key=str.casefold)


def o_que_posso_fazer(graph, ingredientes_disponiveis: list[str]) -> list[str]:

    disponiveis = {
        ingrediente.strip().lower()
        for ingrediente in ingredientes_disponiveis
        if ingrediente and ingrediente.strip()
    }

    resultados = []
    for drink_id in graph.nodes_by_type("drink"):
        ingredientes = [
            graph.get_node(ing_id)["name"].strip().lower()
            for ing_id in graph.neighbors(drink_id)
            if graph.get_node(ing_id)["type"] == "ingredient"
        ]
        if all(ingrediente in disponiveis for ingrediente in ingredientes):
            resultados.append(graph.get_node(drink_id)["name"])

    return sorted(resultados, key=str.casefold)


def drinks_relacionados(graph, nome_drink: str, profundidade: int = 3) -> Optional[list[str]]:
    drink_id = graph.find_id(nome_drink, "drink")
    if drink_id is None:
        return None

    bfs_result = bfs(graph, drink_id, max_depth=profundidade)
    relacionados = [
        graph.get_node(node_id)["name"]
        for node_id, meta in bfs_result.items()
        if node_id != drink_id and graph.get_node(node_id)["type"] == "drink"
    ]
    return sorted(relacionados, key=str.casefold)
