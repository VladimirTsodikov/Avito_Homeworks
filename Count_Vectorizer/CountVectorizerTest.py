import unittest

from Class_CountVectorizer import CountVectorizer


class CountVectorTest(unittest.TestCase):
    v1 = CountVectorizer()
    test_1 = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
    ]
    res_1 = [
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1]
    ]

    def test_fit_transform(self):
        self.assertRaises(TypeError, self.v1.fit_transform, 2)
        self.assertEqual(self.v1.fit_transform(self.test_1), self.res_1)


if __name__ == '__main__':
    unittest.main()
