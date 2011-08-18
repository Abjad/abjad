from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.quantizationtools import QGridSearchTree


def test_quantizationtools_QGridSearchTree_prune_01():

    beatspan = Fraction(1, 4)
    tempo = TempoMark((1, 4), 60)
    qst = QGridSearchTree({2: {2: {2: {2: {2: {2: None}}}}}})

    assert qst.prune(beatspan, tempo, 10) == {2: {2: {2: {2: {2: {2: None}}}}}}
    assert qst.prune(beatspan, tempo, 20) == {2: {2: {2: {2: {2: None}}}}}
    assert qst.prune(beatspan, tempo, 40) == {2: {2: {2: {2: None}}}}
    assert qst.prune(beatspan, tempo, 80) == {2: {2: {2: None}}}
    assert qst.prune(beatspan, tempo, 160) == {2: {2: None}}
    assert qst.prune(beatspan, tempo, 320) == {2: None}
    assert qst.prune(beatspan, tempo, 10000) is None
