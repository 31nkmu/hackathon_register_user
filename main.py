from mixin import *


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUsernameMixin):
    pass


class Post(CheckOwnerMixin):
    def __init__(self, title: str, description: str, price: int, quantity: int, owner: str) -> None:
        file = open_file()
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
