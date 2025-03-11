import asyncio
from time import perf_counter

import aiohttp


# creates a list from a text file
def file_content():
    file = input("Enter the file name: ")
    with open(file, "r") as f:
        return f.read().splitlines()


# searches scryfall for the card, sets name to lower case and removes all whitespace to get exact match
def card_name():
    search_query = input(r"Enter card name: ")
    temp = search_query.strip().title()
    return search_query.replace(" ", "").lower(), temp


async def get_image(session, search_query, temp):
    try:
        # grabs the json data for the card
        async with session.get(
            f"https://api.scryfall.com/cards/search?q={search_query}"
        ) as response:
            card = await response.json()
        # grabs the card image link from the json
        image_url = card["data"][0]["image_uris"]["png"]

        async with session.get(image_url) as img_response:
            image_data = await img_response.read()
        # saves the image, writes to the file in binary mode (better for images)
        with open(f"{temp}.png", "wb") as out_file:
            out_file.write(image_data)
    # prints out reason for failure, usually due to missing data from incorrect card name
    except Exception as e:
        print(f"Error Finding Card: {e}")


async def mult_images(file, session):
    print(perf_counter())
    last_request_time = perf_counter()
    tasks = []
    for i in file:
        elapsed_time = perf_counter() - last_request_time
        if elapsed_time < 0.1:
            await asyncio.sleep(0.1 - elapsed_time)
        temp = i.strip().title()
        search_query = i.strip().lower()

        task = asyncio.ensure_future(get_image(session, search_query, temp))
        tasks.append(task)
        last_request_time = perf_counter()

    await asyncio.gather(*tasks)
    print(perf_counter())


async def options():
    print("Would you like to enter: \n1. A file name\n2. A card name\n3. Exit")
    while True:
        action = action_cleaner()
        if action == 1:
            file = file_content()
            async with aiohttp.ClientSession() as session:
                await mult_images(file, session)
            return await options()
        elif action == 2:
            search_query, temp = card_name()
            async with aiohttp.ClientSession() as session:
                await get_image(session, search_query, temp)
            return await options()
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
    asyncio.run(options())
    return


if __name__ == "__main__":
    main()
