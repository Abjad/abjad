from abjad import *
import py.test


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_01():
    '''Construct train of 1/16th notes equal to 1/4 total duration.'''

    t = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(1, 4)))

    r'''
    \new Voice {
        c'16
        c'16
        c'16
        c'16
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_02():
    '''Construct train of 1/16th notes equal to 9/32 total duration.'''

    t = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(9, 32)))

    r'''
    \new Voice {
        c'16
        c'16
        c'16
        c'16
        c'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'32\n}"


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_03():
    '''Construct train of 1/16th notes equal to only 1/128 total duration.'''

    t = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(1, 128)))

    r'''
    \new Voice {
        c'128
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'128\n}"


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_04():
    '''Construct train of 1/16th notes equal to 4/10 total duration.'''

    t = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Duration(1, 16), Duration(4, 10)))

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\t\\times 4/5 {\n\t\tc'32\n\t}\n}"


def test_notetools_make_repeated_notes_with_shorter_notes_at_end_05():
    '''Construct train of written 1/16th notes within measure of 5/18.'''

    t = Measure((5, 18), notetools.make_repeated_notes_with_shorter_notes_at_end(
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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n}"
