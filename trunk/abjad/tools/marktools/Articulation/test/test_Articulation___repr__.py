from abjad import *
from abjad.tools.marktools import Articulation


def test_Articulation___repr___01():
    '''Repr of unattached articulation is evaluable.
    '''

    articulation_1 = marktools.Articulation('staccato')
    articulation_2 = eval(repr(articulation_1))

    assert isinstance(articulation_1, marktools.Articulation)
    assert isinstance(articulation_2, marktools.Articulation)
    assert articulation_1 == articulation_2
