import copy
from abjad import *
from experimental.tools import *


def test_OffsetExpression___copy___01():

    offset_1 = timeexpressiontools.OffsetExpression(edge=Right, multiplier=Multiplier(1, 3))
    offset_2 = copy.deepcopy(offset_1)

    assert isinstance(offset_1, timeexpressiontools.OffsetExpression)
    assert isinstance(offset_2, timeexpressiontools.OffsetExpression)
    assert not offset_1 is offset_2
    assert offset_1 == offset_2
