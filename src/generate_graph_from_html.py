
from bs4 import BeautifulSoup
from graphviz import Digraph
import uuid

def add_nodes_and_edges(dot, parent_node, parent_id):
    """
    Recursively adds nodes and edges to the Digraph from the parsed HTML list.
    """
    # Direct children of the parent_node are 'li' elements
    # But BeautifulSoup structure is a bit more nested.
    # We need to find the 'ul' that is a sibling to the span of the parent, or within the li.
    ul_tag = parent_node.find('ul')
    if not ul_tag:
        return

    # Each li in this ul is a child concept
    for li in ul_tag.find_all('li', recursive=False):
        span = li.find('span', class_='concept')
        if span:
            child_id = str(uuid.uuid4()) # Generate a unique ID for the node
            label = span.get_text(strip=True)
            example = span.get('data-example', 'No example available.')

            # Add the node for the child
            dot.node(child_id, label, tooltip=example)
            # Add an edge from the parent to the child
            dot.edge(parent_id, child_id)
            
            # Recurse for the children of this new node
            add_nodes_and_edges(dot, li, child_id)


def create_graph_from_html(html_content):
    """
    Creates a graph from the HTML hierarchy.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    dot = Digraph(comment='Concept Graph')
    dot.attr('node', shape='box', style='rounded')

    # Find the root concept to start
    container = soup.find(id='hierarchy-container')
    if not container:
        return None
        
    root_li = container.find('li')
    if root_li:
        root_span = root_li.find('span', class_='concept')
        if root_span:
            root_id = str(uuid.uuid4())
            label = root_span.get_text(strip=True)
            example = root_span.get('data-example', 'No example available.')
            
            dot.node(root_id, label, tooltip=example)
            
            # Start the recursive process
            add_nodes_and_edges(dot, root_li, root_id)

    return dot

if __name__ == "__main__":
    with open('hierarchy.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    graph = create_graph_from_html(html_content)
    
    if graph:
        graph.render('concept_graph', format='png', view=False, cleanup=True)
        print("Successfully generated concept_graph.png")
    else:
        print("Error: Could not generate the graph. Check the HTML structure.")
