import re

def parse_ttl_to_dict(ttl_content):
    """
    Parses TTL content into a flat dictionary of concepts, extracting broader and narrower relationships.
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
            'broader': [],
            'narrower': [] # Added for easier traversal
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
            concepts[concept_id]['broader'].extend(broader_matches)
            
        narrower_matches = re.findall(r'skos:narrower\s+:(\w+)', block)
        if narrower_matches:
            concepts[concept_id]['narrower'].extend(narrower_matches)

    return concepts

def count_descendants(concepts, root_id):
    """
    Counts all direct and indirect narrower concepts for a given root_id.
    """
    # Build a true 'children' map as 'narrower' is not always explicit for all concepts
    children_map = {cid: [] for cid in concepts}
    for cid, data in concepts.items():
        for broader_id in data.get('broader', []):
            if broader_id in children_map:
                children_map[broader_id].append(cid)
    
    descendants = set()
    to_visit = [root_id]
    
    while to_visit:
        current_id = to_visit.pop(0)
        
        # Add to descendants if not the root itself and not already counted
        if current_id != root_id and current_id not in descendants:
            descendants.add(current_id)
        
        # Add children to the list to visit
        for child_id in children_map.get(current_id, []):
            if child_id not in descendants: # Prevent cycles and redundant visits
                to_visit.append(child_id)
                
    return len(descendants)

if __name__ == "__main__":
    with open('../catalogue_MOD.ttl', 'r', encoding='utf-8') as f:
        ttl_content = f.read()

    all_concepts = parse_ttl_to_dict(ttl_content)

    categories = [
        "naturalSupernaturalCauses",
        "physicalViolence",
        "indirectOrPsychologicalModes"
    ]

    print("Number of modes of demise for each upper category:")
    for category_id in categories:
        if category_id in all_concepts:
            count = count_descendants(all_concepts, category_id)
            label = all_concepts[category_id].get('label', category_id)
            print(f"- {label}: {count} modes")
        else:
            print(f"- Category '{category_id}' not found.")
