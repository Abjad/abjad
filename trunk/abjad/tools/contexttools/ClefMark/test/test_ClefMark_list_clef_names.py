# -*- encoding: utf-8 -*-
from abjad import *


def test_ClefMark_list_clef_names_01():

    assert 'treble' in contexttools.ClefMark.list_clef_names()
