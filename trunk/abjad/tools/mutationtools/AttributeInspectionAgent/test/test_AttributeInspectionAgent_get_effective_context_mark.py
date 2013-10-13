# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_AttributeInspectionAgent_get_effective_context_mark_01():
    r'''Clef defaults to none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in staff:
        clef = inspect(note).get_effective_context_mark(contexttools.ClefMark)
        assert clef is None


def test_AttributeInspectionAgent_get_effective_context_mark_02():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(staff)
    for note in staff:
        clef = inspect(note).get_effective_context_mark(contexttools.ClefMark)
        assert clef == contexttools.ClefMark('treble')


def test_AttributeInspectionAgent_get_effective_context_mark_03():
    r'''Clef defaults to none.
    Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('bass')(staff[4])
    for i, note in enumerate(staff):
        if i in (0, 1, 2, 3):
            clef = inspect(note).get_effective_context_mark(
                contexttools.ClefMark)
            assert clef is None
        else:
            clef = inspect(note).get_effective_context_mark(
                contexttools.ClefMark)
            assert clef == contexttools.ClefMark('bass')


def test_AttributeInspectionAgent_get_effective_context_mark_04():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    result = [
        inspect(note).get_effective_context_mark(contexttools.ClefMark)
        for note in staff
        ]
    clef_names = [
        'treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass',
        ]
    clefs = [contexttools.ClefMark(name) for name in clef_names]
    assert result == clefs


def test_AttributeInspectionAgent_get_effective_context_mark_05():
    r'''None cancels an explicit clef.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('bass')(staff[4])
    clef = inspect(staff[4]).get_effective_context_mark(contexttools.ClefMark)
    clef.detach()
    for note in staff:
        clef = inspect(note).get_effective_context_mark(contexttools.ClefMark)
        assert clef == contexttools.ClefMark('treble')


def test_AttributeInspectionAgent_get_effective_context_mark_06():
    r'''Redudant clefs are allowed.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    contexttools.ClefMark('treble')(staff[0])
    contexttools.ClefMark('treble')(staff[4])

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff).is_well_formed()


def test_AttributeInspectionAgent_get_effective_context_mark_07():
    r'''Clefs with transposition are allowed and work as expected.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    contexttools.ClefMark('treble_8')(staff[0])
    contexttools.ClefMark('treble')(staff[4])

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff).is_well_formed()


def test_AttributeInspectionAgent_get_effective_context_mark_08():
    r'''Attaching and then detaching works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.ClefMark('alto')(staff[0])
    clef = inspect(staff[0]).get_effective_context_mark(contexttools.ClefMark)
    clef.detach()

    for leaf in staff:
        clef = inspect(leaf).get_effective_context_mark(contexttools.ClefMark)
        assert clef is None


def test_AttributeInspectionAgent_get_effective_context_mark_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.DynamicMark('f')(staff[2])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8 \f
            f'8
        }
        '''
        )

    assert inspect(staff).get_effective_context_mark(
        contexttools.DynamicMark) is None
    assert inspect(staff[0]).get_effective_context_mark(
        contexttools.DynamicMark) is None
    assert inspect(staff[1]).get_effective_context_mark(
        contexttools.DynamicMark) is None
    assert inspect(staff[2]).get_effective_context_mark(
        contexttools.DynamicMark) == contexttools.DynamicMark('f')
    assert inspect(staff[3]).get_effective_context_mark(
        contexttools.DynamicMark) == contexttools.DynamicMark('f')


def test_AttributeInspectionAgent_get_effective_context_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    flute = instrumenttools.Flute()
    flute.attach(staff)

    assert testtools.compare(
        staff,
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
        )

    flute = instrumenttools.Flute()
    assert inspect(staff).get_effective_context_mark(
        instrumenttools.Instrument) == flute
    assert inspect(staff[0]).get_effective_context_mark(
        instrumenttools.Instrument) == flute
    assert inspect(staff[1]).get_effective_context_mark(
        instrumenttools.Instrument) == flute
    assert inspect(staff[2]).get_effective_context_mark(
        instrumenttools.Instrument) == flute
    assert inspect(staff[3]).get_effective_context_mark(
        instrumenttools.Instrument) == flute


def test_AttributeInspectionAgent_get_effective_context_mark_11():
    r'''Apply key signature mark.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.KeySignatureMark('c', 'major')(staff)

    key_signature = inspect(staff).get_effective_context_mark(
        contexttools.KeySignatureMark)
    assert key_signature == contexttools.KeySignatureMark('c', 'major')

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \key c \major
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_AttributeInspectionAgent_get_effective_context_mark_12():
    r'''There is no default key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = inspect(staff).get_effective_context_mark(
        contexttools.KeySignatureMark)
    assert key_signature is None


def test_AttributeInspectionAgent_get_effective_context_mark_13():
    r'''Tempo interface works on staves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TempoMark(Duration(1, 8), 38, target_context=Staff)(staff)
    contexttools.TempoMark(Duration(1, 8), 42, target_context=Staff)(staff[2])

    assert testtools.compare(
        staff,
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
        )

    assert inspect(staff).is_well_formed()
    assert inspect(staff[0]).get_effective_context_mark(
        contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 38)
    assert inspect(staff[1]).get_effective_context_mark(
        contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 38)
    assert inspect(staff[2]).get_effective_context_mark(
        contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 42)
    assert inspect(staff[3]).get_effective_context_mark(
        contexttools.TempoMark) == contexttools.TempoMark(Duration(1, 8), 42)


def test_AttributeInspectionAgent_get_effective_context_mark_14():
    r'''Tempo interface works on chords.
    '''

    staff = Staff([Chord([2, 3, 4], (1, 4))])
    contexttools.TempoMark(Duration(1, 8), 38, target_context=Staff)(staff[0])

    r'''
    \new Staff {
        \tempo 8=38
        <d' ef' e'>4
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            <d' ef' e'>4
        }
        '''
        )


def test_AttributeInspectionAgent_get_effective_context_mark_15():
    r'''Tempo interface accepts durations.
    '''

    staff = Staff([Note("c'4")])
    contexttools.TempoMark(Duration(1, 8), 38, target_context=Staff)(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            c'4
        }
        '''
        )


def test_AttributeInspectionAgent_get_effective_context_mark_16():
    r'''Detach tempo mark.
    '''

    staff = Staff([Note("c'4")])
    tempo = contexttools.TempoMark(Duration(1, 8), 38, target_context=Staff)
    tempo.attach(staff[0])
    tempo.detach()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'4
        }
        '''
        )


def test_AttributeInspectionAgent_get_effective_context_mark_17():
    r'''The default effective time signature is none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        time_signature = inspect(leaf).get_effective_context_mark(
            contexttools.TimeSignatureMark)
        assert time_signature is None


def test_AttributeInspectionAgent_get_effective_context_mark_18():
    r'''Forced time signature settings propagate to later leaves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.TimeSignatureMark((2, 8))(staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \time 2/8
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    for leaf in staff:
        time_signature = inspect(leaf).get_effective_context_mark(
            contexttools.TimeSignatureMark)
        assert time_signature == contexttools.TimeSignatureMark((2, 8))


def test_AttributeInspectionAgent_get_effective_context_mark_19():
    r'''InputSetExpression and then clearing works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = contexttools.TimeSignatureMark((2, 8))(staff[0])
    time_signature.detach()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    for leaf in staff:
        time_signature = inspect(leaf).get_effective_context_mark(
            contexttools.TimeSignatureMark)
        assert time_signature is None
