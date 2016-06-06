# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_make_repeated_notes_with_shorter_notes_at_end_01():
    r'''Makes repeated 1/16th notes equal to 1/4 total duration.
    '''

    voice = Voice(scoretools.make_repeated_notes_with_shorter_notes_at_end(
        0, Duration(1, 16), Duration(1, 4)))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'16
            c'16
            c'16
            c'16
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_make_repeated_notes_with_shorter_notes_at_end_02():
    r'''Makes repeated 1/16th notes equal to 9/32 total duration.
    '''

    voice = Voice(scoretools.make_repeated_notes_with_shorter_notes_at_end(
        0, Duration(1, 16), Duration(9, 32)))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'32
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_make_repeated_notes_with_shorter_notes_at_end_03():
    r'''Makes repeated 1/16th notes equal to only 1/128 total duration.
    '''

    voice = Voice(scoretools.make_repeated_notes_with_shorter_notes_at_end(
        0, Duration(1, 16), Duration(1, 128)))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'128
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_make_repeated_notes_with_shorter_notes_at_end_04():
    r'''Makes repeated 1/16th notes equal to 4/10 total duration.
    '''

    voice = Voice(scoretools.make_repeated_notes_with_shorter_notes_at_end(
        0, Duration(1, 16), Duration(4, 10)))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'32
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_make_repeated_notes_with_shorter_notes_at_end_05():
    r'''Makes repeated written 1/16th notes within measure of 5/18.
    '''

    measure = Measure(
        (5, 18),
        scoretools.make_repeated_notes_with_shorter_notes_at_end(
            0,
            Duration(1, 16),
            Duration(5, 18),
            prolation=Duration(16, 18)),
        implicit_scaling=True,
        )

    assert format(measure) == stringtools.normalize(
        r'''
        {
            \time 5/18
            \scaleDurations #'(8 . 9) {
                c'16
                c'16
                c'16
                c'16
                c'16
            }
        }
        '''
        )

    assert inspect_(measure).is_well_formed()
