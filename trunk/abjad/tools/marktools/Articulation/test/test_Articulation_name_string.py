from abjad import *


def test_Articulation_name_string_01():

    a = marktools.Articulation('staccato')
    assert a.name_string == 'staccato'

    a.name_string = 'marcato'

    assert a.name_string == 'marcato'

