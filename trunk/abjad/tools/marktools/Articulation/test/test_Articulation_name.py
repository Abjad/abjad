from abjad import *


def test_Articulation_name_01():

    a = marktools.Articulation('staccato')
    assert a.name == 'staccato'

    a.name = 'marcato'

    assert a.name == 'marcato'
