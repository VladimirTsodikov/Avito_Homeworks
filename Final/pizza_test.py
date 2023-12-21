from click.testing import CliRunner
from pizza import Pizza, Margherita, Pepperoni, Hawaiian, WrongPizzaSizeException
from cli import order, menu
import pytest


@pytest.mark.parametrize(
    "source_size, expected_size",
    [
        (Margherita('XL').size, 'XL'),
        (Margherita('L').size, 'L'),
        (Pepperoni('XL').size, 'XL'),
        (Pepperoni('L').size, 'L'),
        (Hawaiian('XL').size, 'XL'),
        (Hawaiian('L').size, 'L'),
    ]
)
def test_pizza_correct_sizes(source_size, expected_size):
    assert source_size == expected_size


def test_pizza_incorrect_size():
    with pytest.raises(WrongPizzaSizeException):
        Margherita('X')
    with pytest.raises(WrongPizzaSizeException):
        Pepperoni('xl')
    with pytest.raises(WrongPizzaSizeException) as excinfo:
        Hawaiian('XLL')
    assert "Данная пицца не может иметь такой размер" in str(excinfo.value)


@pytest.mark.parametrize(
    "source_name, expected_name",
    [
        (Margherita('XL').name, 'Margherita'),
        (Margherita('L').name, 'Margherita'),
        (Pepperoni('XL').name, 'Pepperoni'),
        (Pepperoni('L').name, 'Pepperoni'),
        (Hawaiian('XL').name, 'Hawaiian'),
        (Hawaiian('L').name, 'Hawaiian'),
    ]
)
def test_pizza_correct_names(source_name, expected_name):
    assert source_name == expected_name


def test_pizza_dict_is_dict():
    actual = Margherita('L').dict()
    assert isinstance(actual, dict)


def test_pizza_equal():
    assert Margherita('XL') == Margherita('XL')
    assert Pepperoni('L') == Pepperoni('L')
    assert Hawaiian('XL') == Hawaiian('XL')


def test_pizza_not_equal_1():
    assert Pepperoni('L') != Pepperoni('XL')
    assert Pepperoni('XL') != Hawaiian('XL')
    assert Margherita('XL') != Hawaiian('L')


def test_pizza_not_equal_2():
    assert Pepperoni('L') != 'L'
    assert Margherita('XL') != 42


def test_order_without_delivery():
    runner = CliRunner()
    result = runner.invoke(order, ['Pepperoni'])
    assert result.exit_code == 0
    assert '🔥 Приготовили пиццу Pepperoni в печи за' in result.output
    assert '📦 Доставили пиццу' not in result.output


def test_order_with_delivery():
    runner = CliRunner()
    result = runner.invoke(order, ['Hawaiian', '--delivery'])
    assert result.exit_code == 0
    assert '🔥 Приготовили пиццу Hawaiian в печи за' in result.output
    assert '📦 Доставили пиццу Hawaiian за' in result.output


def test_order_with_error_name_pizza():
    runner = CliRunner()
    result = runner.invoke(order, ['Margherit'])
    assert not result.exception
    assert 'Такой пиццы в данный момент нет в продаже' in result.output


def test_menu():
    runner = CliRunner()
    result = runner.invoke(menu)
    assert result.exit_code == 0
    for subclass in Pizza.__subclasses__():
        assert f'- {subclass.name} {subclass.icon}' in result.output
