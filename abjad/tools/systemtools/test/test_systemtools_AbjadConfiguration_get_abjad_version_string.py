# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_get_abjad_version_string_01():
    assert isinstance(
        systemtools.AbjadConfiguration.get_abjad_version_string(),
        str,
        )
