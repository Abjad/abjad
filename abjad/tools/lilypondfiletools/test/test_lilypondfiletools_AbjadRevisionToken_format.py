# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_AbjadRevisionToken_format_01():

    abjad_version_token = lilypondfiletools.AbjadRevisionToken()
    assert isinstance(format(abjad_version_token), str)
