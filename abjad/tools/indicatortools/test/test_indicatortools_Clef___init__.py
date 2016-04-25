# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Clef___init___01():

    clef_1 = Clef('treble')
    clef_2 = Clef(clef_1)

    assert clef_1 == clef_2
    assert not clef_1 is clef_2


def test_indicatortools_Clef___init___02():

    assert pytest.raises(TypeError, 'Clef(1)')
