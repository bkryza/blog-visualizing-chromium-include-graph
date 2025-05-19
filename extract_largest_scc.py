#!/usr/bin/env python3

import argparse
import networkx as nx


def load_graph(path: str) -> nx.DiGraph:
    """Read GraphML file."""
    G = nx.read_graphml(path)
    return G


def largest_scc_subgraph(G: nx.DiGraph) -> nx.DiGraph:
    """
    Return the subgraph induced by the largest SCC in `G`.
    """
    sccs = list(nx.strongly_connected_components(G))
    if not sccs:
        return G.__class__()
    largest = max(sccs, key=len)
    return G.subgraph(largest).copy()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Extract the largest strongly connected component from a GraphML "
            "file and write it back in GraphML format."
        )
    )
    parser.add_argument("input", help="Path to the input GraphML file.")
    parser.add_argument("output", help="Where to save the extracted subgraph.")
    args = parser.parse_args(argv)

    G = load_graph(args.input)

    H = largest_scc_subgraph(G)

    nx.write_graphml(H, args.output)
    print(
        f"Wrote largest SCC ({H.number_of_nodes()} nodes, "
        f"{H.number_of_edges()} edges) to '{args.output}'."
    )

if __name__ == "__main__":
    main()