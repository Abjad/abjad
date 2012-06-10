from abjad.tools.mathtools.Ratio import Ratio
from experimental.specificationtools.PartIndicator import PartIndicator


def test_PartIndicator___repr___01():
    '''Repr is evaluable.
    '''

    part_indicator_1 = PartIndicator((1, 2, 1), 0)
    part_indicator_2 = eval(repr(part_indicator_1))

    assert isinstance(part_indicator_1, PartIndicator)
    assert isinstance(part_indicator_2, PartIndicator)
    assert not part_indicator_1 is part_indicator_2
    assert part_indicator_1 == part_indicator_2
