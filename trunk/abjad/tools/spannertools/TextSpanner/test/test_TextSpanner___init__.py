# -*- encoding: utf-8 -*-
from abjad import *


def test_TextSpanner___init___01():
    r'''Init empty text spanner.
    '''

    spanner = spannertools.TextSpanner()
    assert isinstance(spanner, spannertools.TextSpanner)
