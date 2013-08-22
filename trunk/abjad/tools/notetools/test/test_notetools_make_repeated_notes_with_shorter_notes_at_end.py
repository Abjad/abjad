# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_01():
    r'''Make train of 1/16th notes equal to 1/4 total duration.
    '''

    voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(1, 4)))

    r'''
    \new Voice {
        c'16
        c'16
        c'16
        c'16
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'16
            c'16
            c'16
            c'16
        }
        '''
        )


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_02():
    r'''Make train of 1/16th notes equal to 9/32 total duration.
    '''

    voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(9, 32)))

    r'''
    \new Voice {
        c'16
        c'16
        c'16
        c'16
        c'32
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_03():
    r'''Make train of 1/16th notes equal to only 1/128 total duration.
    '''

    voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(1, 128)))

    r'''
    \new Voice {
        c'128
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'128
        }
        '''
        )


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_04():
    r'''Make train of 1/16th notes equal to 4/10 total duration.
    '''

    voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(4, 10)))

    r'''
    \new Voice {
        c'16
        c'16
        c'16
        c'16
        c'16
        c'16
        \times 4/5 {
            c'32
        }
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            \times 4/5 {
                c'32
            }
        }
        '''
        )


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_05():
    r'''Make train of written 1/16th notes within measure of 5/18.
    '''

    measure = Measure((5, 18), notetools.make_repeated_notes_with_shorter_notes_at_end(
        0, Duration(1, 16), Duration(5, 18), prolation = Duration(16, 18)))

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

    assert inspect(measure).is_well_formed()
    assert testtools.compare(
        measure,
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
