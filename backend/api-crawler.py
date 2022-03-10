import os, requests, json, time

# TODO: Utilizar o seguinte modelo para o nome do ficheiro '1 - [pokemon name]'

dirpath = os.path.dirname(os.path.abspath(__file__))

def crawl_them_all():
    """
    Função para transferir de forma incrementada cada API response de cada pokemon
    """
    number = 1
    while True:
        api = f"https://pokeapi.co/api/v2/pokemon/{number}"
        answer = requests.get(api)

        if answer.status_code != 200:
            print("> We have 'em all!")
            break

        with open(f"{dirpath}/pokelist/{number}.json", "w", encoding="utf8") as json_file:
            json.dump(json.loads(answer.text), json_file, indent=4)
        print(f"Pokémon {number} guardado com êxito!")

        number += 1


if __name__ == '__main__':
    crawl_them_all()
