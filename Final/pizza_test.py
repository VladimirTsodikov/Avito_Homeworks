from pizza import Margherita, Pepperoni, Hawaiian
import unittest


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
    
    def test_exception_if_error_size(self):
        self.assertRaises(SyntaxError, Margherita, 'S')
        self.assertRaises(SyntaxError, Pepperoni, 'X')
        self.assertRaises(SyntaxError, Hawaiian, 'xl')

    def test_isinstanse(self):
        actual = Margherita('L').dict()
        self.assertIsInstance(actual, dict)

    def test_equal(self):
        self.assertEqual(Margherita('XL'), Margherita('XL'))
        self.assertEqual(Pepperoni('L'), Pepperoni('L'))

    def test_not_equal(self):
        self.assertNotEqual(Pepperoni('L'), Pepperoni('XL'))
        self.assertNotEqual(Pepperoni('XL'), Hawaiian('XL'))
        self.assertNotEqual(Margherita('XL'), Hawaiian('L'))
