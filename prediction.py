import sys
import numpy as np
import pickle
import networkx as nx
from time import sleep
from matplotlib import pyplot as plt
from networkx.algorithms import community as cm
from termcolor import colored
import re

def main():
    f = open('network', 'rb')
    G = pickle.load(f)
    f.close()
    f = open('simple_recipes', 'rb')
    simple_recipes = pickle.load(f)
    f.close()

    for recipe in simple_recipes[0:10]:
        print(recipe)
    possible_cuisines = []
    for recipe in simple_recipes:
        for cuisine in recipe['cuisines']:
            if cuisine in possible_cuisines:
                continue
            else:
                possible_cuisines.append(cuisine)
    for recipe in simple_recipes[1500:2000]:



if __name__ == '__main__':
    main()