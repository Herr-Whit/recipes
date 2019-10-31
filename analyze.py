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

    G = build_network(recipes[0:1000])
    print('Built network')
    fig = plt.subplot(111)
    mcc = max(nx.connected_components(G), key=len)
    nx.draw(G.subgraph(mcc), node_size=1)
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
            if count > 2:
                graph.add_edge(recipe['title'], recipe2['title'])
    return graph








if __name__ == '__main__':
    main()