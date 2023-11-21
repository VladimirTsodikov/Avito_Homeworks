import click
from random import randint
from pizza import *


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza')
def order(pizza: str, delivery: bool):
    """Готовит и доставляет пиццу"""
    if pizza.lower() not in [subclass.__name__.lower()
                             for subclass in Pizza.__subclasses__()]:
        raise SyntaxError('Такой пиццы в данный момент нет в продаже')
    print(f'🔥 Приготовили пиццу {pizza} в печи за {randint(10, 25)} мин!')
    if (delivery):
        print(f'📦 Доставили пиццу {pizza} за {randint(20, 60)} мин!')


@cli.command()
def menu():
    """Выводит меню"""
    for subclass in Pizza.__subclasses__():
        print(f'- {subclass.__name__} {subclass.icon()} : доступные размеры: ', end='')
        for size in subclass.var_sizes():
            print(f'{size}', end=' ')
        print()
        for size in subclass.var_sizes():
            print(f'\tРазмер {size}. Состав: ')
            for key, value in subclass(size=size).dict().items():
                print(f'\t{key} -- {value} грамм')
            print()
        print()


if __name__ == '__main__':
    cli()
