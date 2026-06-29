import json
import pytest

from drinkgraph.graph import Graph
from drinkgraph.loader import load_from_json


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def grafo_simples():
    """Grafo com 2 drinks e 4 ingredientes, limão e açúcar compartilhados."""
    g = Graph()
    mojito     = g.add_node("Mojito",     "drink")
    caipirinha = g.add_node("Caipirinha", "drink")
    rum        = g.add_node("rum",        "ingredient")
    cachaca    = g.add_node("cachaça",    "ingredient")
    limao      = g.add_node("limão",      "ingredient")
    acucar     = g.add_node("açúcar",     "ingredient")

    g.add_edge(mojito,     rum)
    g.add_edge(mojito,     limao)
    g.add_edge(mojito,     acucar)
    g.add_edge(caipirinha, cachaca)
    g.add_edge(caipirinha, limao)
    g.add_edge(caipirinha, acucar)

    return g, mojito, caipirinha, rum, cachaca, limao, acucar


@pytest.fixture
def drinks_json(tmp_path):
    """Cria um arquivo JSON temporário com 3 drinks."""
    data = {
        "drinks": [
            {"nome": "Mojito",     "ingredientes": ["rum", "limão", "açúcar", "hortelã"]},
            {"nome": "Caipirinha", "ingredientes": ["cachaça", "limão", "açúcar"]},
            {"nome": "Daiquiri",   "ingredientes": ["rum", "limão", "açúcar"]},
        ]
    }
    path = tmp_path / "drinks.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# add_node
# ---------------------------------------------------------------------------

def test_add_node_retorna_id_correto():
    g = Graph()
    node_id = g.add_node("Mojito", "drink")
    assert node_id == "drink:mojito"


def test_add_node_duplicado_retorna_mesmo_id():
    g = Graph()
    id1 = g.add_node("Limão", "ingredient")
    id2 = g.add_node("limão", "ingredient")   # mesmo nome, case diferente
    assert id1 == id2
    assert len(g) == 1


def test_add_node_strips_espacos():
    g = Graph()
    id1 = g.add_node("  rum  ", "ingredient")
    id2 = g.add_node("rum",     "ingredient")
    assert id1 == id2


def test_add_node_drink_e_ingredient_nao_colidem():
    """Mesmo nome, tipos diferentes → ids distintos."""
    g = Graph()
    id_drink = g.add_node("limão", "drink")
    id_ing   = g.add_node("limão", "ingredient")
    assert id_drink != id_ing
    assert len(g) == 2


def test_add_node_armazena_nome_original():
    g = Graph()
    nid = g.add_node("Hortelã", "ingredient")
    assert g.get_node(nid)["name"] == "Hortelã"


def test_add_node_armazena_data():
    g = Graph()
    nid = g.add_node("Mojito", "drink", data={"instrucoes": "Macere..."})
    assert g.get_node(nid)["data"]["instrucoes"] == "Macere..."


def test_add_node_data_padrao_dict_vazio():
    g = Graph()
    nid = g.add_node("rum", "ingredient")
    assert g.get_node(nid)["data"] == {}


# ---------------------------------------------------------------------------
# add_edge
# ---------------------------------------------------------------------------

def test_add_edge_cria_aresta_bidirecional(grafo_simples):
    g, mojito, caipirinha, rum, cachaca, limao, acucar = grafo_simples
    assert rum   in g.neighbors(mojito)
    assert mojito in g.neighbors(rum)


def test_add_edge_no_inexistente_levanta_keyerror():
    g = Graph()
    a = g.add_node("rum", "ingredient")
    with pytest.raises(KeyError):
        g.add_edge(a, "drink:nao-existe")


def test_add_edge_no_a_inexistente_levanta_keyerror():
    g = Graph()
    b = g.add_node("rum", "ingredient")
    with pytest.raises(KeyError):
        g.add_edge("drink:nao-existe", b)


def test_add_edge_idempotente():
    """Adicionar a mesma aresta duas vezes não duplica vizinhos."""
    g = Graph()
    a = g.add_node("Mojito", "drink")
    b = g.add_node("rum",    "ingredient")
    g.add_edge(a, b)
    g.add_edge(a, b)
    assert len(g.neighbors(a)) == 1


# ---------------------------------------------------------------------------
# neighbors / has_node / find_id / get_node
# ---------------------------------------------------------------------------

def test_neighbors_no_sem_vizinhos():
    g = Graph()
    nid = g.add_node("rum", "ingredient")
    assert g.neighbors(nid) == set()


def test_neighbors_no_inexistente_retorna_set_vazio():
    g = Graph()
    assert g.neighbors("ingredient:fantasma") == set()


def test_has_node_existente(grafo_simples):
    g, mojito, *_ = grafo_simples
    assert g.has_node(mojito)


def test_has_node_inexistente():
    g = Graph()
    assert not g.has_node("drink:fantasma")


def test_find_id_case_insensitive():
    g = Graph()
    g.add_node("Mojito", "drink")
    assert g.find_id("mojito", "drink") is not None
    assert g.find_id("MOJITO", "drink") is not None


def test_find_id_inexistente_retorna_none():
    g = Graph()
    assert g.find_id("Caipirinha", "drink") is None


def test_get_node_retorna_estrutura_correta():
    g = Graph()
    nid = g.add_node("rum", "ingredient")
    node = g.get_node(nid)
    assert node["type"] == "ingredient"
    assert node["name"] == "rum"
    assert "data" in node


def test_get_node_inexistente_retorna_none():
    g = Graph()
    assert g.get_node("ingredient:fantasma") is None


# ---------------------------------------------------------------------------
# nodes_by_type
# ---------------------------------------------------------------------------

