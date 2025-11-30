
import re
import argparse
from graphviz import Digraph

def parse_skos_ttl(ttl_content):
    """
    Parses the SKOS TTL content to extract concepts and their relationships.
    """
    concepts = {}
    current_concept = None

    for line in ttl_content.splitlines():
        line = line.strip()
        if not line or line.startswith('@prefix'):
            continue

        concept_match = re.match(r':(\w+)\s+a\s+skos:Concept', line)
        if concept_match:
            current_concept = concept_match.group(1)
            if current_concept not in concepts:
                concepts[current_concept] = {'broader': [], 'narrower': [], 'label': current_concept}
            continue

        if current_concept:
            prop_match = re.match(r'skos:(\w+)\s+("([^"]+)"|:?(\w+))', line)
            if prop_match:
                prop = prop_match.group(1)
                value = prop_match.group(3) or prop_match.group(4)
                
                if prop == 'broader':
                    concepts[current_concept]['broader'].append(value)
                elif prop == 'narrower':
                    concepts[current_concept]['narrower'].append(value)
                elif prop == 'prefLabel':
                    concepts[current_concept]['label'] = value
    return concepts

def get_descendants(concepts, root_id):
    """
    Get all concepts that are narrower than the given root_id, including the root itself.
    """
    children_map = {cid: [] for cid in concepts}
    for cid, details in concepts.items():
        for broader_id in details.get('broader', []):
            if broader_id in children_map:
                children_map[broader_id].append(cid)

    descendants = set()
    to_visit = [root_id]
    
    while to_visit:
        concept_id = to_visit.pop(0)
        if concept_id in descendants:
            continue
        descendants.add(concept_id)
        if concept_id in children_map:
            to_visit.extend(children_map[concept_id])
            
    return descendants

def generate_dot_graph(concepts, allowed_concepts):
    """
    Generates a DOT graph from the parsed concepts, but only including allowed_concepts.
    """
    dot = Digraph(comment='SKOS Vocabulary')
    dot.attr('node', shape='plaintext')
    dot.attr(rankdir='LR')

    for concept_id in allowed_concepts:
        details = concepts[concept_id]
        label = details.get('label', concept_id)
        dot.node(concept_id, label)

    for concept_id in allowed_concepts:
        details = concepts[concept_id]
        for broader_id in details.get('broader', []):
            if broader_id in allowed_concepts:
                dot.edge(broader_id, concept_id)

    return dot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a visualization for a specific part of a SKOS vocabulary.")
    parser.add_argument("root_concept", help="The root concept ID to start the visualization from.")
    parser.add_argument("output_filename", help="The name of the output file (without extension).")
    args = parser.parse_args()

    with open("../catalogue_MOD.ttl", "r") as f:
        ttl_content = f.read()
    
    all_concepts = parse_skos_ttl(ttl_content)
    
    concepts_to_render = get_descendants(all_concepts, args.root_concept)
    
    dot_graph = generate_dot_graph(all_concepts, concepts_to_render)
    
    dot_graph.render(f'../images/{args.output_filename}', format='png', view=False, cleanup=True)
    print(f"Generated {args.output_filename}.png")

