"""
Test the graph visualization module.
"""

from framework.graph.edge import EdgeCondition, EdgeSpec, GraphSpec
from framework.graph.node import NodeSpec
from framework.graph.visualize import graph_to_mermaid


def test_graph_to_mermaid():
    """Test generating a Mermaid diagram from a GraphSpec."""
    # Create a dummy graph
    node1 = NodeSpec(id="start", name="Start Node", description="Entry", node_type="function")
    node2 = NodeSpec(id="process", name="AI Processor", description="LLM", node_type="llm_generate")
    node3 = NodeSpec(id="end", name="End Node", description="Terminal", node_type="function")
    
    edge1 = EdgeSpec(id="e1", source="start", target="process", condition=EdgeCondition.ALWAYS)
    edge2 = EdgeSpec(id="e2", source="process", target="end", condition=EdgeCondition.ON_SUCCESS)
    edge3 = EdgeSpec(id="e3", source="process", target="start", condition=EdgeCondition.ON_FAILURE)
    
    graph = GraphSpec(
        id="test-graph",
        goal_id="test",
        entry_node="start",
        terminal_nodes=["end"],
        nodes=[node1, node2, node3],
        edges=[edge1, edge2, edge3]
    )
    
    mermaid = graph_to_mermaid(graph)
    
    # Check for expected syntax
    assert "flowchart TD" in mermaid
    
    # Check nodes are present
    assert "start" in mermaid
    assert "process" in mermaid
    assert "end" in mermaid
    
    # Check styling classes
    assert ":::entry" in mermaid
    assert ":::terminal" in mermaid
    
    # Check shapes
    assert '("Start Node")' in mermaid       # function -> rounded
    assert '{{"AI Processor"}}' in mermaid   # llm -> hexagon
    
    # Check edges
    assert "-->|success|" in mermaid
    assert "-.->|failure|" in mermaid
