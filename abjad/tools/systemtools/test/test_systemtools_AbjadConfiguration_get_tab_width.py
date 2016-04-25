# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_AbjadConfiguration_get_tab_width_01():
    assert systemtools.AbjadConfiguration.get_tab_width() == 4
