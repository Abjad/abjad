from abjad import *
import py.test


def test_Note___cmp___01():
    '''Compare equal notes.
    '''

    note_1 = Note(12, (1, 4))
    note_2 = Note(12, (1, 4))

    assert not note_1 == note_2
    assert      note_1 != note_2

    comparison_string = 'note_1 <  note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 <= note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >  note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >= note_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Note___cmp___02():
    '''Compare note to equivalent pitch, duration pair.
    '''

    note_1 = Note(12, (1, 4))
    pitch_duration_pair = (12, (1, 4))

    assert not note_1 == pitch_duration_pair
    assert      note_1 != pitch_duration_pair

    comparison_string = 'note_1 <  pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 <= pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >  pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >= pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Note___cmp___03():
    '''Compare unequal notes.
    '''

    note_1 = Note(12, (1, 4))
    note_2 = Note(13, (1, 4))

    assert not note_1 == note_2
    assert      note_1 != note_2

    comparison_string = 'note_1 <  note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 <= note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >  note_2'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >= note_2'
    assert py.test.raises(NotImplementedError, comparison_string)


def test_Note___cmp___04():
    '''Compare note to unequal note / pitch pair.
    '''

    note_1 = Note(12, (1, 4))
    pitch_duration_pair = (13, (1, 4))

    assert not note_1 == pitch_duration_pair
    assert      note_1 != pitch_duration_pair

    comparison_string = 'note_1 <  pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 <= pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >  pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
    comparison_string = 'note_1 >= pitch_duration_pair'
    assert py.test.raises(NotImplementedError, comparison_string)
