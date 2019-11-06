import sys
import numpy as np
import pickle
import networkx as nx
from time import sleep
from matplotlib import pyplot as plt
from networkx.algorithms import community as cm
import re
import random


def main():
    if not len(sys.argv) == 3:
        print("Use: analyze read/write size")
        exit(1)
    if sys.argv[1] == 'write':
        f = open('res/recipes_balanced', 'rb')
        recipes = pickle.load(f)
        f.close()
        print(len(recipes))

        f = open('res/simple_recipes', 'wb')
        simple_recipes = simplify(recipes)
        simple_recipes = filter_cuisine(simple_recipes)
        pickle.dump(simple_recipes, f)
        f.close()

        G = build_network(random.sample(simple_recipes, int(sys.argv[2])))
        f = open('res/network', 'wb')
        pickle.dump(G, f)
        f.close()
        exit(0)
    elif sys.argv[1] == 'read':
        f = open('res/simple_recipes', 'rb')
        simple_recipes = pickle.load(f)
        f.close()
        f = open('res/network', 'rb')
        G = build_network(random.sample(simple_recipes, int(sys.argv[2])))
        #pickle.load(f)
        f.close()
    else:
        exit(2)

    for recipe in simple_recipes[0:10]:
        print(recipe)
    possible_cuisines = []
    for recipe in simple_recipes:
        for cuisine in recipe['cuisines']:
            if cuisine in possible_cuisines:
                continue
            else:
                possible_cuisines.append(cuisine)

    print(len(simple_recipes))
    print('Built network')

    fig = plt.subplot(111)
    mcc = max(nx.connected_components(G), key=len)
    mcc_graph = G.subgraph(mcc)

    # cliques = list(cm.asyn_lpa_communities(mcc_graph, weight=None, seed=0)) # 6
    # cliques = list(cm.k_clique_communities(mcc_graph, 3))
    cliques = list(cm.greedy_modularity_communities(mcc_graph))
    # cliques = list(cm.label_propagation_communities(mcc_graph))

    print(len(list(cliques)))

    ncolors = []
    # sorted_cliques = sorted(cliques, key=lambda s: len(s))
    for clique in cliques:
        print(clique)
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c',
              '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
              '#000075', '#808080', '#ffffff', '#000000']
    for node in mcc_graph.nodes:
        found = False
        for i, clique in enumerate(cliques[0:10]):
            if found:
                continue
            elif node in set(clique):
                try:
                    ncolors.append(colors[i])
                except IndexError:
                    ncolors.append('black')
                found = True
        if not found:
            ncolors.append('black')

    nx.draw(mcc_graph, node_size=10, line_width=0.005, node_color=ncolors)
    plt.savefig('img/graph.png')
    plt.clf()
    for i in range(len(cliques)):
        try:
            print('\n\n', colors[i], '\n')
            report_stats(cliques[i], simple_recipes, save='img/clique' + str(i) + '.png')
            for node in list(cliques[i])[0:10]:
                print(node)
                print(list(filter(lambda rec: rec['title'] == node, simple_recipes))[0]['cuisines'])
        except IndexError:
            break
    print(possible_cuisines)
    print("Distribution of cuisines:")
    report_stats(G.nodes, simple_recipes)
    report_stats(mcc_graph.nodes, simple_recipes, save='img/baseline.png')
    f = open('img/distribution.png', 'wb')
    plt.savefig(f)
    f.close()
    f = open('res/cliques', 'wb')
    pickle.dump(cliques, f)
    f.close()
    sumn = 0
    for clique in cliques:
        print(len(clique))
        sumn += len(clique)
    print("Number of nodes: ", sumn)


def report_stats(nodes, recipes, save='no'):
    count_ing, count_cuisines = comm_characteristics(nodes, recipes)
    '''try:
        idx = count_cuisines[0].index('European')
        del count_cuisines[1][idx:idx + 1]
        count_cuisines[0].remove('European')
    except ValueError:
        pass
    try:
        idx = count_cuisines[0].index('Eastern European')
        del count_cuisines[1][idx:idx + 1]
        count_cuisines[0].remove('Eastern European')
    except ValueError:
        pass
    try:
        idx = count_cuisines[0].index('Mediterranean')
        del count_cuisines[1][idx:idx + 1]
        count_cuisines[0].remove('Mediterranean')
    except ValueError:
        pass
    try:
        idx = count_cuisines[0].index('Asian')
        del count_cuisines[1][idx:idx + 1]
        count_cuisines[0].remove('Asian')
    except ValueError:
        pass
    '''
    if not save == 'no':
        f = open(save, 'wb')
        plt.subplot(111)
        plt.bar(count_cuisines[0][0:8], count_cuisines[1][0:8])
        plt.savefig(f)
        plt.clf()
        f.close()
    print(count_ing[0])
    print(count_ing[1])
    print(count_cuisines[0])
    print(count_cuisines[1], '\n')


def simplify(recipes):
    simple_recipes = []
    for recipe in recipes:
        simple_recipe = {'title': recipe['title'], 'cuisines': recipe['cuisines'], 'dishTypes': recipe['dishTypes']}
        ingredients = []
        for ingredient in recipe['extendedIngredients']:
            ingredients.append(ingredient['name'])
        simple_recipe['ingredients'] = ingredients
        simple_recipes.append(simple_recipe)
    return simple_recipes


def filter_cuisine(simple_recipes, cuisines=[]):
    filtered = []
    for recipe in simple_recipes:
        '''if len(cuisines) > 0:
            found = False
            for cuisine in cuisines:
                if found:
                    continue
                if cuisine in recipe['cuisines']:
                    found = True
                    filtered.append(recipe)
        else:
            '''
        if len(recipe['cuisines']) > 0:
            filtered.append(recipe)
    return filtered


def build_network(recipes):
    graph = nx.Graph()
    for recipe in recipes:
        graph.add_node(recipe['title'])
    for recipe in recipes:
        for recipe2 in recipes:
            if recipe['title'] == recipe2['title']:
                continue
            count = 0
            # for ingredient in recipe['extendedIngredients']:
            for ingredient in recipe['ingredients']:
                if ingredient in recipe2['ingredients']:
                    count += 1
            if count > 6:
                graph.add_edge(recipe['title'], recipe2['title'])
    return graph


def comm_characteristics(community, recipes):
    ingredients = [[], []]
    cuisines = [[], []]
    for recipe in community:
        recipe = list(filter(lambda rec: rec['title'] == recipe, recipes))[0]
        for ingredient in recipe['ingredients']:
            if ingredient in ingredients[0]:
                ingredients[1][ingredients[0].index(ingredient)] += 1
            else:
                ingredients[0].append(ingredient)
                ingredients[1].append(1)
        for cuisine in recipe['cuisines']:
            if cuisine in cuisines[0]:
                cuisines[1][cuisines[0].index(cuisine)] += 1
            else:
                cuisines[0].append(cuisine)
                cuisines[1].append(1)
    ingredients[1], ingredients[0] = (list(x) for x in zip(*sorted(zip(ingredients[1], ingredients[0]),reverse=True)))
    cuisines[1], cuisines[0] = (list(x) for x in zip(*sorted(zip(cuisines[1], cuisines[0]), reverse=True)))
    return ingredients, cuisines


if __name__ == '__main__':
    main()