def test_nodes_by_type(grafo_simples):
    g, *_ = grafo_simples
    assert len(g.nodes_by_type("drink")) == 2
    assert len(g.nodes_by_type("ingredient")) == 4


def test_nodes_by_type_tipo_vazio():
    g = Graph()
    assert g.nodes_by_type("drink") == []


# ---------------------------------------------------------------------------
# degree / all_edges / is_connected
# ---------------------------------------------------------------------------

def test_degree_correto(grafo_simples):
    g, mojito, _, _, _, limao, _ = grafo_simples
    # Mojito tem 3 vizinhos (rum, limão, açúcar)
    assert g.degree(mojito) == 3
    # limão é compartilhado: Mojito + Caipirinha
    assert g.degree(limao) == 2


def test_degree_no_inexistente_levanta_keyerror():
    g = Graph()
    with pytest.raises(KeyError):
        g.degree("drink:fantasma")


def test_all_edges_sem_duplicatas(grafo_simples):
    g, *_ = grafo_simples
    edges = g.all_edges()
    # 6 arestas no total (3 para cada drink)
    assert len(edges) == 6
    # Nenhuma aresta duplicada
    assert len(set(edges)) == len(edges)


def test_is_connected_grafo_conexo(grafo_simples):
    g, *_ = grafo_simples
    assert g.is_connected()


def test_is_connected_grafo_desconexo():
    g = Graph()
    g.add_node("Mojito",     "drink")
    g.add_node("rum",        "ingredient")
    # sem aresta entre eles
    assert not g.is_connected()


def test_is_connected_grafo_vazio():
    g = Graph()
    assert g.is_connected()


# ---------------------------------------------------------------------------
# ingredientes_mais_usados
# ---------------------------------------------------------------------------

def test_ingredientes_mais_usados(grafo_simples):
    g, *_ = grafo_simples
    top = g.ingredientes_mais_usados(top_n=2)
    nomes = [nome for nome, _ in top]
    # limão e açúcar cada um com 2 drinks
    assert "limão"  in nomes
    assert "açúcar" in nomes


def test_ingredientes_mais_usados_respeita_top_n():
    g = Graph()
    d = g.add_node("Mojito", "drink")
    for i in range(5):
        ing = g.add_node(f"ing{i}", "ingredient")
        g.add_edge(d, ing)
    top3 = g.ingredientes_mais_usados(top_n=3)
    assert len(top3) == 3


# ---------------------------------------------------------------------------
# __len__ e __repr__
# ---------------------------------------------------------------------------

def test_len(grafo_simples):
    g, *_ = grafo_simples
    assert len(g) == 6   # 2 drinks + 4 ingredientes


def test_repr_inclui_arestas():
    g = Graph()
    a = g.add_node("Mojito", "drink")
    b = g.add_node("rum",    "ingredient")
    g.add_edge(a, b)
    assert "arestas=1" in repr(g)


# ---------------------------------------------------------------------------
# load_from_json
# ---------------------------------------------------------------------------

def test_load_from_json_constroi_grafo(drinks_json):
    g = load_from_json(str(drinks_json))
    assert len(g.nodes_by_type("drink")) == 3
    # rum, limão, açúcar, hortelã, cachaça = 5 ingredientes únicos
    assert len(g.nodes_by_type("ingredient")) == 5


def test_load_from_json_ingredientes_compartilhados(drinks_json):
    g = load_from_json(str(drinks_json))
    limao_id = g.find_id("limão", "ingredient")
    # Mojito, Caipirinha e Daiquiri usam limão → grau 3
    assert g.degree(limao_id) == 3


def test_load_from_json_receita_mojito(drinks_json):
    g = load_from_json(str(drinks_json))
    mojito_id = g.find_id("Mojito", "drink")
    nomes_ing = {
        g.get_node(n)["name"]
        for n in g.neighbors(mojito_id)
        if g.get_node(n)["type"] == "ingredient"
    }
    assert nomes_ing == {"rum", "limão", "açúcar", "hortelã"}


def test_load_from_json_instrucoes(tmp_path):
    data = {
        "drinks": [
            {
                "nome": "Mojito",
                "ingredientes": ["rum"],
                "instrucoes": "Macere a hortelã...",
            }
        ]
    }
    path = tmp_path / "d.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    g = load_from_json(str(path))
    nid = g.find_id("Mojito", "drink")
    assert "Macere" in g.get_node(nid)["data"]["instrucoes"]


def test_load_from_json_drinks_sem_instrucoes(tmp_path):
    data = {"drinks": [{"nome": "Rum Puro", "ingredientes": ["rum"]}]}
    path = tmp_path / "d.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    g = load_from_json(str(path))
    nid = g.find_id("Rum Puro", "drink")
    assert g.get_node(nid)["data"]["instrucoes"] == ""


def test_load_from_json_drinks_vazio(tmp_path):
    data = {"drinks": []}
    path = tmp_path / "empty.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    g = load_from_json(str(path))
    assert len(g) == 0


def test_load_from_json_grafo_conexo(drinks_json):
    g = load_from_json(str(drinks_json))
    assert g.is_connected()


def test_load_dataset_completo():
    """Smoke test: carrega o JSON real e valida a estrutura mínima."""
    import os
    path = os.path.join(
        os.path.dirname(__file__), "..", "data", "drinks.json"
    )
    g = load_from_json(path)
    assert len(g.nodes_by_type("drink")) >= 10
    assert len(g.nodes_by_type("ingredient")) >= 10
    assert g.is_connected()
    top = g.ingredientes_mais_usados(top_n=1)
    assert top[0][1] >= 3   # o ingrediente mais comum aparece em ≥ 3 drinks