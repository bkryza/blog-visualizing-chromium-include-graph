import networkx as nx
import argparse

# Function to extract the first directory from a file path
def get_component(file_path):
    parts = file_path.split('/')
    return parts[0]

# Define a mapping from component names to colors (hex codes)
COLOR_MAP = {
    'third_party':  '#33CC33',
    'chrome':       '#FF33FF',
    'components':   '#FF9900',
    'out':          '#00CCCC',
    'content':      '#800000',
    'ui':           '#808000',
    'net':          '#7B68EE',
    'services':     '#0000FF',
    'media':        '#FF66CC',
    'extensions':   '#FF3399',
    'base':         '#20B2AA',
    'remoting':     '#8B4513',
    'cc':           '#87CEEB',
    'gpu':          '#228B22',
    'device':       '#006400',
    'mojo':         '#2F4F4F',
    'v8':           '#800080',
    'storage':      '#008080',
    'google_apis':  '#7FFF00',
    'sandbox':      '#556B2F',
    'pdf':          '#DAA520',
    'ppapi':        '#FF8C00',
    'headless':     '#008B8B',
    'ipc':          '#CD853F',
    'printing':     '#696969',
    'crypto':       '#E0FFFF',
    'gin':          '#FF0000',
    'tools':        '#A9A9A9',
    'skia':         '#DDA0DD',
    'url':          '#008B8B',
    'sql':          '#90EE90',
    'dbus':         '#D3D3D3',
    'testing':      '#C0C0C0',
    'apps':         '#4169E1',
    'build':        '#FF1493',
    'codelabs':     '#FFDAB9',
    'chromeos':     '#FA8072',
    'ash':          '#FF00FF',
}

def add_component_color_and_labels(graphml_file, output_graphml_file):
    G = nx.read_graphml(graphml_file)

    degree_map = dict(G.in_degree())

    top10 = sorted(degree_map, key=lambda n: degree_map[n], reverse=True)[:10]

    for node, data in G.nodes(data=True):
        file_path = data.get('file', '')
        component = get_component(file_path)
        G.nodes[node]['component'] = component
        G.nodes[node]['color'] = COLOR_MAP.get(component, '#000000')
        if node in top10:
            G.nodes[node]['label'] = G.nodes[node].get('file', '')
        else:
            G.nodes[node]['label'] = '____' # This is a hack to force Gephi to not render node id when label is empty

    # 4) Ensure each component has at least one labeled node
    #    (pick the highest-in-degree node in that component)
    #    Skip empty-component ("") if you like
    components = {data['component'] for _, data in G.nodes(data=True) if data.get('component')}
    for comp in components:
        # collect nodes of this component
        comp_nodes = [n for n, d in G.nodes(data=True) if d.get('component') == comp]
        if not comp_nodes:
            continue
        # find the comp-in-degree max
        best = max(comp_nodes, key=lambda n: degree_map.get(n, 0))
        # label it (idempotent if already done)
        G.nodes[best]['label'] = G.nodes[best].get('file', '')

    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Dependencies: {', '.join(sorted(components))}")

    nx.write_graphml(G, output_graphml_file)


def main():
    parser = argparse.ArgumentParser(
        description='Add component, color, and top-10 in-degree labels to each node in a GraphML file.'
    )
    parser.add_argument('input_graphml',  type=str, help='Path to the input GraphML file')
    parser.add_argument('output_graphml', type=str, help='Path for the updated GraphML output')
    args = parser.parse_args()

    add_component_color_and_labels(args.input_graphml, args.output_graphml)
    print(f"Updated GraphML with component, color, and labels saved to {args.output_graphml}")

if __name__ == '__main__':
    main()