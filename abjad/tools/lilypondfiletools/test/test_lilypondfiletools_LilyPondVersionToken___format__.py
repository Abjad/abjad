# -*- coding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_LilyPondVersionToken___format___01():

    lilypond_version_token = lilypondfiletools.LilyPondVersionToken()
    assert isinstance(format(lilypond_version_token), str)
    assert format(lilypond_version_token).count('.') == 2
