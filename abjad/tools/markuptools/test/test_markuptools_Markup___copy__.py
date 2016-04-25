# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_markuptools_Markup___copy___01():
    r'''Copy keywords.
    '''

    markup_1 = markuptools.Markup('foo bar', direction=Up)
    markup_2 = copy.copy(markup_1)

    assert markup_1 == markup_2
    assert repr(markup_1) == repr(markup_2)
    assert format(markup_1) == format(markup_2)
