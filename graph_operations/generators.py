import networkx as nx


def create_complete_graph(n=100):
    return nx.complete_graph(n)


def create_erdos_renyi_graph(n=100, p=0.05):
    return nx.erdos_renyi_graph(n, p)


def create_small_world_graph(n=100, k=4, p=0.1):
    return nx.watts_strogatz_graph(n, k, p)


def create_scale_free_graph(n=100, m=3):
    return nx.barabasi_albert_graph(n, m)
