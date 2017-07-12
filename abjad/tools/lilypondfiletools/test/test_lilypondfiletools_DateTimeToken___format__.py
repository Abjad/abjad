# -*- coding: utf-8 -*-
import abjad


def test_lilypondfiletools_DateTimeToken___format___01():

    date_time_token = abjad.DateTimeToken()
    assert isinstance(date_time_token._get_lilypond_format(), str)
    assert len(date_time_token._get_lilypond_format()) == 16
