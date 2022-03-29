import requests
import json
import shutil
from pathlib import Path, PurePath
# from mysql-connect import loadfiles

# Path to backend directory
working_dir = Path.cwd()

pokedex_api_url = 'https://pokeapi.glitch.me/v1/pokemon/'
pokedex_api_folder = Path(f'{working_dir}/pokedex_api')
pokedex_api_image_folder = Path(f'{working_dir}/images/portraits')

pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'
pokeapi_folder = Path(f'{working_dir}/pokeapi')
pokeapi_image_folder = Path(f'{working_dir}/images/sprites')

# Dictionary with all the menu options
menu_options = {1: 'Scrape APIs',
                2: 'Download images',
                3: 'Exit'}


def print_menu():
    """
    Prints the menu based on the dictionary keys and values
    """
    print(f"\n╔═══════ Menu ═══════╗")
    for key in menu_options.keys():
        print(' ', key, '-', menu_options[key])
    print(f"╚════════════════════╝")


def check_folders(folders):
    """
    Create and check if folders and subfolders exist based on the choosen option
    :param folders: List of folders to be created
    """
    try:
        # If option 1 then creates 2 folders by looping keys from a list
        if folders == ['pokeapi2', 'pokedex_api2']:
            for folder in folders:
                Path(folder).mkdir()
            print(f'\n[INFO] Folders "pokeapi2" and "pokedex_api2" were created. Proceeding...')

        # If option 2 then creates 1 folder and 2 subfolders by looping keys from a list
        if folders == ['sprites', 'portraits']:
            for folder in folders:
                Path('images', folder).mkdir(parents=True)
            print(f'\n[INFO] Folder "images" and subfolders "sprites" and "portraits" were created. Proceeding...')

    except FileExistsError:
        print(f'\n[WARNING] Folder or subfolder already exists! Proceeding...')


def scrape_apis(folders, url_choice):
    """
    Scrape API responses in .json format from each pokemon
    """
    check_folders(folders)

    if url_choice == 'a':
        folder = 'pokeapi2'
        url = pokeapi_url
    elif url_choice == 'b':
        folder = 'pokedex_api2'
        url = pokedex_api_url
    else:
        print("[ERROR] You must either type 'a' or 'b'.")
        return

    # While loop only starts if input is either 'a' or 'b'
    number = 1
    while True:
        api = url+f'/{number}'
        answer = requests.get(api)

        if answer.status_code != 200:
            print('> We have \'em all!')
            break

        with open(Path(working_dir, folder, f'{number}.json'), 'w') as json_file:
            json.dump(json.loads(answer.text), json_file, indent=4)
        print(f'Pokémon {number} saved successfully!')

        number += 1
        if number == 10:
            break


def download_images(folders, url_choice):
    """
    Scrape all images
    """
    check_folders(folders)

    target_directory = PurePath.joinpath(working_dir, "images")

    max_files = 730
    for num in range(715, max_files + 1):
        path = PurePath.joinpath(pokedex_api_folder, str(num) + ".json")
        with open(path, "r") as json_file:
            pokedex_api_obj = json.load(json_file)
        img_url = pokedex_api_obj[0]['sprite']

        with open(f'{target_directory}/{num}.png', 'wb') as handle:
            response = requests.get(img_url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)


if __name__ == '__main__':
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('> Enter your choice: '))

            # Check what choice was entered and act accordingly
            if option == 1:
                print("- a) Poke API\n- b) Pokedex API")
                api_choice = str(input("> Choose the API: "))
                scrape_apis(['pokeapi2', 'pokedex_api2'], api_choice)
                input('[INFO] Press "Enter" to continue...')
            elif option == 2:
                print("- a) Poke API\n- b) Pokedex API")
                api_choice = str(input("> Choose the API: "))
                download_images(['sprites', 'portraits'], api_choice)
                input('[INFO] Press "Enter" to continue...')
            elif option == 3:
                print('[INFO] Thank you. See you next time!')
                exit()
            else:
                print('Invalid option. Please enter a number between 1 and 3.')
        except ValueError:
            print('Wrong input. Please enter a number...')
