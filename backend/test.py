import os
import shutil
import requests
import json


def load_file(num, folder="pokedex_api"):
    """
    Loads a json file and returns it
    :param num: number of the pokémon
    :param folder: folder name
    :return: returns the json file
    """

    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, str(folder), str(num) + ".json")

    try:
        with open(file_path, "r") as f:
            file = json.load(f)
    except FileNotFoundError:
        raise Exception('The file does not exist.')

    return file


def download_image(number=1, folder='images/portratis'):
    """
    Downloads an image from the parsed jsons
    :param number: number provided to download from
    :param folder: folder to search in
    :return: returns False if both the directory was made and the file exists, otherwise it gets both
    """

    sprite = load_file(number)[0]['sprite']
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, str(folder), str(number) + ".png")

    if not os.path.exists(str(folder)):
        os.mkdir(str(folder))

    if not os.path.exists(file_path):
        r = requests.get(sprite, stream=True)
        if r.status_code == 200:
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return r.status_code

    return False


def download_images(first_index=1):
    """
    Downloads all images starting from a first index, using download_image function
    :param first_index: first number
    :return: None
    """
    index = first_index
    while True:
        download_image(index)
        index += 1


download_images()
