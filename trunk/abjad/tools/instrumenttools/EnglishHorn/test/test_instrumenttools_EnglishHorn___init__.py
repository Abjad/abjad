from abjad import *


def test_instrumenttools_EnglishHorn___init___01():

    english_horn = instrumenttools.EnglishHorn()

    assert isinstance(english_horn, instrumenttools.EnglishHorn)
