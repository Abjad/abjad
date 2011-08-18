from abjad import *


def test_instrumenttools_FrenchHorn___init___01():

    french_horn = instrumenttools.FrenchHorn()

    assert isinstance(french_horn, instrumenttools.FrenchHorn)
