from abjad import *
import py.test


def test__Leaf_written_duration_01():
    '''Leaf durations can go up to 'maxima...': duration < (16, 1).
    '''

    t = Note(1, 2)

    assert t.format == "cs'\\breve"
    t.written_duration = Duration(3)
    assert t.format == "cs'\\breve."
    t.written_duration = Duration(4)
    assert t.format == "cs'\\longa"
    t.written_duration = Duration(6)
    assert t.format == "cs'\\longa."
    t.written_duration = Duration(7)
    assert t.format == "cs'\\longa.."
    t.written_duration = Duration(8)
    assert t.format == "cs'\\maxima"
    t.written_duration = Duration(12)
    assert t.format == "cs'\\maxima."
    t.written_duration = Duration(14)
    assert t.format == "cs'\\maxima.."
    t.written_duration = Duration(15)
    assert t.format == "cs'\\maxima..."
    assert py.test.raises(AssignabilityError, 'Note(1, 16)')
