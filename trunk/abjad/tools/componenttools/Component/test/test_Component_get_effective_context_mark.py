from abjad import *
import py.test


def test_Component_get_effective_context_mark_01():
    '''Clef defaults to none.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in t:
        assert note.get_effective_context_mark(contexttools.ClefMark) is None


def test_Component_get_effective_context_mark_02():
    '''Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t)
    for note in t:
        assert note.get_effective_context_mark(contexttools.ClefMark) == \
            contexttools.ClefMark('treble')


def test_Component_get_effective_context_mark_03():
    '''Clef defaults to none.
    Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('bass')(t[4])
    for i, note in enumerate(t):
        if i in (0, 1, 2, 3):
            assert note.get_effective_context_mark(contexttools.ClefMark) is None
        else:
            assert note.get_effective_context_mark(contexttools.ClefMark) == \
                contexttools.ClefMark('bass')


def test_Component_get_effective_context_mark_04():
    '''Clefs carry over to notes following.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    assert [note.get_effective_context_mark(contexttools.ClefMark)
        for note in t] == \
        [contexttools.ClefMark(name) for name in ['treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass']]


def test_Component_get_effective_context_mark_05():
    '''None cancels an explicit clef.
    '''

    t = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('bass')(t[4])
    clef = t[4].get_effective_context_mark(contexttools.ClefMark)
    clef.detach()
    for note in t:
        assert note.get_effective_context_mark(contexttools.ClefMark) == \
            contexttools.ClefMark('treble')


def test_Component_get_effective_context_mark_06():
    '''Redudant clefs are allowed.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    contexttools.ClefMark('treble')(t[0])
    contexttools.ClefMark('treble')(t[4])

    r'''
    \new Staff {
        \clef "treble"
        c'8
        cs'8
        d'8
        ef'8
        \clef "treble"
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == '\\new Staff {\n\t\\clef "treble"\n\tc\'8\n\tcs\'8\n\td\'8\n\tef\'8\n\t\\clef "treble"\n\te\'8\n\tf\'8\n\tfs\'8\n\tg\'8\n}'


def test_Component_get_effective_context_mark_07():
    '''Clefs with transposition are allowed and work as expected.
    '''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr(t)
    contexttools.ClefMark('treble_8')(t[0])
    contexttools.ClefMark('treble')(t[4])

    r'''
    \new Staff {
        \clef "treble_8"
        c'8
        cs'8
        d'8
        ef'8
        \clef "treble"
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == '\\new Staff {\n\t\\clef "treble_8"\n\tc\'8\n\tcs\'8\n\td\'8\n\tef\'8\n\t\\clef "treble"\n\te\'8\n\tf\'8\n\tfs\'8\n\tg\'8\n}'


def test_Component_get_effective_context_mark_08():
    '''InputSetExpression and then clearing works as expected.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('alto')(t[0])
    clef = t[0].get_effective_context_mark(contexttools.ClefMark)
    clef.detach()

    for leaf in t:
        assert leaf.get_effective_context_mark(contexttools.ClefMark) is None


def test_Component_get_effective_context_mark_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.DynamicMark('f')(staff[2])

    r'''
    \new Staff {
        c'8
        d'8
        e'8 \f
        f'8
    }
    '''

    assert staff.get_effective_context_mark(contexttools.DynamicMark) is None
    assert staff[0].get_effective_context_mark(contexttools.DynamicMark) is None
    assert staff[1].get_effective_context_mark(contexttools.DynamicMark) is None
    assert staff[2].get_effective_context_mark(contexttools.DynamicMark) == contexttools.DynamicMark('f')
    assert staff[3].get_effective_context_mark(contexttools.DynamicMark) == contexttools.DynamicMark('f')


def test_Component_get_effective_context_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.InstrumentMark('Flute', 'Fl.')(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Flute }
        \set Staff.shortInstrumentName = \markup { Fl. }
        c'8
        d'8
        e'8
        f'8
    }
    '''

    flute = contexttools.InstrumentMark('Flute', 'Fl.')
    assert staff.get_effective_context_mark(contexttools.InstrumentMark) == flute
    assert staff[0].get_effective_context_mark(contexttools.InstrumentMark) == flute
    assert staff[1].get_effective_context_mark(contexttools.InstrumentMark) == flute
    assert staff[2].get_effective_context_mark(contexttools.InstrumentMark) == flute
    assert staff[3].get_effective_context_mark(contexttools.InstrumentMark) == flute


def test_Component_get_effective_context_mark_11():
    '''Apply key signature mark.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.KeySignatureMark('c', 'major')(t)

    r'''
    \new Staff {
        \key c \major
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert t.get_effective_context_mark(contexttools.KeySignatureMark) == contexttools.KeySignatureMark('c', 'major')
    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Staff {\n\t\\key c \\major\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_Component_get_effective_context_mark_12():
    '''There is no default key signature.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    assert t.get_effective_context_mark(contexttools.KeySignatureMark) is None


def test_Component_get_effective_context_mark_13():
    '''Tempo interface works on staves.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(t)
    contexttools.TempoMark(Duration(1, 8), 42, target_context = Staff)(t[2])

    r'''
    \new Staff {
        \tempo 8=38
        c'8
        d'8
        \tempo 8=42
        e'8
        f'8
    }
    '''

    assert select(t).is_well_formed()
    assert t[0].get_effective_context_mark(contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 38)
    assert t[1].get_effective_context_mark(contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 38)
    assert t[2].get_effective_context_mark(contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 42)
    assert t[3].get_effective_context_mark(contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 42)
    assert t.lilypond_format == "\\new Staff {\n\t\\tempo 8=38\n\tc'8\n\td'8\n\t\\tempo 8=42\n\te'8\n\tf'8\n}"



def test_Component_get_effective_context_mark_14():
    '''Tempo interface works on chords.
    '''

    t = Staff([Chord([2, 3, 4], (1, 4))])
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(t[0])

    r'''
    \new Staff {
        \tempo 8=38
        <d' ef' e'>4
    }
    '''

    assert t.lilypond_format == "\\new Staff {\n\t\\tempo 8=38\n\t<d' ef' e'>4\n}"


def test_Component_get_effective_context_mark_15():
    '''Tempo interface accepts durations.
    '''

    staff = Staff([Note("c'4")])
    contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(staff[0])

    r'''
    \new Staff {
        \tempo 8=38
        c'4
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t\\tempo 8=38\n\tc'4\n}"


def test_Component_get_effective_context_mark_16():
    '''Detach tempo mark.
    '''

    staff = Staff([Note("c'4")])
    tempo = contexttools.TempoMark(Duration(1, 8), 38, target_context = Staff)(staff[0])
    tempo.detach()


    r'''
    \new Staff {
        c'4
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'4\n}"


def test_Component_get_effective_context_mark_17():
    '''The default effective time signature is none.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert leaf.get_effective_context_mark(
            contexttools.TimeSignatureMark) is None


def test_Component_get_effective_context_mark_18():
    '''Forced time signature settings propagate to later leaves.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 8))(t[0])

    r'''
    \new Staff {
        \time 2/8
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert leaf.get_effective_context_mark(
            contexttools.TimeSignatureMark) == contexttools.TimeSignatureMark(
                (2, 8))


def test_Component_get_effective_context_mark_19():
    '''InputSetExpression and then clearing works as expected.
    '''

    t = Staff("c'8 d'8 e'8 f'8")
    time_signature = contexttools.TimeSignatureMark((2, 8))(t[0])
    time_signature.detach()

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    for leaf in t:
        assert leaf.get_effective_context_mark(
            contexttools.TimeSignatureMark) is None
