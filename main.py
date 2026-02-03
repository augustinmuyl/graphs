import networkx as nx
import scipy.sparse.linalg as spla
from graph_operations.generators import create_complete_graph


def compute_graph_properties(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    return num_nodes, num_edges, density


def compute_eigenvalues(G):
    eigenvalues = nx.normalized_laplacian_spectrum(G)
    return eigenvalues


if __name__ == "__main__":
    graph = create_complete_graph()
    nodes, edges, density = compute_graph_properties(graph)
    eigenvalues = compute_eigenvalues(graph)
    print(f"Number of nodes: {nodes}")
    print(f"Number of edges: {edges}")
    print(f"Density of the graph: {density}")
    print(eigenvalues[1], eigenvalues[-1] - eigenvalues[1])
