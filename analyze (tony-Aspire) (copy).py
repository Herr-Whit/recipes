import sys
import numpy as np
import pickle
import networkx as nx
from time import sleep
from matplotlib import pyplot as plt


def main():
    f = open('recipes2', 'rb')
    recipes = pickle.load(f)
    f.close()
    print(type(recipes))

    print(type(recipes))
    print(len(recipes))

    G = build_network(recipes[0:2000])
    f = open('network', 'wb')
    pickle.dump(G, f)
    f.close()
    print('Built network')

    fig = plt.subplot(111)
    mcc = max(nx.connected_components(G), key=len)
    mcc_graph = G.subgraph(mcc)
    comp = nx.k_components(mcc_graph)
    print(comp)
    ncolors = []
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
    for node in mcc_graph.nodes:
        found = False
        for i, cluster in enumerate(comp[3]):
            if found:
                continue
            elif node in cluster:
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
                if ingredient in recipe2['extendedIngredients']:
                    count += 1
            if count > 1:
                graph.add_edge(recipe['title'], recipe2['title'])
    return graph


if __name__ == '__main__':
    main()