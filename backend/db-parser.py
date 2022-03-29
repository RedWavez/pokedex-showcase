import os
import json
from settings.database import DB


def load_files(directory, num):
    """
    Load one .json file from a folder and returns that data
    :param directory: directory name
    :param num: pokemon number
    :return: returns json file data
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, directory, str(num) + ".json")

    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        raise Exception('The file does not exist.')

    return json_data


def info_parsing(directories, num, cursor):
    """
    Parse every object from the .json files from diferent folders
    :param cursor:
    :param directories:
    :param num:
    :return:
    """
    try:
        pokeapi_obj = load_files(directories[0], num)
        pokedex_api_obj = load_files(directories[1], num)
    except Exception as e:
        raise e
    # Main =====================================================
    id_num = pokeapi_obj['id']  # Pokemon and index number
    name = pokeapi_obj['name'].title()
    height = pokeapi_obj['height'] / 10
    weight = pokeapi_obj['weight'] / 10
    base_xp = pokeapi_obj['base_experience']
    # Stats ====================================================
    hp = pokeapi_obj['stats'][0]['base_stat']
    attack = pokeapi_obj['stats'][1]['base_stat']
    defense = pokeapi_obj['stats'][2]['base_stat']
    sp_attack = pokeapi_obj['stats'][3]['base_stat']
    sp_def = pokeapi_obj['stats'][4]['base_stat']
    speed = pokeapi_obj['stats'][5]['base_stat']

    if len(pokedex_api_obj[0]["gender"]) > 1:
        male_ratio = pokedex_api_obj[0]["gender"][0]
        female_ratio = pokedex_api_obj[0]["gender"][1]
    else:
        male_ratio = None
        female_ratio = None

    descr = pokedex_api_obj[0]['description']
    sprite = pokedex_api_obj[0]['sprite']

    type1 = pokeapi_obj['types'][0]['type']['name']
    if len(pokeapi_obj['types']) < 2:
        type2 = ""
    else:
        type2 = pokeapi_obj['types'][1]['type']['name']

    n_ability1 = None
    n_ability2 = None
    h_ability = None
    for x in range(0, len(pokeapi_obj['abilities'])):
        y = pokeapi_obj['abilities'][x]['is_hidden']
        if not y:
            if n_ability1 is None:
                n_ability1 = pokeapi_obj['abilities'][x]['ability']["name"]
            else:
                n_ability2 = pokeapi_obj['abilities'][x]['ability']["name"]
        else:
            h_ability = pokeapi_obj['abilities'][x]['ability']["name"]

    # Pokemon ==================================================
    cursor.execute("INSERT INTO pokemon (ID, name, height, weight, descr, base_xp, sprite, hp, attack, def, sp_attack,"
                   "sp_def, speed, male_ratio, female_ratio) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id_num, name, height, weight, descr, base_xp, sprite, hp, attack, defense, sp_attack,
                    sp_def, speed, male_ratio, female_ratio))
    DB.commit()

    # Abilities ================================================
    cursor.execute("INSERT INTO abilities (ID, normal_ability1, normal_ability2, hidden_ability) "
                   "VALUES (%s, %s, %s, %s)", (id_num, n_ability1, n_ability2, h_ability))
    DB.commit()

    # Types =====================================================
    cursor.execute("INSERT INTO types (ID, type1, type2) "
                   "VALUES (%s, %s, %s)", (id_num, type1, type2))
    DB.commit()


if __name__ == '__main__':
    max_files = 26
    for num in range(1, max_files + 1):
        info_parsing(("pokeapi", "pokedex_api"), num)
