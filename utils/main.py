import json


def read_json(file_path) -> dict:
    with open(file_path, mode="r", encoding="utf-8") as file:
        content = json.load(file)
        return content


def get_photo(directory, name):
    with open(f"media/{directory}/{name}", mode="rb") as file:
        return file.read()


def combine_fields(table_fields, list_of_fields):
    return dict(zip(table_fields, list_of_fields))
