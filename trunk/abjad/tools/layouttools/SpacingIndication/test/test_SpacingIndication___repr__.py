from abjad import *
from abjad.tools.contexttools import TempoMark
from abjad.tools.layouttools import SpacingIndication


def test_SpacingIndication___repr___01():
    '''Repr is evaluable.
    '''

    indication_1 = SpacingIndication(TempoMark(Duration(1, 8), 44), Duration(1, 68))
    indication_2 = SpacingIndication(indication_1)

    assert indication_1 is not indication_2
    assert indication_1 == indication_2
