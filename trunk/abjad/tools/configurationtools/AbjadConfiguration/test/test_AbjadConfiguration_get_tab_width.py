# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_AbjadConfiguration_get_tab_width_01():
    assert configurationtools.AbjadConfiguration.get_tab_width() == 4
