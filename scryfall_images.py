import datetime
import time
from json import loads
from shutil import copyfileobj

from requests import get


# creates a list from a text file
def file_content():
    file = input("Enter the file name: ")
    with open(file, "r") as f:
        return f.read().splitlines()


# searches scryfall for the card, sets name to lower case and removes all whitespace to get exact match
def card_name():
    search_query = input(r"Enter card name: ")
    return search_query.replace(" ", "").lower()


def get_image(search_query):
    try:
        # grabs the json data for the card
        card = loads(
            get(f"https://api.scryfall.com/cards/search?q={search_query}").text
        )
        # grabs the card image link from the json
        img_url = card["data"][0]["image_uris"]["png"]

        # saves the image, writes to the file in binary mode (better for images)
        with open("image.png", "wb") as out_file:
            copyfileobj(get(img_url, stream=True).raw, out_file)
        last_loop_start = datetime.now()
        _delta = datetime.now() - (last_loop_start + 0.100)
        if _delta.seconds > 0:
            time.sleep(0.100 - _delta.seconds)
    # prints out reason for failure, usually due to missing data from incorrect card name
    except Exception as e:
        print(f"Error Finding Card: {e}")


def mult_images(file):
    for i in file:
        temp = i.replace(" ", "").lower()
        name = i.title()
        try:
            # grabs the json data for the card
            card = loads(get(f"https://api.scryfall.com/cards/search?q={temp}").text)
            # grabs the card image link from the json
            img_url = card["data"][0]["image_uris"]["png"]

            # saves the image, writes to the file in binary mode (better for images)
            with open(f"{name}.png", "wb") as out_file:
                copyfileobj(get(img_url, stream=True).raw, out_file)
        # prints out reason for failure, usually due to missing data from incorrect card name
        except Exception as e:
            print(f"Error Finding Card: {e}")


def options():
    print("Would you like to enter: \n1. A file name\n2. A card name\n3. Exit")
    while True:
        action = action_cleaner()
        if action == 1:
            file = file_content()
            mult_images(file)
            return options()
        elif action == 2:
            search_query = card_name()
            get_image(search_query)
            return options
        elif action == 3:
            exit()
        else:
            print("Invalid Input")


def action_cleaner():
    while True:
        action = input("Enter your selection 1/2: ")
        try:
            action = int(action.strip())
            return action
        except ValueError:
            print("Invalid Input")


def main():
    options()
    return


if __name__ == "__main__":
    main()
