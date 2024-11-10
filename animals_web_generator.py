import json


def load_data(file_path: str) -> dict:
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def load_html_template(file_path: str) -> str:
    """ Loads an HTML file """
    with open(file_path, "r") as handle:
        return handle.read()


def get_animals_data(skin_type: str) -> dict[str, dict[str, str]]:
    """ Returns a dictionary with the relevant data for each animal """
    full_animals_data = load_data("animals_data.json")

    animals_data = {}
    for animal in full_animals_data:
        try:
            animal_skin_type = animal["characteristics"]["skin_type"]
        except KeyError:
            animal_skin_type = "not specified"

        if skin_type != animal_skin_type and skin_type != "All":
            continue

        animal_data = {}
        animal_data["taxonomy"] = " >> ".join(animal["taxonomy"].values())
        if "characteristics" in animal:
            if "diet" in animal["characteristics"]:
                animal_data["Diet"] = animal["characteristics"]["diet"]
            if "type" in animal["characteristics"]:
                animal_data["Type"] = animal["characteristics"]["type"]
            if "lifespan" in animal["characteristics"]:
                animal_data["Lifespan"] = animal["characteristics"]["lifespan"]
        if "locations" in animal:
            animal_data["Location"] = " and ".join(animal["locations"])
        animals_data[animal["name"]] = animal_data
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


def get_possible_skin_types() -> list[str]:
    """ Returns the possible skin types of the animals """
    full_animals_data = load_data("animals_data.json")
    skin_types = set()
    for animal in full_animals_data:
        if "characteristics" in animal and "skin_type" in animal["characteristics"]:
            skin_types.add(animal["characteristics"]["skin_type"])
    return list(skin_types)


def get_user_input() -> str:
    """ Asks the user for the skin type of the animals """
    skin_types = get_possible_skin_types()
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


if __name__ == "__main__":
    new_html = load_html_template("animals_template.html")
    skin_type = get_user_input()
    animals_data = get_animals_data(skin_type)

    html_animals_data = ""
    for animal_name, animal_data in animals_data.items():
        html_animals_data += build_animal_info_html(animal_name, animal_data)

    new_html = new_html.replace("__REPLACE_ANIMALS_INFO__", html_animals_data)
    with open("animals.html", "w") as handle:
        handle.write(new_html)