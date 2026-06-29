import json
from pathlib import Path
from typing import Union

from .graph import Graph


def load_from_json(path: Union[str, Path]) -> Graph:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    graph = Graph()

    for drink in raw.get("drinks", []):
        drink_id = graph.add_node(
            drink["nome"],
            "drink",
            data={"instrucoes": drink.get("instrucoes", "")},
        )
        for ingrediente in drink.get("ingredientes", []):
            ing_id = graph.add_node(ingrediente, "ingredient")
            graph.add_edge(drink_id, ing_id)

    return graph
