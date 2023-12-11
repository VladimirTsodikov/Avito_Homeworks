from unittest.mock import patch
from what_is_year_now import what_is_year_now
import pytest


@pytest.fixture
def year_now():
    return what_is_year_now()


def test_year_today(year_now):
    import datetime  # для получения значения текущего года встроенным способом
    current_year = datetime.datetime.now().year  # Получаем текущий год
    assert year_now == current_year


def test_get_year_2021_YYYY_MM_DD():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '2021-11-11T15:29Z'}
        assert what_is_year_now() == 2021
        mock_get_year.assert_called_once()


def test_get_year_1915_YYYY_MM_DD():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '1915-01-17T11:07Z'}
        assert what_is_year_now() == 1915
        mock_get_year.assert_called_once()


def test_get_year_1874_DD_MM_YYYY():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '11.07.1874T05:19Z'}
        assert what_is_year_now() == 1874
        mock_get_year.assert_called_once()


def test_get_year_3576_DD_MM_YYYY():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '19.12.3576T15:29Z'}
        assert what_is_year_now() == 3576
        mock_get_year.assert_called_once()


def test_get_exception_1():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '19-12-3576T15:29Z'}
        with pytest.raises(ValueError):
            what_is_year_now()


def test_get_exception_2():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '2023.08.14T15:29Z'}
        with pytest.raises(ValueError):
            what_is_year_now()


def test_get_exception_3():
    with patch("what_is_year_now.json.load") as mock_get_year:
        mock_get_year.return_value = {'currentDateTime': '20211111T15:29Z'}
        with pytest.raises(ValueError):
            what_is_year_now()
