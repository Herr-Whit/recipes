from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
import sys
import json
import base64
import numpy as np
import pickle

def main():
    if len(sys.argv) != 3:
        exit(1)
    key = sys.argv[1]
    num = sys.argv[2]

    recipes = get_recipes(key, num)
    print("Got info! Here is...")
    f = open('recipes2', 'wb+')
    pickle.dump(recipes, f)
    f.close()


def get_recipes(key, number, type='random'):
    if type == 'random':
        URL = 'https://api.spoonacular.com/recipes/random?apiKey=' + key + "&number=" + number
    else:
        exit(1)
    params = {
        'number': int(number),
        'apiKey': key
    }
    print(params)
    reply = requests.get(url=URL)
    print(reply.content.decode())
    print(reply.request)
    recipes = reply.content
    return recipes


if __name__ == '__main__':
    main()