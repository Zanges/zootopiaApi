import requests
import os
from dotenv import load_dotenv


load_dotenv()

API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")


# def load_data(file_path: str) -> dict:
#     """ Loads a JSON file """
#     with open(file_path, "r") as handle:
#         return json.load(handle)


def load_html_template(file_path: str) -> str:
    """ Loads an HTML file """
    with open(file_path, "r") as handle:
        return handle.read()


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


def build_animal_info_html(animal_name: str, animal_data: dict[str, str]) -> str:
    """ Returns the HTML code for the information of an animal """
    html_code = '<li class="cards__item">\n'
    html_code += f'<div class="card__title">{animal_name}</div>\n'
    html_code += f'<p class="card__taxonomy">{animal_data["taxonomy"]}</p>\n'
    html_code += '<ul class="card__info">\n' # cant wrap an ul in a p tag. mistake in the guide
    for key, value in animal_data.items():
        if key != "taxonomy":
            html_code += f'<li><strong>{key}:</strong> {value}</li>\n'
    html_code += '</ul>\n</li>\n'
    return html_code


def get_possible_skin_types(name: str) -> list[str]:
    """ Returns the possible skin types of the animals """
    full_animals_data = fetch_data(name)
    skin_types = set()
    for animal in full_animals_data:
        if "characteristics" in animal and "skin_type" in animal["characteristics"]:
            skin_types.add(animal["characteristics"]["skin_type"])
    return list(skin_types)


def get_user_input_animal() -> str:
    """ Asks the user for the name of the animal """
    while True:
        user_input = input("Enter the name of the animal: ")
        if user_input.isalpha():
            return user_input
        print("Invalid input. Please try again.")


def get_user_input_skin(name: str) -> str:
    """ Asks the user for the skin type of the animals """
    skin_types = get_possible_skin_types(name)
    print("Possible skin types:")
    print("All")
    for skin_type in skin_types:
        print(skin_type)
    while True:
        try:
            skin_type = input("Enter the skin type of the animals: ")
            if skin_type in skin_types or skin_type == "All":
                return skin_type
            else:
                print("Invalid skin type. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def build_query_error_html(query_name: str) -> str:
    """ Returns the HTML code for the error message """
    return f'<p class="error">No animals found<br>with the name<br>"{query_name}".</p>'


def main():
    new_html = load_html_template("animals_template.html")
    query_name = get_user_input_animal()
    skin_type = get_user_input_skin(query_name)
    animals_data = get_animals_data(query_name, skin_type)
    html_animals_data = ""
    if not animals_data:
        html_animals_data = build_query_error_html(query_name)
    for animal_name, animal_data in animals_data.items():
        html_animals_data += build_animal_info_html(animal_name, animal_data)
    new_html = new_html.replace("__REPLACE_ANIMALS_INFO__", html_animals_data)
    with open("animals.html", "w") as handle:
        handle.write(new_html)
    print("The HTML file has been generated.")
    print(">>> animals.html")


if __name__ == "__main__":
    main()