import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")


def fetch_data(name: str) -> dict:
    """ Fetches data from the API """
    url = f"https://api.api-ninjas.com/v1/animals?name={name}"
    headers = {
        "X-Api-Key": API_NINJAS_KEY
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == requests.codes.ok:
        return response.json()
    response.raise_for_status()


def get_animals_data(name: str, skin_type: str) -> dict[str, dict[str, str]]:
    """ Returns a dictionary with the relevant data for each animal """
    full_animals_data = fetch_data(name)

    animals_data = {}
    for animal in full_animals_data:
        try:
            animal_skin_type = animal["characteristics"]["skin_type"]
        except KeyError:
            animal_skin_type = "not specified"

        if skin_type != animal_skin_type and skin_type != "All":
            continue

        animals_data[animal["name"]] = {
            "taxonomy": " >> ".join(animal["taxonomy"].values()),
            "Diet": animal.get("characteristics", {}).get("diet", None),
            "Type": animal.get("characteristics", {}).get("type", None),
            "Lifespan": animal.get("characteristics", {}).get("lifespan", None),
            "Location": " and ".join(animal.get("locations", None))
        }

        to_remove = [] # remove the key if the value is None
        for key, value in animals_data[animal["name"]].items():
            if value is None:
                to_remove.append(key)
        for key in to_remove:
            del animals_data[animal["name"]][key]

    return animals_data