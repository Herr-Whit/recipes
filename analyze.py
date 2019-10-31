import sys
import numpy as np
import pickle
import networkx as nx
from time import sleep
from matplotlib import pyplot as plt
from networkx.algorithms import community as cm


def main():
    f = open('recipes2', 'rb')
    recipes = pickle.load(f)
    f.close()
    print(recipes[0]['extendedIngredients'])
    print(len(recipes))

    G = build_network(recipes[0:2000])
    f = open('network', 'wb')
    pickle.dump(G, f)
    f.close()
    print('Built network')

    fig = plt.subplot(111)
    mcc = max(nx.connected_components(G), key=len)
    mcc_graph = G.subgraph(mcc)

    cliques = list(cm.k_clique_communities(mcc_graph, 3))
    print(len(list(cliques)))
    ncolors = []
    sorted_cliques = sorted(cliques, key=lambda s: len(s))
    for clique in sorted_cliques:
        print(clique)
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
    for node in mcc_graph.nodes:
        found = False
        for i, clique in enumerate(cliques):
            if found:
                continue
            elif node in set(clique):
                ncolors.append(colors[i])
                found = True
        if not found:
            ncolors.append('black')

    print("number of nodes:", len(mcc_graph.nodes), '\nnumber of node colors', len(ncolors))

    nx.draw(mcc_graph, node_size=10, line_width=0.5, node_color=ncolors)
    plt.savefig('graph')


def build_network(recipes):
    graph = nx.Graph()
    for recipe in recipes:
        graph.add_node(recipe['title'])
    for recipe in recipes:
        for recipe2 in recipes:
            if recipe['title'] == recipe2['title']:
                continue
            count = 0
            for ingredient in recipe['extendedIngredients']:
                if ingredient['name'] in recipe2['extendedIngredients']['name']:
                    count += 1
            if count > 2:
                graph.add_edge(recipe['title'], recipe2['title'])
    return graph


if __name__ == '__main__':
    main()