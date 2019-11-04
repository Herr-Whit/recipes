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
    recipes = []
    while True:
        more = get_recipes(key, num)
        if len(more) > 0:
            recipes = recipes + get_recipes(key, num)
        else:
            break
    print("Got info! Here is...")
    f = open('recipes_main', 'wb')
    pickle.dump(recipes, f)
    f.close()


def get_recipes(key, number, type='random'):
    if type == 'random':
        URL = 'https://api.spoonacular.com/recipes/random?apiKey=' + key + "&number=" + number + "&dishTypes=main_course" + "&vegetarian=false&vegan=false&glutenFree=false&dairyFree=false&veryPopular=false"
    else:
        exit(1)
    params = {
        'number': int(number),
        'apiKey': key
    }
    print(params)
    reply = requests.get(url=URL)
    if reply.status_code == 200:
        print(reply.content.decode())
        print(reply.request)
        recipes = json.loads(reply.content.decode())
        return recipes['recipes']
    else:
        return []


if __name__ == '__main__':
    main()