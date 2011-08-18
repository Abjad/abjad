from abjad import *
from abjad.tools import seqtools


def test_seqtools_increase_sequence_elements_at_indices_by_addenda_01():
    '''Increase elements of list l by the elements of addenda
        at indices in l.'''

    l = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    t = seqtools.increase_sequence_elements_at_indices_by_addenda(l, [0.5, 0.5], [0, 4, 8])
    assert t == [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]
