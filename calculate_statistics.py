#!/usr/bin/env python3

import argparse
import networkx as nx

def load_graph(path: str) -> nx.DiGraph:
    """
    Load a directed include graph from a GraphML file.
    """
    try:
        G = nx.read_graphml(path)
    except Exception as e:
        print(f"Error loading GraphML file: {e}")
        raise

    return G

def compute_statistics(G: nx.DiGraph) -> dict:
    """
    Compute various statistics on the include graph.
    """
    stats = {}

    # Node and edge count
    print("Calculating basic metrics (nodes, edges)...")
    stats['num_nodes'] = G.number_of_nodes()
    stats['num_edges'] = G.number_of_edges()

    # Degree metrics
    print("Calculating degree metrics (in/out degrees)...")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    stats['max_in_degree'] = max(in_degrees.values()) if in_degrees else 0
    stats['max_out_degree'] = max(out_degrees.values()) if out_degrees else 0
    stats['top_included_files'] = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    stats['most_including_files'] = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:10]

    # Degree centrality
    print("Calculating degree centrality...")
    stats['degree_centrality'] = nx.degree_centrality(G)
    stats['top_degree_centrality'] = sorted(stats['degree_centrality'].items(), key=lambda x: x[1], reverse=True)[:10]

    # Connected components and cycles
    print("Finding strongly connected components...")
    scc = list(nx.strongly_connected_components(G))
    stats['num_strongly_connected_components'] = len(scc)
    stats['largest_strongly_connected_component_size'] = max((len(c) for c in scc), default=0)

    for c in scc:
        if len(c) == stats['largest_strongly_connected_component_size']:
            stats['largest_strongly_connected_component_nodes'] = []
            for n in c:
                stats['largest_strongly_connected_component_nodes'].append(G.nodes[n]['file'])
            break

    # Detect simple cycles
    print("Finding simple cycles...")
    try:
        cycles = list(nx.simple_cycles(G))
        stats['num_cycles'] = len(cycles)
    except nx.NetworkXNoCycle:
        stats['num_cycles'] = 0

    # Average clustering coefficient
    print("Calculating average directed clustering coefficient...")
    stats['average_clustering'] = nx.average_clustering(G)

    print("Statistics calculation complete.")

    return stats

def print_statistics(stats: dict, G: nx.DiGraph):
    """
    Print the computed statistics.
    """
    def fname(node_id):
        return G.nodes[node_id].get('file', node_id)

    print("Graph Statistics:")
    print(f"- Number of nodes: {stats['num_nodes']}")
    print(f"- Number of edges: {stats['num_edges']}")
    print(f"- Maximum in-degree (most included): {stats['max_in_degree']}")
    print(f"- Maximum out-degree (most including): {stats['max_out_degree']}")

    print("\nTop 10 most included files (in-degree):")
    for node, deg in stats['top_included_files']:
        print(f"  {fname(node)}: {deg}")

    print("\nTop 10 most including files (out-degree):")
    for node, deg in stats['most_including_files']:
        print(f"  {fname(node)}: {deg}")

    print("\nTop 10 nodes by degree centrality:")
    for node, cent in stats['top_degree_centrality']:
        print(f"  {fname(node)}: {cent:.4f}")

    print(f"\nNumber of strongly connected components: {stats['num_strongly_connected_components']}")
    print(f"Size of largest strongly connected component: {stats['largest_strongly_connected_component_size']}")
    print(f"Largest strongly connected component nodes: ")
    for f in stats['largest_strongly_connected_component_nodes']:
        print(f"  {f}")

    print(f"Number of simple cycles: {stats['num_cycles']}")
    print(f"\nAverage clustering coefficient: {stats['average_clustering']:.4f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Analyze a C/C++ include graph stored in GraphML format.")
    parser.add_argument("graphml",
                        help="Path to the GraphML file representing the include graph")
    args = parser.parse_args()

    print(f"Loading graph from {args.graphml}...")

    G = load_graph(args.graphml)

    print("Calculating statistics...")

    stats = compute_statistics(G)
    print_statistics(stats, G)

