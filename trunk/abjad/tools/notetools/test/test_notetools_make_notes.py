from abjad import *


def test_notetools_make_notes_01():
    '''
    notetools.make_notes can take a single pitch and a single duration.
    '''
    t = notetools.make_notes(1, (1,4))
    assert isinstance(t, list)
    assert len(t) == 1
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert not tietools.is_component_with_tie_spanner_attached(t[0])


def test_notetools_make_notes_02():
    '''Tied durations result in more than one tied Note.'''
    t = notetools.make_notes(1, (5, 8))
    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Note)
    assert t[0].written_duration == Duration(4, 8)
    assert t[1].written_duration == Duration(1, 8)
    assert tietools.is_component_with_tie_spanner_attached(t[0])
    assert tietools.is_component_with_tie_spanner_attached(t[1])

def test_notetools_make_notes_03():
    '''
    notetools.make_notes may take a list of pitches and a single duration.
    '''
    t = notetools.make_notes([1, 2], (1, 4))
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 1
    assert t[1].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 2

def test_notetools_make_notes_04():
    '''
    notetools.make_notes may take a single pitch and a list of duration.
    '''
    t = notetools.make_notes(1, [(1, 8), (1, 4)])
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 1
    assert t[1].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 1
    assert t[0].written_duration == Duration(1, 8)
    assert t[1].written_duration == Duration(1, 4)

def test_notetools_make_notes_05():
    '''
    notetools.make_notes may take a list of pitches and list of durations.
    '''
    t = notetools.make_notes([0, 1], [(1, 8), (1, 4)])
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 0
    assert t[1].written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == 1
    assert t[0].written_duration == Duration(1, 8)
    assert t[1].written_duration == Duration(1, 4)


def test_notetools_make_notes_06():
    '''
    Durations can be Durations.
    '''
    t = notetools.make_notes(1, Duration(1, 4))
    assert len(t) == 1
    assert t[0].written_duration == Duration(1, 4)

def test_notetools_make_notes_07():
    '''
    Durations can be a list of Durations.
    '''
    t = notetools.make_notes(1, [Duration(1, 4)])
    assert len(t) == 1
    assert t[0].written_duration == Duration(1, 4)

def test_notetools_make_notes_08():
    '''
    Key word 'direction' == 'big_endian' returns note durations in descending
    order. This is the default.
    '''
    t = notetools.make_notes(1, (5, 16), direction='big-endian')
    assert len(t) == 2
    assert t[0].written_duration == Duration(4, 16)
    assert t[1].written_duration == Duration(1, 16)

def test_notetools_make_notes_09():
    '''
    Key word 'direction' == 'little_endian' returns note durations in ascending
    order.
    '''
    t = notetools.make_notes(1, (5, 16), direction='little-endian')
    assert len(t) == 2
    assert t[0].written_duration == Duration(1, 16)
    assert t[1].written_duration == Duration(4, 16)


# PROLATED NOTES #

def test_notetools_make_notes_10():
    '''
    make_notes() can take parameters for a single prolated note.
    '''
    t = notetools.make_notes(1, (1, 36))
    assert len(t) == 1
    assert isinstance(t[0], Tuplet)
    assert len(t[0]) == 1
    assert t[0].prolated_duration == Duration(1, 36)
    assert t[0][0].prolated_duration == Duration(1, 36)
    assert t[0][0].written_duration == Duration(1, 32)


def test_notetools_make_notes_11():
    '''
    make_notes() can take a single pitch and a list of prolated durations.
    '''
    t = notetools.make_notes(1, [(1, 12), (1, 6), (1, 8)])
    assert len(t) == 2
    assert isinstance(t[0], Tuplet)
    assert isinstance(t[1], Note)
    assert len(t[0]) == 2
    assert t[0].prolated_duration == Duration(3, 12)
    assert t[0][0].prolated_duration == Duration(1, 12)
    assert t[0][1].prolated_duration == Duration(1, 6)
    assert t[0][0].written_duration == Duration(1, 8)
    assert t[0][1].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
    r'''
    \times 2/3 {
        cs'8
        cs'4
    }
    cs'8
    '''


def test_notetools_make_notes_12():
    '''
    make_notes() may take a direction attribute.
    '''
    t = notetools.make_notes(1, [(5, 12), (1, 6), (1, 8)], \
        direction='little-endian')
    assert len(t) == 2
    assert isinstance(t[0], Tuplet)
    assert isinstance(t[1], Note)
    assert len(t[0]) == 3
    assert t[0].prolated_duration == Duration(7, 12)
    assert t[0][0].prolated_duration == Duration(1, 12)
    assert t[0][1].prolated_duration == Duration(4, 12)
    assert t[0][2].prolated_duration == Duration(1, 6)
    assert t[0][0].written_duration == Duration(1, 8)
    assert t[0][1].written_duration == Duration(4, 8)
    assert t[0][2].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
