"""
Graph Visualization
------------------
Utilities for generating visual representations of agent graphs.
"""

from framework.graph.edge import EdgeCondition, GraphSpec


def graph_to_mermaid(graph: GraphSpec, direction: str = "TD") -> str:
    """
    Convert a GraphSpec to a Mermaid.js flowchart syntax.

    Args:
        graph: The graph specification to visualize
        direction: Flowchart direction (TD, LR, etc.)

    Returns:
        String containing the Mermaid chart definition
    """
    lines = [f"flowchart {direction}"]
    
    # helper to clean IDs for mermaid
    def clean_id(id_str: str) -> str:
        return id_str.replace("-", "_").replace(" ", "_")

    # 1. Define Nodes with Styling
    for node in graph.nodes:
        nid = clean_id(node.id)
        name = node.name.replace('"', "'")  # Escape quotes
        
        # Shape/Style based on node type
        if node.node_type == "function":
            # Rectangle with rounded corners
            shape_open, shape_close = "(", ")"
        elif node.node_type == "router":
            # Rhombus
            shape_open, shape_close = "{", "}"
        elif node.node_type == "human_input":
            # Parallelogram (input/output)
            shape_open, shape_close = "[/", "/]"
        elif "llm" in node.node_type:
            # Hexagon for AI/LLM
            shape_open, shape_close = "{{", "}}"
        else:
            # Default rectangle
            shape_open, shape_close = "[", "]"

        # Add styling for entry/terminal
        style_class = ""
        if node.id == graph.entry_node:
            style_class = ":::entry"
        elif node.id in graph.terminal_nodes:
            style_class = ":::terminal"
            
        lines.append(f"    {nid}{shape_open}\"{name}\"{shape_close}{style_class}")

    # 2. Define Edges
    for edge in graph.edges:
        source = clean_id(edge.source)
        target = clean_id(edge.target)
        
        # Label based on condition
        label = ""
        if edge.condition == EdgeCondition.ALWAYS:
            arrow = "-->"
        elif edge.condition == EdgeCondition.ON_SUCCESS:
            arrow = "-->"
            label = "|success|"
        elif edge.condition == EdgeCondition.ON_FAILURE:
            arrow = "-.->"
            label = "|failure|"
        elif edge.condition == EdgeCondition.CONDITIONAL:
            arrow = "-->"
            expr = edge.condition_expr or "cond"
            # Truncate long expressions
            if len(expr) > 20:
                expr = expr[:17] + "..."
            label = f"|{expr}|"
        elif edge.condition == EdgeCondition.LLM_DECIDE:
            arrow = "==>"
            label = "|LLM decides|"
        else:
            arrow = "-->"
            label = f"|{edge.condition}|"

        lines.append(f"    {source}{arrow}{label}{target}")

    # 3. Add Router Routes (which are implicit edges)
    for node in graph.nodes:
        if node.node_type == "router" and node.routes:
            source = clean_id(node.id)
            for condition, target_id in node.routes.items():
                target = clean_id(target_id)
                lines.append(f"    {source}-->|{condition}|{target}")

    # 4. Styling Definitions
    lines.append("")
    lines.append("    classDef entry fill:#e1f5fe,stroke:#01579b,stroke-width:2px;")
    lines.append("    classDef terminal fill:#f1f8e9,stroke:#33691e,stroke-width:2px;")
    
    return "\n".join(lines)
