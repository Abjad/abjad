# -*- encoding: utf-8 -*-
from abjad import *


def test_TextScriptSpanner___init___01():
    r'''Init empty text script spanner.
    '''

    spanner = spannertools.TextScriptSpanner()
    assert isinstance(spanner, spannertools.TextScriptSpanner)
