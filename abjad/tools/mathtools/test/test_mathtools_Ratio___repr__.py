# -*- coding: utf-8 -*-
from abjad.tools.mathtools.Ratio import Ratio


def test_mathtools_Ratio___repr___01():
    r'''Repr is evaluable.
    '''

    ratio_1 = Ratio((1, 2, -1))
    ratio_2 = eval(repr(ratio_1))

    assert isinstance(ratio_1, Ratio)
    assert isinstance(ratio_2, Ratio)
    assert ratio_1 is not ratio_2
    assert ratio_1 == ratio_2
