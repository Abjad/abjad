from abjad import *


def test_AbjadRevisionToken_format_01():

    abjad_version_token = lilyfiletools.AbjadRevisionToken()
    assert isinstance(abjad_version_token.format, str)
