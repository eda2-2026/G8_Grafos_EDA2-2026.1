import json

from drinkgraph.graph import Graph
from drinkgraph.loader import load_from_json


def test_add_node_e_add_edge():
    g = Graph()
    rum = g.add_node("rum", "ingredient")
    mojito = g.add_node("Mojito", "drink")
    g.add_edge(mojito, rum)

    assert rum in g.neighbors(mojito)
    assert mojito in g.neighbors(rum)


def test_add_node_duplicado_retorna_mesmo_id():
    g = Graph()
    id1 = g.add_node("Limão", "ingredient")
    id2 = g.add_node("limão", "ingredient")  # mesmo nome, case diferente

    assert id1 == id2
    assert len(g) == 1


def test_add_edge_com_no_inexistente_levanta_erro():
    g = Graph()
    a = g.add_node("rum", "ingredient")
    try:
        g.add_edge(a, "drink:inexistente")
        assert False, "deveria ter levantado KeyError"
    except KeyError:
        pass


def test_nodes_by_type():
    g = Graph()
    g.add_node("Mojito", "drink")
    g.add_node("Caipirinha", "drink")
    g.add_node("rum", "ingredient")

    assert len(g.nodes_by_type("drink")) == 2
    assert len(g.nodes_by_type("ingredient")) == 1


def test_find_id():
    g = Graph()
    g.add_node("Mojito", "drink")

    assert g.find_id("mojito", "drink") is not None
    assert g.find_id("Caipirinha", "drink") is None


def test_load_from_json_constroi_grafo(tmp_path):
    data = {
        "drinks": [
            {"nome": "Mojito", "ingredientes": ["rum", "limão", "açúcar"]},
            {"nome": "Caipirinha", "ingredientes": ["cachaça", "limão", "açúcar"]},
        ]
    }
    path = tmp_path / "drinks.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    g = load_from_json(str(path))

    assert len(g.nodes_by_type("drink")) == 2
    # limão e açúcar são compartilhados -> só contam uma vez cada
    assert len(g.nodes_by_type("ingredient")) == 4

    mojito_id = g.find_id("Mojito", "drink")
    assert len(g.neighbors(mojito_id)) == 3
