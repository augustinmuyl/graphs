import networkx as nx
import scipy.sparse.linalg as spla


def create_graph():
    G = nx.complete_graph(100)
    return G


def compute_graph_properties(G):
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    return num_nodes, num_edges, density


def compute_eigenvalues(G, k=5):
    L = nx.normalized_laplacian_matrix(G)
    eigenvalues = spla.eigsh(L, k=k, which="SM", return_eigenvectors=False)
    return eigenvalues


if __name__ == "__main__":
    graph = create_graph()
    nodes, edges, density = compute_graph_properties(graph)
    eigenvalues = compute_eigenvalues(graph, k=1)
    print(f"Number of nodes: {nodes}")
    print(f"Number of edges: {edges}")
    print(f"Density of the graph: {density}")
    print(f"Top {len(eigenvalues)} eigenvalues: {eigenvalues}")
