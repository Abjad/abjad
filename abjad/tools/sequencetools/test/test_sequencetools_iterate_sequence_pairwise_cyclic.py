# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_pairwise_cyclic_01(): 

    t = range(6)
    pairs = sequencetools.iterate_sequence_pairwise_cyclic(t)
    for x in range(100):
        assert pairs.next()
