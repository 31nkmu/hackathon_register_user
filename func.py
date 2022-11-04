import json
from typing import List


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise Exception('Пароль слишком короткий!')
    if password.isalpha() or password.isdigit():
        raise Exception('Пароль должен состоять из букв и цифр!')


def create_json() -> None:
    try:
        with open('user.json', 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass


def open_file() -> List[dict]:
    with open('user.json') as file:
        return json.load(file)


def write_file(data: List[dict]) -> None:
    with open('user.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def name_in_data(name: str, data: List[dict]) -> bool:
    return any(dict_['name'].lower() == name.lower() for dict_ in data)


def true_password(name: str, password: str, data: List[dict]) -> bool:
    for data_one_users in data:
        if data_one_users['name'] == name:
            return data_one_users['password'] == password
