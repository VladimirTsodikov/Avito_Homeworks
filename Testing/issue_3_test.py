from one_hot_encoder import fit_transform
import unittest


class TestFitTransform(unittest.TestCase):
    def test_cities(self):
        actual = fit_transform(['Moscow', 'New York', 'Moscow', 'London'])
        expected = [
            ('Moscow',   [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow',   [0, 0, 1]),
            ('London',   [1, 0, 0]),
        ]
        self.assertEqual(actual, expected)

    def test_cars(self):
        actual = fit_transform(['Peugeot', 'Niva', 'Ford', 'Lada', 'Niva',
                                'Dodge', 'Dodge', 'Kia', 'Porsche', 'Acura',
                                'Ford', 'BMW', 'Honda', 'Audi', 'Niva',
                                'Volkswagen', 'BMW'])
        expected = [
            ('Peugeot', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
            ('Niva',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            ('Ford',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
            ('Lada',    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
            ('Niva',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            ('Dodge',   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
            ('Dodge',   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
            ('Kia',     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
            ('Porsche', [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
            ('Acura',   [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
            ('Ford',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
            ('BMW',     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
            ('Honda',   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ('Audi',    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ('Niva',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
            ('Volkswagen', [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
            ('BMW',     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
        ]
        self.assertEqual(actual, expected)

    def test_isinstanse(self):
        actual = fit_transform(['str1', 'str2', 'cat', 'dog'])
        self.assertIsInstance(actual, list)

    def test_exception(self):
        # не передали в функцию fit_transform ничего
        self.assertRaises(TypeError, fit_transform)

        # передали в функцию fit_transform int (не iterable)
        self.assertRaises(TypeError, fit_transform, 2)

        # передали в функцию fit_transform список из одной пустой строки - OK
        self.assertEqual(fit_transform(['']), [('', [1])])

    def test_in_or_not_in(self):
        actual = fit_transform(['pen', 'pensil', 'phone', 'pen', 'clock',
                                'bottle', 'pensil', 'rubber', 'book', 'pen'])

        self.assertIn(('pen', [0, 0, 0, 0, 0, 0, 1]), actual)
        self.assertIn(('rubber', [0, 1, 0, 0, 0, 0, 0]), actual)
        self.assertNotIn(('phone', [0, 0, 1, 0, 0, 0, 0]), actual)

        self.assertEqual(actual.count(('pen', [0, 0, 0, 0, 0, 0, 1])), 3)
        self.assertEqual(actual.count(('book', [1, 0, 0, 0, 0, 0, 0])), 1)
