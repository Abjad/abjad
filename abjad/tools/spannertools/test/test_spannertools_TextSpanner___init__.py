# -*- coding: utf-8 -*-
import abjad
from abjad import *


def test_spannertools_TextSpanner___init___01():
    r'''Initialize empty text spanner.
    '''

    spanner = spannertools.TextSpanner()
    assert isinstance(spanner, spannertools.TextSpanner)
