import re
from pyvis.network import Network

def parse_ttl_to_dict(ttl_content):
    """
    Parses TTL content into a flat dictionary of concepts.
    """
    concepts = {}
    # Split by empty lines, which separate the blocks for each concept
    for block in re.split(r'\n\s*\n', ttl_content):
        block = block.strip()
        if not block:
            continue

        # Get the concept ID
        id_match = re.match(r':(\w+)', block)
        if not id_match:
            continue
        concept_id = id_match.group(1)
        
        concepts[concept_id] = {
            'id': concept_id,
            'label': '',
            'definition': '',
            'example': '',
            'broader': []
        }

        # Extract properties
        label_match = re.search(r'skos:prefLabel\s+"([^"]+)"', block)
        if label_match:
            concepts[concept_id]['label'] = label_match.group(1)

        def_match = re.search(r'skos:definition\s+"([^"]+)"', block, re.DOTALL)
        if def_match:
            concepts[concept_id]['definition'] = def_match.group(1)

        ex_match = re.search(r'skos:example\s+"([^"]+)"', block, re.DOTALL)
        if ex_match:
            concepts[concept_id]['example'] = ex_match.group(1)

        broader_matches = re.findall(r'skos:broader\s+:(\w+)', block)
        if broader_matches:
            concepts[concept_id]['broader'] = broader_matches

    return concepts

def create_pyvis_visualization(concepts):
    """
    Creates an interactive pyvis network visualization.
    """
    net = Network(height="800px", width="100%", notebook=False, cdn_resources='in_line', directed=True)

    # Add nodes
    for concept_id, data in concepts.items():
        label = data.get('label') or concept_id
        # Use definition for main hover, example can be part of it or a click action if needed
        hover_title = f"Definition: {data.get('definition', 'N/A')}"
        if data.get('example'):
            hover_title += f"\n\nExample: {data['example']}"
            
        net.add_node(concept_id, label=label, title=hover_title, shape='dot')

    # Add edges
    for concept_id, data in concepts.items():
        for broader_id in data.get('broader', []):
            if broader_id in concepts:
                net.add_edge(broader_id, concept_id)
    
    # Set physics and nodes options for a better layout and visible labels
    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 14,
          "face": "arial",
          "color": "black",
          "min": 10,
          "max": 30
        }
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "roundness": 0
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "nodeDistance": 200,
          "damping": 0.09
        },
        "minVelocity": 0.75,
        "solver": "hierarchicalRepulsion"
      }
    }
    """)

    return net

if __name__ == "__main__":
    with open('catalogue_MOD.ttl', 'r', encoding='utf-8') as f:
        ttl_content = f.read()

    concepts_dict = parse_ttl_to_dict(ttl_content)
    
    network = create_pyvis_visualization(concepts_dict)
    
    html = network.generate_html()
    with open('pyvis_hierarchy.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully generated pyvis_hierarchy.html")
