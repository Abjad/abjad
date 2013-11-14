# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_TextScriptSpanner___init___01():
    r'''Initializeempty text script spanner.
    '''

    spanner = spannertools.TextScriptSpanner()
    assert isinstance(spanner, spannertools.TextScriptSpanner)
