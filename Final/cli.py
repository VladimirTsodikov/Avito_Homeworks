import click
# from random import randint
from pizza import Pizza, bake, pizza_delivery


class WrongPizzaNameException(ValueError):
    """Вызывается, когда нет такого названия пиццы,
    которую хочет заказать пользователь"""


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza')
def order(pizza: str, delivery: bool):
    """Готовит и доставляет пиццу"""
    try:
        if pizza.lower() not in [subclass.name.lower()
                                 for subclass in Pizza.__subclasses__()]:
            raise WrongPizzaNameException
        bake(pizza)
        # print(f'🔥 Приготовили пиццу {pizza} в печи за {randint(10, 25)} мин!')
        if (delivery):
            pizza_delivery(pizza)
            # print(f'📦 Доставили пиццу {pizza} за {randint(20, 60)} мин!')
    except WrongPizzaNameException:
        print('Такой пиццы в данный момент нет в продаже')


@cli.command()
def menu():
    """Выводит меню"""
    for subclass in Pizza.__subclasses__():
        print(f'- {subclass.name} {subclass.icon} : доступные размеры: ', end='')
        for size in subclass.recipes:
            print(f'{size}', end=' ')
        print()
        for size in subclass.recipes:
            print(f'\tРазмер {size}. Состав: ')
            for key, value in subclass.recipes[size].items():
                print(f'\t{key} -- {value} грамм')
            print()
        print()


if __name__ == '__main__':  # pragma: no cover
    cli()
