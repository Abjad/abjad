# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_AbjadConfiguration_get_abjad_version_string_01():
    assert isinstance(
        systemtools.AbjadConfiguration.get_abjad_version_string(),
        str,
        )
