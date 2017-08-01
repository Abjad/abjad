# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_get_tab_width_01():
    assert systemtools.AbjadConfiguration.get_tab_width() == 4
