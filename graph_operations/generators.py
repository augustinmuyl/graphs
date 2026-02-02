import networkx as nx


def create_graph():
    G = nx.complete_graph(100)
    return G


def create_erdos_renyi_graph(n=100, p=0.05):
    G = nx.erdos_renyi_graph(n, p)
    return G


def create_small_world_graph(n=100, k=4, p=0.1):
    G = nx.watts_strogatz_graph(n, k, p)
    return G


def create_scale_free_graph(n=100):
    G = nx.barabasi_albert_graph(n, 3)
    return G
