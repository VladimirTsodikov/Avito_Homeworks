from one_hot_encoder import fit_transform
import pytest


@pytest.mark.parametrize(
    "source_corpus, result",
    [
        (fit_transform(['Moscow', 'New York', 'Moscow', 'London']),
         [
            ('Moscow',   [0, 0, 1]),
            ('New York', [0, 1, 0]),
            ('Moscow',   [0, 0, 1]),
            ('London',   [1, 0, 0]),
        ]),

        (fit_transform(['', 'mentor', 'teacher', '', 'teacher']),
         [
             ('',        [0, 0, 1]),
             ('mentor',  [0, 1, 0]),
             ('teacher', [1, 0, 0]),
             ('',        [0, 0, 1]),
             ('teacher', [1, 0, 0]),
        ]),

        (fit_transform(['one']),
         [
             ('one', [1]),
        ]),
    ]
)
def test_correct_fit_transform(source_corpus, result):
    assert (source_corpus) == result


def test_phones():
    actual = fit_transform(['Samsung', 'Xiaomi', 'Meizu', 'iPhone',
                            'Poco', 'Lenovo', 'Poco', 'IPhone', 'Xiaomi',
                            'HTC', 'Nokia', 'Sumsang', 'Huawei', 'Poco',
                            'OPPO', 'Oppo', 'Vivo', 'HTC', 'ZTE', 'HTc'])
    expected = [
        ('Samsung', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
        ('Xiaomi',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
        ('Meizu',   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
        ('iPhone',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
        ('Poco',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
        ('Lenovo',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
        ('Poco',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
        ('IPhone',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
        ('Xiaomi',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
        ('HTC',     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
        ('Nokia',   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('Sumsang', [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('Huawei',  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('Poco',    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
        ('OPPO',    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('Oppo',    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('Vivo',    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('HTC',     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
        ('ZTE',     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ('HTc',     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    ]
    assert actual == expected


def test_empty_params():
    with pytest.raises(TypeError):
        fit_transform()


def test_not_iterable_params():
    with pytest.raises(TypeError):
        fit_transform(42)
