import networkx as nx
import numpy as np
import glob

datadir = 'raw'

def get_egos():
    paths = glob.glob("%s/*.edges" % (datadir,))
    egos = [int(x.split("/")[-1].split('.')[0]) for x in paths]
    return egos

def construct_network(ego):
    fname = "%s/%d.edges" % (datadir, ego)
    f = open(fname,'r')
    net = nx.DiGraph()
    for line in f:
        nodes = [int(x) for x in line.strip().split(' ')]
        [net.add_edge(ego, node) for node in nodes]
        net.add_edge(*nodes)
    f.close()
    return net
    

def process(adjacency=True):
    egos = get_egos()
    networks = [construct_network(ego) for ego in egos]
    if adjacency:
        max_nodes = max([n.number_of_nodes() for n in networks])
        X = np.zeros((len(networks), max_nodes**2))
        for i,network in enumerate(networks):
            X[i] = np.resize(nx.adjacency_matrix(network), max_nodes**2) #network.number_of_nodes()**2)
        return X
    else:
        return networks
