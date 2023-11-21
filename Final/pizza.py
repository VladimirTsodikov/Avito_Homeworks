from random import randint


class Pizza:
    def __init__(self, name: str, size: str):
        self.name = name  # название пиццы
        self.size = size  # выбранный размер пиццы
        self.recipe = {}  # ингридиенты и вес в граммах

    def dict(self) -> dict:
        return self.recipe

    def __eq__(self, __other: object) -> bool:
        if self.name != __other.name:
            return False
        if self.size != __other.size:
            return False
        return True


class Margherita(Pizza):
    @staticmethod
    def var_sizes():
        """Возвращает доступные для заказа размеры этой пиццы"""
        return {'L', 'XL'}

    @staticmethod
    def icon():
        return '🍅'

    def __init__(self, size: str):
        if size not in Margherita.var_sizes():
            raise SyntaxError('Данная пицца не может иметь такой размер')
        super().__init__("Margherita", size)

        match self.size:
            case 'L':
                self.recipe = {
                    'tomato sauce': 50,
                    'mozzarella': 150,
                    'tomatoes': 250,
                }
            case 'XL':
                self.recipe = {
                    'tomato sauce': 70,
                    'mozzarella': 200,
                    'tomatoes': 350,
                }
            # если добавятся другие размеры для этой пиццы - добавить 'case'


class Pepperoni(Pizza):
    @staticmethod
    def var_sizes():
        """Возвращает доступные для заказа размеры этой пиццы"""
        return {'L', 'XL'}

    @staticmethod
    def icon():
        return '🍕'

    def __init__(self, size: str):
        if size not in Pepperoni.var_sizes():
            raise SyntaxError('Данная пицца не может иметь такой размер')
        super().__init__("Pepperoni", size)

        match self.size:
            case 'L':
                self.recipe = {
                    'tomato sauce': 65,
                    'mozzarella': 120,
                    'pepperoni': 260,
                }
            case 'XL':
                self.recipe = {
                    'tomato sauce': 85,
                    'mozzarella': 180,
                    'pepperoni': 350,
                }
            # если добавятся другие размеры для этой пиццы - добавить 'case'


class Hawaiian(Pizza):
    @staticmethod
    def var_sizes():
        """Возвращает доступные для заказа размеры этой пиццы"""
        return {'L', 'XL'}

    @staticmethod
    def icon():
        return '🍍'

    def __init__(self, size: str):
        if size not in Hawaiian.var_sizes():
            raise SyntaxError('Данная пицца не может иметь такой размер')
        super().__init__("Hawaiian", size)

        match self.size:
            case 'L':
                self.recipe = {
                    'tomato sauce': 40,
                    'mozzarella': 110,
                    'chicken': 250,
                    'pineapples': 80
                }
            case 'XL':
                self.recipe = {
                    'tomato sauce': 65,
                    'mozzarella': 160,
                    'chicken': 340,
                    'pineapples': 115
                }
            # если добавятся другие размеры для этой пиццы - добавить 'case'


def log(function_to_decorate):
    def time_bake(pizza: Pizza):
        print(function_to_decorate.__name__, end=' ')
        function_to_decorate(pizza)
    return time_bake


@log
def bake(pizza: Pizza):
    print(f'- {randint(7, 14)} мин!')


if __name__ == '__main__':
    bake(Margherita('L'))
