from morse import decode
import pytest


@pytest.mark.parametrize(
    "source_string, result",
    [
        ('.--. .. -....- ...-- .-.-.- .---- ....- .---- ..... .-.-.- .-.-.- '
         '.-.-.-', 'PI-3.1415...'),
        ('-.. . ...- . .-.. --- .--. . .-.', 'DEVELOPER'),
        ('... . .-.. ..-. -....- . -.. ..- -.-. .- - .. --- -.',
         'SELF-EDUCATION'),
        ('.-.. .. - . .-. .- - ..- .-. .', 'LITERATURE'),
    ]
)
def test_decode(source_string, result):
    assert decode(source_string) == result
