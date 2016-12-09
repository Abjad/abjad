# -*- coding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_DateTimeToken___format___01():

    date_time_token = lilypondfiletools.DateTimeToken()
    assert isinstance(date_time_token._get_lilypond_format(), str)
    assert len(date_time_token._get_lilypond_format()) == 16
