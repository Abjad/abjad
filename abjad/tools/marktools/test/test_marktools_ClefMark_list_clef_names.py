# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_ClefMark_list_clef_names_01():

    assert 'treble' in marktools.ClefMark.list_clef_names()
