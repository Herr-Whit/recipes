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
    f = open('recipes_balanced', 'rb')
    recipes = pickle.load(f)
    f.close()
    print('loaded ', len(recipes), ' recipes')
    cuisines = ['American', 'European', 'Asian', 'South American', 'African', 'Mexican']
    while True:
        for cuisine in cuisines:
            print('Get ' + cuisine + ' dishes')
            more = get_recipes(key, num, cuisine)
            if len(more) > 0:
                recipes = recipes + more
            else:
                break
        if len(more) == 0:
            break

    print("Got info! Here is...")
    f = open('res/recipes_balanced', 'wb')
    pickle.dump(recipes, f)
    f.close()


def get_recipes(key, number, cuisine, type='random'):
    if type == 'random':
        cuisines = '&cuisines=' + cuisine
        preferences = "&vegetarian=false&vegan=false&glutenFree=false&dairyFree=false&veryPopular=false"
        URL = 'https://api.spoonacular.com/recipes/random?apiKey=' + key + "&number=" + number + "&dishTypes=main_course" + preferences + cuisines
    else:
        exit(1)
    params = {
        'number': int(number),
        'apiKey': key
    }
    print(params)
    reply = requests.get(url=URL)
    if reply.status_code == 200:
        print('Ok!')
        recipes = json.loads(reply.content.decode())
        return recipes['recipes']
    else:
        print('not ok: ', reply.status_code)
        return []


if __name__ == '__main__':
    main()