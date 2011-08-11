from abjad import *
from abjad.tools import seqtools


def test_seqtools_retain_sequence_elements_at_indices_01( ):

    t = seqtools.retain_sequence_elements_at_indices(range(20), [1, 16, 17, 18])
    assert t == [1, 16, 17, 18]


def test_seqtools_retain_sequence_elements_at_indices_02( ):

    t = seqtools.retain_sequence_elements_at_indices(range(20), [ ])
    assert t == [ ]


def test_seqtools_retain_sequence_elements_at_indices_03( ):

    t = seqtools.retain_sequence_elements_at_indices(range(20), [99, 100, 101])
    assert t == [ ]
