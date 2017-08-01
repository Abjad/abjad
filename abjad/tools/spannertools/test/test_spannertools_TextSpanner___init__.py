# -*- coding: utf-8 -*-
import abjad


def test_spannertools_TextSpanner___init___01():
    r'''Initialize empty text spanner.
    '''

    spanner = abjad.TextSpanner()
    assert isinstance(spanner, abjad.TextSpanner)
