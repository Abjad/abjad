# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_AbjadRevisionToken_format_01():

    abjad_version_token = lilypondfiletools.AbjadRevisionToken()
    assert isinstance(abjad_version_token.lilypond_format, str)
