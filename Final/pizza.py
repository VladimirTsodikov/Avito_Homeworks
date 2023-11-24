from random import randint


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
        try:
            if size not in self.recipes:  # проверка доступности выбора такого размера
                raise WrongPizzaSizeException
            self.size = size  # выбранный размер пиццы
            self.recipe = self.recipes[size]  # ингридиенты и вес в граммах
        except WrongPizzaSizeException:
            print('Данная пицца не может иметь такой размер')

    def dict(self) -> dict:
        if self.recipe:
            return self.recipe

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pizza):
            return False
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

    def __init__(self, size: str):
        super().__init__(size)


class Pepperoni(Pizza):
    name = 'Pepperoni'
    icon = '🍕'
    recipes = {
        'L': {'tomato sauce': 65, 'mozzarella': 120, 'pepperoni': 260, },
        'XL': {'tomato sauce': 85, 'mozzarella': 180, 'pepperoni': 350, },
    }

    def __init__(self, size: str):
        super().__init__(size)


class Hawaiian(Pizza):
    name = 'Hawaiian'
    icon = '🍍'
    recipes = {
        'L': {'tomato sauce': 40, 'mozzarella': 110,
              'chicken': 250, 'pineapples': 80, },
        'XL': {'tomato sauce': 65, 'mozzarella': 160,
               'chicken': 340, 'pineapples': 115, },
    }

    def __init__(self, size: str):
        super().__init__(size)


def log(function_to_decorate):
    def time_bake(pizza: Pizza):
        print(function_to_decorate.__name__, end=' ')
        function_to_decorate(pizza)
    return time_bake


@log
def bake(pizza: Pizza):
    print(f'- {randint(7, 14)} мин!')


if __name__ == '__main__':
    # bake(Margherita('X'))
    mar = Margherita('X')
    print(2+4)
