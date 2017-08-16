import abjad


def test_scoretools_Leaf__multiplied_duration_01():
    r'''Mulplied duration == written * multiplier.
    '''

    note = abjad.Note("c'4")
    abjad.attach(abjad.Multiplier(1, 2), note)
    assert note._get_multiplied_duration() == abjad.Duration(1, 8)


def test_scoretools_Leaf__multiplied_duration_02():
    r'''Mulplied duration equals duration when multiplier is none.
    '''

    note = abjad.Note("c'4")
    assert note._get_multiplied_duration() == abjad.Duration(1, 4)


def test_scoretools_Leaf__multiplied_duration_03():
    r'''Attach multiplier and then abjad.detach multiplier.
    '''

    note = abjad.Note("c'4")
    note.written_duration = abjad.Duration(3, 8)
    abjad.attach(abjad.Multiplier(2, 3), note)

    assert note.written_duration == abjad.Duration(3, 8)
    assert abjad.inspect(note).get_indicator(abjad.Multiplier) == abjad.Multiplier(2, 3)
    assert note._get_multiplied_duration() == abjad.Duration(1, 4)

    note.written_duration = abjad.Duration(1, 4)
    abjad.detach(abjad.Multiplier, note)

    assert note.written_duration == abjad.Duration(1, 4)
    assert abjad.inspect(note).get_indicators(abjad.Multiplier) == ()
    assert note._get_multiplied_duration() == abjad.Duration(1, 4)
