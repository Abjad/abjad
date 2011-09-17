from abjad import *


def test_LilyPondVersionToken_format_01():

    lilypond_version_token = lilypondfiletools.LilyPondVersionToken()
    assert isinstance(lilypond_version_token.format, str)
    assert lilypond_version_token.format.count('.') == 2
