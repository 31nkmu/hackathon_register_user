import json
from typing import List


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise Exception('Пароль слишком короткий!')
    if password.isalpha() or password.isdigit():
        raise Exception('Пароль должен состоять из букв и цифр!')


class FileManipulationMixin:
    @staticmethod
    def _create_json() -> None:
        try:
            with open('user.json', 'x') as file:
                json.dump([], file)
        except FileExistsError:
            pass

    @staticmethod
    def _open_file() -> List[dict]:
        with open('user.json') as file:
            return json.load(file)

    @staticmethod
    def _write_file(data: List[dict]) -> None:
        with open('user.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class ValidateUserMixin:
    @staticmethod
    def _name_in_data(name: str, data: List[dict]) -> [True or False]:
        return any(dict_['name'].lower() == name.lower() for dict_ in data)

    @staticmethod
    def _true_password(name: str, password: str, file: List[dict]) -> [True or False]:
        data_one_users = [dict_ for dict_ in file if dict_['name'] == name][0]
        return data_one_users['password'] == password


class CheckOwnerMixin(ValidateUserMixin):
    def check(self, owner: str, file: List[dict]):
        if not self._name_in_data(owner, file):
            raise Exception('Нет такого пользователя!')


class RegisterMixin(FileManipulationMixin, ValidateUserMixin):
    def register(self, name: str, password: str) -> str:
        self._create_json()
        file = self._open_file()
        if self._name_in_data(name, file):
            raise Exception('Такой юзер уже существует!')
        validate_password(password)
        if file:
            id_ = max([dict_['id'] for dict_ in file]) + 1
        else:
            id_ = 1
        file.append({
            'id': id_,
            'name': name,
            'password': password
        })
        self._write_file(file)
        return 'Successfully registered'


class LoginMixin(FileManipulationMixin, ValidateUserMixin):
    def login(self, name: str, password: str) -> str:
        file = self._open_file()
        if not self._name_in_data(name, file):
            raise Exception('Нет такого юзера в БД!')
        if not self._true_password(name, password, file):
            raise Exception('Неверный пароль!')
        return 'Вы успешно залогинились!'


class ChangePasswordMixin(FileManipulationMixin, ValidateUserMixin):
    def change_password(self, name: str, old_password: str, new_password: str) -> str:
        validate_password(new_password)
        file = self._open_file()
        if not self._name_in_data(name, file):
            raise Exception('Нет такого юзера в БД!')
        if not self._true_password(name, old_password, file):
            raise Exception('Старый пароль указан не верно!')
        for dict_ in file:
            if dict_['name'] == name:
                dict_['password'] = new_password
        self._write_file(file)
        return 'Password changed successfully!'


class ChangeUsernameMixin(FileManipulationMixin, ValidateUserMixin):
    def change_name(self, old_name, new_name):
        file = self._open_file()
        if not self._name_in_data(old_name, file):
            raise 'Нет такого зарегистрированного юзера в БД!'
        while self._name_in_data(new_name, file):
            print('Пользователь с таким именем уже существует!')
            new_name = input('Введите другое имя:\n')
        for dict_ in file:
            if dict_['name'] == old_name:
                dict_['name'] = new_name
        self._write_file(file)
        return 'Username changed successfully!'


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUsernameMixin):
    pass


class Post(CheckOwnerMixin, FileManipulationMixin):
    def __init__(self, title: str, description: str, price: int, quantity: int, owner: str) -> None:
        file = self._open_file()
        self.check(owner, file)
        self.title = title
        self.description = description
        self.price = price
        self.quantity = quantity
        self.owner = owner

    def __str__(self):
        return f'owner: {self.owner}\n' \
               f'title: {self.title}\n' \
               f'description: {self.description}\n' \
               f'price: {self.price}\n' \
               f'quantity: {self.quantity}'
