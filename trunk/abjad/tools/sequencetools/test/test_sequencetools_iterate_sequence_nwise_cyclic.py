from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_nwise_cyclic_01():

    g = sequencetools.iterate_sequence_nwise_cyclic(range(6), 3)

    assert g.next() == (0, 1, 2)
    assert g.next() == (1, 2, 3)
    assert g.next() == (2, 3, 4)
    assert g.next() == (3, 4, 5)
    assert g.next() == (4, 5, 0)
    assert g.next() == (5, 0, 1)
    assert g.next() == (0, 1, 2)
    assert g.next() == (1, 2, 3)
    assert g.next() == (2, 3, 4)
    assert g.next() == (3, 4, 5)
