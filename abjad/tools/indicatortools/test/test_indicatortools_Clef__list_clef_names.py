# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Clef__list_clef_names_01():

    assert 'treble' in Clef._list_clef_names()
