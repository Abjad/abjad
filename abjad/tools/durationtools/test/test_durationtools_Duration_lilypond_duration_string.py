# -*- coding: utf-8 -*-
from abjad import *


def test_durationtools_Duration_lilypond_duration_string_01():

    assert Duration((1, 16)).lilypond_duration_string == '16'
    assert Duration((2, 16)).lilypond_duration_string == '8'
    assert Duration((3, 16)).lilypond_duration_string == '8.'
    assert Duration((4, 16)).lilypond_duration_string == '4'
