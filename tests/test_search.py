import pytest

from drinkgraph.graph import Graph
from drinkgraph import search


def _grafo_exemplo():
    """
    Mojito --- rum
    Mojito --- limão
    Caipirinha --- cachaça
    Caipirinha --- limão   (limão é compartilhado)
    """
    g = Graph()
    mojito = g.add_node("Mojito", "drink")
    rum = g.add_node("rum", "ingredient")
    limao = g.add_node("limão", "ingredient")
    caipirinha = g.add_node("Caipirinha", "drink")
    cachaca = g.add_node("cachaça", "ingredient")

    g.add_edge(mojito, rum)
    g.add_edge(mojito, limao)
    g.add_edge(caipirinha, cachaca)
    g.add_edge(caipirinha, limao)

    return g, mojito, rum, limao, caipirinha, cachaca


def test_bfs_alcanca_nos_conectados_com_distancia_correta():
    g, mojito, rum, limao, caipirinha, cachaca = _grafo_exemplo()

    resultado = search.bfs(g, mojito)

    assert resultado[mojito]["distancia"] == 0
    assert resultado[rum]["distancia"] == 1
    assert resultado[limao]["distancia"] == 1
    # Caipirinha só é alcançada passando por limão -> distância 2
    assert resultado[caipirinha]["distancia"] == 2
    assert resultado[cachaca]["distancia"] == 3


def test_bfs_respeita_max_depth():
    g, mojito, rum, limao, caipirinha, cachaca = _grafo_exemplo()

    resultado = search.bfs(g, mojito, max_depth=1)

    assert rum in resultado
    assert limao in resultado
    assert caipirinha not in resultado  # estaria a distância 2


def test_bfs_no_inexistente_levanta_erro():
    g, *_ = _grafo_exemplo()
    with pytest.raises(KeyError):
        search.bfs(g, "drink:nao-existe")


def test_reconstruir_caminho():
    g, mojito, rum, limao, caipirinha, cachaca = _grafo_exemplo()

    resultado = search.bfs(g, mojito)
    caminho = search.reconstruir_caminho(resultado, caipirinha)

    assert caminho[0] == mojito
    assert caminho[-1] == caipirinha
    assert limao in caminho  # passa pelo ingrediente compartilhado


# ---------------------------------------------------------------------------
# Gabarito para quando vocês implementarem as funções em search.py.
# Por enquanto, esses testes só confirmam que elas ainda não foram feitas.
# Substituam pelo @pytest.mark.skip / pelo teste real conforme for implementando.
# ---------------------------------------------------------------------------

def test_receita_do_drink():
    g, mojito, rum, limao, _, _ = _grafo_exemplo()

    ingredientes = search.receita_do_drink(g, "Mojito")
    assert set(ingredientes) == {"rum", "limão"}

    assert search.receita_do_drink(g, "Nao Existe") is None


def test_o_que_posso_fazer():
    g, mojito, rum, limao, caipirinha, cachaca = _grafo_exemplo()

    assert search.o_que_posso_fazer(g, ["rum", "limão"]) == ["Mojito"]
    assert search.o_que_posso_fazer(g, ["cachaça", "limão"]) == ["Caipirinha"]
    assert search.o_que_posso_fazer(g, ["limão"]) == []


def test_drinks_relacionados():
    g, mojito, rum, limao, caipirinha, cachaca = _grafo_exemplo()

    assert search.drinks_relacionados(g, "Mojito", profundidade=2) == ["Caipirinha"]
    assert search.drinks_relacionados(g, "Mojito", profundidade=1) == []
    assert search.drinks_relacionados(g, "Nao Existe") is None
