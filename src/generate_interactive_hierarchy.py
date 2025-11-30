import re
import html

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

def build_hierarchy(concepts):
    """
    Builds a hierarchical structure from a flat dictionary of concepts.
    """
    nested_concepts = {}
    for cid, data in concepts.items():
        nested_concepts[cid] = data
        nested_concepts[cid]['children'] = []

    root_nodes = []
    for cid, data in concepts.items():
        if data['broader']:
            for parent_id in data['broader']:
                if parent_id in nested_concepts:
                    nested_concepts[parent_id]['children'].append(data)
        else:
            root_nodes.append(data)
    
    # If there's a single root 'modeOfDemise', use that as the entry point
    for node in root_nodes:
        if node['id'] == 'modeOfDemise':
            return [node]

    return root_nodes


def generate_html_recursive(nodes):
    """
    Recursively generates the HTML list for the hierarchy.
    """
    if not nodes:
        return ""
    
    # Sort nodes alphabetically by label
    sorted_nodes = sorted(nodes, key=lambda x: x.get('label', x['id']))
    
    html_str = '<ul>'
    for node in sorted_nodes:
        label = html.escape(node.get('label') or node['id'])
        definition = html.escape(node.get('definition', 'No definition available.'))
        example = html.escape(node.get('example', 'No example available.'))

        html_str += '<li>'
        html_str += f'<span class="concept" data-definition="{definition}" data-example="{example}">{label}</span>'
        
        if node.get('children'):
            html_str += generate_html_recursive(node['children'])
        
        html_str += '</li>'
    html_str += '</ul>'
    return html_str


def main():
    """
    Main function to generate the interactive HTML file.
    """
    with open('../catalogue_MOD.ttl', 'r', encoding='utf-8') as f:
        ttl_content = f.read()

    concepts_dict = parse_ttl_to_dict(ttl_content)
    hierarchy = build_hierarchy(concepts_dict)
    hierarchy_html = generate_html_recursive(hierarchy)

    header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SKOS Hierarchy</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                padding: 2em;
                background-color: #f8f9fa;
                color: #333;
            }}
            h1 {{
                color: #005a9c;
            }}
            ul {{
                list-style-type: none;
                padding-left: 20px;
            }}
            .concept {{
                cursor: pointer;
                padding: 3px 6px;
                border-radius: 5px;
                transition: background-color 0.2s ease-in-out;
                display: inline-block;
            }}
            .concept:hover {{
                background-color: #dee2e6;
            }}
            #tooltip {{
                position: absolute;
                display: none;
                padding: 12px;
                background-color: rgba(0, 0, 0, 0.8);
                color: #fff;
                border-radius: 8px;
                font-size: 0.9em;
                pointer-events: none;
                max-width: 350px;
                z-index: 1000;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            /* Tree-like structure lines */
            li {{
                position: relative;
            }}
            ul > li {{
                margin-top: 5px;
            }}
            ul li::before, ul li::after {{
                content: '';
                position: absolute;
                left: -15px;
            }}
            ul li::before {{
                border-left: 1px solid #adb5bd;
                height: 100%;
                top: 0;
                width: 1px;
            }}
            ul li:last-child::before {{
                height: 1.1em;
            }}
            ul li::after {{
                border-top: 1px solid #adb5bd;
                height: 1px;
                top: 1.1em;
                width: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>Interactive SKOS Vocabulary</h1>
        <div id="hierarchy-container">
    "
    
    footer = """
        </div>
        <div id="tooltip"></div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const concepts = document.querySelectorAll('.concept');
                const tooltip = document.getElementById('tooltip');

                if (!concepts.length) {{
                    console.error("No concepts found. Check HTML generation.");
                    return;
                }}

                concepts.forEach(concept => {{
                    concept.addEventListener('mouseover', function(e) {{
                        const definition = this.getAttribute('data-definition');
                        if (definition) {{
                            tooltip.innerHTML = definition;
                            tooltip.style.display = 'block';
                        }}
                    }});

                    concept.addEventListener('mousemove', function(e) {{
                        tooltip.style.left = (e.pageX + 20) + 'px';
                        tooltip.style.top = (e.pageY + 20) + 'px';
                    }});

                    concept.addEventListener('mouseout', function() {{
                        tooltip.style.display = 'none';
                    }});

                    concept.addEventListener('click', function(e) {{
                        const example = this.getAttribute('data-example');
                        if (example) {{
                            alert('Example:\n' + example.replace(/&quot;/g, '"'));
                        }}
                        e.stopPropagation();
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """

    final_html = header + hierarchy_html + footer
    
    with open('../hierarchy.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("Successfully generated hierarchy.html")

if __name__ == '__main__':
    main()
