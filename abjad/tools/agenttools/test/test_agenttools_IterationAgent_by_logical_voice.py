# -*- coding: utf-8 -*-
import abjad


def test_agenttools_IterationAgent_by_logical_voice_01():
    r'''Yields nothing when class not present.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Rest,
        logical_voice,
        reverse=True,
        )

    assert len(list(iterator)) == 0


def test_agenttools_IterationAgent_by_logical_voice_02():
    r'''Yields internal nodes only.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Tuplet,
        logical_voice,
        reverse=True,
        )

    assert len(list(iterator)) == 3


def test_agenttools_IterationAgent_by_logical_voice_03():
    r'''Yields exact leaves.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        reverse=True,
        )

    assert len(list(iterator)) == 9


def test_agenttools_IterationAgent_by_logical_voice_04():
    r'''Yields leaves based on names higher in inheritence hierarchy.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[-1][-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Leaf,
        logical_voice,
        reverse=True,
        )

    assert len(list(iterator)) == 9


def test_agenttools_IterationAgent_by_logical_voice_05():
    r'''Yields notes in two contiguous Voices with the same name.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    voice_1.name = voice_2.name = 'piccolo'
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        reverse=True,
        )
    iterator = list(iterator)

    assert len(iterator) == 4
    for note in iterator:
        assert isinstance(note, abjad.Note)


def test_agenttools_IterationAgent_by_logical_voice_06():
    r'''Yields only notes matching the given logical voice.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        reverse=True,
        )
    iterator = list(iterator)

    assert len(iterator) == 2
    for note in iterator:
        assert isinstance(note, abjad.Note)
        assert note.written_pitch.number == 2


def test_agenttools_IterationAgent_by_logical_voice_07():
    r'''Yields only notes matching the given logical voice.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    voice_1.name = 'flute'
    voice_2.name = 'piccolo'
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[-1]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        reverse=True,
        )
    iterator = list(iterator)

    assert len(iterator) == 2
    for e in iterator:
        assert isinstance(e, abjad.Note)
        assert e.written_pitch.number == 2


def test_agenttools_IterationAgent_by_logical_voice_08():
    r'''Yields nothing when class not present.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Rest,
        logical_voice,
        )

    assert len(list(iterator)) == 0


def test_agenttools_IterationAgent_by_logical_voice_09():
    r'''Yields internal nodes only.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Tuplet,
        logical_voice,
        )
    assert len(list(iterator)) == 3


def test_agenttools_IterationAgent_by_logical_voice_10():
    r'''Yields exact leaves.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        )

    assert len(list(iterator)) == 9


def test_agenttools_IterationAgent_by_logical_voice_11():
    r'''Yields leaves based on names higher in inheritence hierarchy.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier(2, 3), "c'4 c'4 c'4")
    staff = abjad.Staff(3 * tuplet)
    logical_voice = abjad.inspect(staff[0][0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Leaf,
        logical_voice,
        )

    assert len(list(iterator)) == 9


def test_agenttools_IterationAgent_by_logical_voice_12():
    r'''Yields notes in two contiguous Voices with the same name.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    voice_1.name = voice_2.name = 'piccolo'
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        )
    iterator = list(iterator)

    assert len(iterator) == 4
    for note in iterator:
        assert isinstance(note, abjad.Note)


def test_agenttools_IterationAgent_by_logical_voice_13():
    r'''Yields only notes matching the given logical voice.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        )
    iterator = list(iterator)

    assert len(iterator) == 2
    for note in iterator:
        assert isinstance(note, abjad.Note)
        assert note.written_pitch.number == 0


def test_agenttools_IterationAgent_by_logical_voice_14():
    r'''Yields only notes matching the given logical voice.
    '''

    voice_1 = abjad.Voice("c'4 c'4")
    voice_2 = abjad.Voice("d'4 d'4")
    voice_1.name = 'flute'
    voice_2.name = 'piccolo'
    staff = abjad.Staff([voice_1, voice_2])
    logical_voice = abjad.inspect(staff[0]).get_parentage().logical_voice
    iterator = abjad.iterate(staff).by_logical_voice(
        abjad.Note,
        logical_voice,
        )
    iterator = list(iterator)

    assert len(iterator) == 2
    for note in iterator:
        assert isinstance(note, abjad.Note)
        assert note.written_pitch.number == 0
