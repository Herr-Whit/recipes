import requests
import sys
import json
import pickle


def main():
    if len(sys.argv) != 3:
        exit(1)
    key = sys.argv[1]
    num = sys.argv[2]

    f = open('recipes2', 'rb')
    recipes2 = pickle.load(f)
    f.close()
    f = open('recipes2', 'wb')

    recipes = []
    while True:
        batch = get_recipes(key, num)
        if len(batch) > 0:
            recipes = recipes + batch
        else:
            break

    pickle.dump(recipes2 + recipes, f)
    f.close()


def get_recipes(key, number, type='random'):
    if type == 'random':
        URL = 'https://api.spoonacular.com/recipes/random?apiKey=' + key + "&number=" + number
    else:
        exit(1)
    reply = requests.get(url=URL)
    if not reply.ok:
        print('response not ok!')
        print(reply.status_code)
        return []
    recipes = reply.content
    return json.loads(recipes.decode())['recipes']


if __name__ == '__main__':
    main()
