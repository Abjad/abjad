# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_01():
    r'''Pitches can be a list of any length greater than 1.
    '''

    duration = notetools.make_accelerating_notes_with_lilypond_multipliers(
        [1], Duration(2), Duration(1, 2), Duration(1, 2))
    assert len(duration) == 4
    for n in duration:
        assert n.written_pitch.numbered_pitch._pitch_number == 1


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_02():
    r'''Pitches can be a list of any length greater than 1.
    '''

    duration = notetools.make_accelerating_notes_with_lilypond_multipliers(
        [1, 2], Duration(2), Duration(1, 2), Duration(1, 2))
    assert len(duration) == 4
    for i, n in enumerate(duration):
        if i % 2 == 0:
            assert n.written_pitch.numbered_pitch._pitch_number == 1
        else:
            assert n.written_pitch.numbered_pitch._pitch_number == 2


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_03():
    r'''Start and stop fractions must be smaller than durations.
    '''
    code = 't = notetools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Duration(2), Duration(4), Duration(1, 2))'
    assert py.test.raises(ValueError, code)


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_04():
    '''
    The default written duration of notes returned is 1/8.
    '''
    duration = notetools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Duration(2), Duration(1, 2), Duration(1, 2))
    for n in duration:
        assert n.written_duration == Duration(1, 8)


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_05():
    '''
    The written duration can be set.
    '''
    duration = notetools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Duration(2), Duration(1, 2), Duration(1, 2),
    written=Duration(1))
    for n in duration:
        assert n.written_duration == Duration(1)


def test_notetools_make_accelerating_notes_with_lilypond_multipliers_06():
    '''
    note_curve() can take an exp argument to set the exponent in
    exponential interpolation.
    '''
    t_line = notetools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Duration(2), Duration(1, 32), Duration(1, 8), 1)
    t_exp = notetools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Duration(2), Duration(1, 32), Duration(1, 8), 2)
    assert inspect(t_exp[4]).get_duration() < inspect(t_line[4]).get_duration()
