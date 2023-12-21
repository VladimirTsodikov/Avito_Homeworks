from random import randint
from typing import Callable


class WrongPizzaSizeException(ValueError):
    """Вызывается, когда у пиццы нет такого варианта размера,
    который ввёл пользователь"""


class Pizza:
    name = ''  # название пиццы
    icon = ''  # иконка пиццы
    # Словарь рецептов. Ключи - доступные для заказа размеры пиццы,
    # значения - словари, состоящие из ингридинтов и веса в граммах
    recipes = {}

    def __init__(self, size: str):
        if size not in self.recipes:  # проверка доступности выбора такого размера
            raise WrongPizzaSizeException('Данная пицца не может иметь такой размер')
        self.size = size  # выбранный размер пиццы
        self.recipe = self.recipes[size]  # ингридиенты и вес в граммах

    def dict(self) -> dict:
        if hasattr(self, 'recipe'):
            return self.recipe

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pizza):
            return NotImplemented
        if self.name != other.name:
            return False
        if self.size != other.size:
            return False
        return True


class Margherita(Pizza):
    name = 'Margherita'
    icon = '🍅'
    recipes = {
        'L': {'tomato sauce': 50, 'mozzarella': 150, 'tomatoes': 250, },
        'XL': {'tomato sauce': 70, 'mozzarella': 200, 'tomatoes': 350, },
    }
    # не нужно: автоматически сработает __init__ базового класса Pizza
    # def __init__(self, size: str):
    #     super().__init__(size)


class Pepperoni(Pizza):
    name = 'Pepperoni'
    icon = '🍕'
    recipes = {
        'L': {'tomato sauce': 65, 'mozzarella': 120, 'pepperoni': 260, },
        'XL': {'tomato sauce': 85, 'mozzarella': 180, 'pepperoni': 350, },
    }


class Hawaiian(Pizza):
    name = 'Hawaiian'
    icon = '🍍'
    recipes = {
        'L': {'tomato sauce': 40, 'mozzarella': 110,
              'chicken': 250, 'pineapples': 80, },
        'XL': {'tomato sauce': 65, 'mozzarella': 160,
               'chicken': 340, 'pineapples': 115, },
    }


def log(func: Callable) -> Callable:
    def time(pizza: Pizza, min_time: int, max_time: int):  # обычно называют wrapper
        func(pizza)
        print(f'{randint(min_time, max_time)} мин!\n')
    return time


@log
def bake(pizza: Pizza):
    print(f'🔥 Приготовили пиццу {pizza} в печи за', end=' ')


@log
def pizza_delivery(pizza: Pizza):
    print(f'📦 Доставили пиццу {pizza} за', end=' ')


if __name__ == '__main__':  # pragma: no cover
    # bake(Margherita('X'))
    mar = Margherita('X')
    print(mar.dict())
