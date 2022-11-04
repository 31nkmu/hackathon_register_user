from func import *


class CheckOwnerMixin:
    @staticmethod
    def check(owner: str, file: List[dict]) -> None:
        if not name_in_data(owner, file):
            raise Exception('Нет такого пользователя!')


class RegisterMixin:
    @staticmethod
    def register(name: str, password: str) -> str:
        create_json()
        file = open_file()
        if name_in_data(name, file):
            raise Exception('Такой юзер уже существует!')
        validate_password(password)
        if file:
            id_ = max([dict_['id'] for dict_ in file]) + 1
        else:
            id_ = 0
        file.append({
            'id': id_,
            'name': name,
            'password': password
        })
        write_file(file)
        return 'Successfully registered'


class LoginMixin:
    @staticmethod
    def login(name: str, password: str) -> str:
        file = open_file()
        if not name_in_data(name, file):
            raise Exception('Нет такого юзера в БД!')
        if not true_password(name, password, file):
            raise Exception('Неверный пароль!')
        return 'Вы успешно залогинились!'


class ChangePasswordMixin:
    @staticmethod
    def change_password(name: str, old_password: str, new_password: str) -> str:
        validate_password(new_password)
        file = open_file()
        if not name_in_data(name, file):
            raise Exception('Нет такого юзера в БД!')
        if not true_password(name, old_password, file):
            raise Exception('Старый пароль указан не верно!')
        for dict_ in file:
            if dict_['name'] == name:
                dict_['password'] = new_password
                write_file(file)
                return 'Password changed successfully!'


class ChangeUsernameMixin:
    @staticmethod
    def change_name(old_name, new_name) -> str:
        file = open_file()
        if not name_in_data(old_name, file):
            raise 'Нет такого зарегистрированного юзера в БД!'
        while name_in_data(new_name, file):
            print('Пользователь с таким именем уже существует!')
            new_name = input('Введите другое имя:\n')
        for dict_ in file:
            if dict_['name'] == old_name:
                dict_['name'] = new_name
                write_file(file)
                return 'Username changed successfully!'
