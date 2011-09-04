import py.test
from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durationtools import Offset
from abjad.tools.quantizationtools import QGridSearchTree
from abjad.tools.quantizationtools import QGridTempoLookup
from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds


def test_quantizationtools_QGridTempoLookup___init___01():
    '''Requires three arguments.'''
    offsets = [Offset(0), Offset((1, 2)), Offset(1)]
    beatspan = Fraction(1, 4)
    tempo = TempoMark((1, 4), 60)
    qtl = QGridTempoLookup(offsets, beatspan, tempo)

    assert len(qtl) == len(offsets)
    for offset in offsets:
        assert offset in qtl
        assert qtl[offset] == tempo_scaled_rational_to_milliseconds(offset * beatspan, tempo)


def test_quantizationtools_QGridTempoLookup___init___02():
    '''Offset list may be a QGridSearchTree instead.'''
    search_tree = QGridSearchTree({2: {2: None, 3: None}})
    beatspan = Fraction(1, 4)
    tempo = TempoMark((1, 4), 60)
    qtl = QGridTempoLookup(search_tree, beatspan, tempo)

    assert len(qtl) == len(search_tree.offsets)
    for offset in search_tree.offsets:
        assert offset in qtl
        assert qtl[offset] == tempo_scaled_rational_to_milliseconds(offset * beatspan, tempo)
