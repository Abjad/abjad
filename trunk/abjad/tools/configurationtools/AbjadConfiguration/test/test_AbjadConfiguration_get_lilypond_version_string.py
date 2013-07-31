# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import configurationtools


def test_AbjadConfiguration_get_lilypond_version_string_01():
    lilypond_version_string = \
        configurationtools.AbjadConfiguration.get_lilypond_version_string()
    assert isinstance(lilypond_version_string, str)
    assert lilypond_version_string.count('.') == 2
