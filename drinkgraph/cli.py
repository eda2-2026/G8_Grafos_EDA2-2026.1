"""

Interface de linha de comando. Usa argparse (sem dependências externas).
Exemplos de uso (a partir da raiz do projeto):

    python main.py receita "Mojito"
    python main.py posso-fazer "rum,hortelã,limão,açúcar"
    python main.py relacionados "Mojito" --profundidade 2
"""

import argparse
import re
from pathlib import Path

from . import search
from .loader import load_from_json

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "drinks.json"


def cmd_receita(args, graph):
    try:
        ingredientes = search.receita_do_drink(graph, args.drink)
    except NotImplementedError:
        print("receita_do_drink ainda não foi implementada (Pessoa B).")
        return

    if ingredientes is None:
        print(f'Drink "{args.drink}" não encontrado.')
        return

    print(f"Receita de {args.drink}:")
    for ingrediente in ingredientes:
        print(f"  - {ingrediente}")

    drink_id = graph.find_id(args.drink, "drink")
    if drink_id is not None:
        instrucoes = graph.get_node(drink_id)["data"].get("instrucoes", "").strip()
        if instrucoes:
            print("\nModo de preparo:")
            print(f"  {instrucoes}")


def cmd_posso_fazer(args, graph):
    disponiveis = [
        ingrediente.strip().lower()
        for ingrediente in re.split(r"[,;]", args.ingredientes)
        if ingrediente.strip()
    ]
    try:
        drinks = search.o_que_posso_fazer(graph, disponiveis)
    except NotImplementedError:
        print("o_que_posso_fazer ainda não foi implementada (Pessoa B).")
        return

    if not drinks:
        print("Nenhum drink pode ser feito com esses ingredientes ainda.")
        return

    print("Você pode fazer:")
    for nome in drinks:
        print(f"  - {nome}")


def cmd_relacionados(args, graph):
    if args.profundidade < 1:
        print("A profundidade deve ser um número inteiro positivo.")
        return

    try:
        relacionados = search.drinks_relacionados(graph, args.drink, args.profundidade)
    except NotImplementedError:
        print("drinks_relacionados ainda não foi implementada (Pessoa B).")
        return

    if relacionados is None:
        print(f'Drink "{args.drink}" não encontrado.')
        return

    if not relacionados:
        print(f"Nenhum drink relacionado encontrado para {args.drink}.")
        return

    print(f"Drinks relacionados a {args.drink} (profundidade {args.profundidade}):")
    for nome in relacionados:
        print(f"  - {nome}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="drinkgraph",
        description="Busca de drinks em um grafo de ingredientes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Use aspas para nomes de drinks ou listas de ingredientes com espaços.",
    )
    parser.add_argument(
        "--data",
        default=str(DATA_PATH),
        help="Caminho do JSON com os drinks",
    )
    parser.add_argument("--version", action="version", version="drinkgraph 1.0")

    sub = parser.add_subparsers(dest="comando", required=True)

    p_receita = sub.add_parser("receita", help="Mostra a receita de um drink")
    p_receita.add_argument("drink", help="Nome do drink")
    p_receita.set_defaults(func=cmd_receita)

    p_posso = sub.add_parser(
        "posso-fazer",
        help="Lista drinks possíveis com os ingredientes informados",
    )
    p_posso.add_argument(
        "ingredientes",
        help="Ingredientes disponíveis, separados por vírgula ou ponto-e-vírgula",
    )
    p_posso.set_defaults(func=cmd_posso_fazer)

    p_rel = sub.add_parser(
        "relacionados",
        help="Lista drinks relacionados via ingredientes compartilhados",
    )
    p_rel.add_argument("drink", help="Nome do drink")
    p_rel.add_argument(
        "--profundidade",
        type=int,
        default=3,
        help="Profundidade máxima para buscar drinks relacionados",
    )
    p_rel.set_defaults(func=cmd_relacionados)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    graph = load_from_json(args.data)
    args.func(args, graph)


if __name__ == "__main__":
    main()
