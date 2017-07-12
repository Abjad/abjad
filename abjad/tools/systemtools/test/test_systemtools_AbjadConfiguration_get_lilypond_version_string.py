# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_AbjadConfiguration_get_lilypond_version_string_01():
    lilypond_version_string = \
        systemtools.AbjadConfiguration.get_lilypond_version_string()
    assert isinstance(lilypond_version_string, str)
    assert lilypond_version_string.count('.') == 2
