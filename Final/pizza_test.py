from pizza import Margherita, Pepperoni, Hawaiian
import unittest
from cli import order
import pytest
import re

class TestPizza(unittest.TestCase):
    def test_Margherita_size(self):
        actual = [Margherita('XL').size, Margherita('L').size]
        excepted = ['XL', 'L']
        self.assertEqual(actual, excepted)

    def test_Pepperoni_size(self):
        actual = [Pepperoni('XL').size, Pepperoni('L').size]
        excepted = ['XL', 'L']
        self.assertEqual(actual, excepted)

    def test_Hawaiian_size(self):
        actual = [Hawaiian('XL').size, Hawaiian('L').size]
        excepted = ['XL', 'L']
        self.assertEqual(actual, excepted)

    def test_names(self):
        actual = [Margherita('XL').name, Margherita('L').name,
                  Pepperoni('XL').name, Pepperoni('L').name,
                  Hawaiian('XL').name, Hawaiian('L').name,
                  ]
        excepted = ['Margherita', 'Margherita',
                    'Pepperoni', 'Pepperoni',
                    'Hawaiian', 'Hawaiian',
                    ]
        self.assertEqual(actual, excepted)

    # def test_exception_if_error_size(self):
    #     self.assertRaises(Exception, Margherita, 'S')
    #     self.assertRaises(Exception, Pepperoni, 'X')
    #     self.assertRaises(Exception, Hawaiian, 'xl')

    # def test_exception(self):
    #     with pytest.raises(Exception):
    #         Margherita('X')
        # self.assertRaisesRegex(Exception, "Данная пицца не может иметь такой размер", Margherita, 'S')
    def test_isinstanse(self):
        actual = Margherita('L').dict()
        self.assertIsInstance(actual, dict)

    def test_equal(self):
        self.assertEqual(Margherita('XL'), Margherita('XL'))
        self.assertEqual(Pepperoni('L'), Pepperoni('L'))

    def test_not_equal_1(self):
        self.assertNotEqual(Pepperoni('L'), Pepperoni('XL'))
        self.assertNotEqual(Pepperoni('XL'), Hawaiian('XL'))
        self.assertNotEqual(Margherita('XL'), Hawaiian('L'))

    def test_not_equal_2(self):
        self.assertNotEqual(Pepperoni('L'), 'L')
        self.assertNotEqual(Margherita('XL'), 42)


# class TestOrder(unittest.TestCase):
#     def test_order(self):
#         self.assertRaises(SyntaxError, order('Pepperoni'))

# import pytest

# def test_exception():
#     with pytest.raises(SyntaxError):
#         order('Pepperni', False)