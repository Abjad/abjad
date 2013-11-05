# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_01():
    r'''Clef defaults to none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in staff:
        clef = inspect(note).get_effective_context_mark(marktools.ClefMark)
        assert clef is None


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_02():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = marktools.ClefMark('treble')
    attach(clef, staff)
    for note in staff:
        clef = inspect(note).get_effective_context_mark(marktools.ClefMark)
        assert clef == marktools.ClefMark('treble')


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_03():
    r'''Clef defaults to none.
    Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = marktools.ClefMark('bass')
    attach(clef, staff[4])
    for i, note in enumerate(staff):
        if i in (0, 1, 2, 3):
            clef = inspect(note).get_effective_context_mark(
                marktools.ClefMark)
            assert clef is None
        else:
            clef = inspect(note).get_effective_context_mark(
                marktools.ClefMark)
            assert clef == marktools.ClefMark('bass')


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_04():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = marktools.ClefMark('treble')
    attach(clef, staff[0])
    clef = marktools.ClefMark('bass')
    attach(clef, staff[4])
    result = [
        inspect(note).get_effective_context_mark(marktools.ClefMark)
        for note in staff
        ]
    clef_names = [
        'treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass',
        ]
    clefs = [marktools.ClefMark(name) for name in clef_names]
    assert result == clefs


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_05():
    r'''None cancels an explicit clef.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = marktools.ClefMark('treble')
    attach(clef, staff[0])
    clef = marktools.ClefMark('bass')
    attach(clef, staff[4])
    clef = inspect(staff[4]).get_effective_context_mark(marktools.ClefMark)
    clef.detach()

    for note in staff:
        clef = inspect(note).get_effective_context_mark(marktools.ClefMark)
        assert clef == marktools.ClefMark('treble')


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_06():
    r'''Redudant clefs are allowed.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = marktools.ClefMark('treble')
    attach(clef, staff[0])
    clef = marktools.ClefMark('treble')
    attach(clef, staff[4])

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


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_07():
    r'''Clefs with transposition are allowed and work as expected.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = marktools.ClefMark('treble_8')
    attach(clef, staff[0])
    clef = marktools.ClefMark('treble')
    attach(clef, staff[4])

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


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_08():
    r'''Attaching and then detaching works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = marktools.ClefMark('alto')
    attach(clef, staff[0])
    clef = inspect(staff[0]).get_effective_context_mark(marktools.ClefMark)
    clef.detach()

    for leaf in staff:
        clef = inspect(leaf).get_effective_context_mark(marktools.ClefMark)
        assert clef is None


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    dynamic = marktools.DynamicMark('f')
    attach(dynamic, staff[2])

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
        marktools.DynamicMark) is None
    assert inspect(staff[0]).get_effective_context_mark(
        marktools.DynamicMark) is None
    assert inspect(staff[1]).get_effective_context_mark(
        marktools.DynamicMark) is None
    assert inspect(staff[2]).get_effective_context_mark(
        marktools.DynamicMark) == marktools.DynamicMark('f')
    assert inspect(staff[3]).get_effective_context_mark(
        marktools.DynamicMark) == marktools.DynamicMark('f')


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    flute = instrumenttools.Flute()
    attach(flute, staff)

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


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_11():
    r'''Apply key signature mark.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = marktools.KeySignatureMark('c', 'major')
    attach(key_signature, staff)

    key_signature = inspect(staff).get_effective_context_mark(
        marktools.KeySignatureMark)
    assert key_signature == marktools.KeySignatureMark('c', 'major')

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


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_12():
    r'''There is no default key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = inspect(staff).get_effective_context_mark(
        marktools.KeySignatureMark)
    assert key_signature is None


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_13():
    r'''Tempo interface works on staves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = marktools.TempoMark(Duration(1, 8), 38, target_context=Staff)
    attach(tempo, staff)
    tempo = marktools.TempoMark(Duration(1, 8), 42, target_context=Staff)
    attach(tempo, staff[2])

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
        marktools.TempoMark) == marktools.TempoMark(Duration(1, 8), 38)
    assert inspect(staff[1]).get_effective_context_mark(
        marktools.TempoMark) == marktools.TempoMark(Duration(1, 8), 38)
    assert inspect(staff[2]).get_effective_context_mark(
        marktools.TempoMark) == marktools.TempoMark(Duration(1, 8), 42)
    assert inspect(staff[3]).get_effective_context_mark(
        marktools.TempoMark) == marktools.TempoMark(Duration(1, 8), 42)


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_14():
    r'''Tempo interface works on chords.
    '''

    staff = Staff([Chord([2, 3, 4], (1, 4))])
    tempo = marktools.TempoMark(Duration(1, 8), 38, target_context=Staff)
    attach(tempo, staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            <d' ef' e'>4
        }
        '''
        )


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_15():
    r'''Tempo interface accepts durations.
    '''

    staff = Staff([Note("c'4")])
    tempo = marktools.TempoMark(Duration(1, 8), 38, target_context=Staff)
    attach(tempo, staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            c'4
        }
        '''
        )


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_16():
    r'''Detach tempo mark.
    '''

    staff = Staff([Note("c'4")])
    tempo = marktools.TempoMark(Duration(1, 8), 38, target_context=Staff)
    attach(tempo, staff[0])
    tempo.detach()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'4
        }
        '''
        )


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_17():
    r'''The default effective time signature is none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        time_signature = inspect(leaf).get_effective_context_mark(
            marktools.TimeSignatureMark)
        assert time_signature is None


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_18():
    r'''Forced time signature settings propagate to later leaves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = marktools.TimeSignatureMark((2, 8))
    attach(time_signature, staff[0])

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
            marktools.TimeSignatureMark)
        assert time_signature == marktools.TimeSignatureMark((2, 8))


def test_mutationtools_AttributeInspectionAgent_get_effective_context_mark_19():
    r'''InputSetExpression and then clearing works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = marktools.TimeSignatureMark((2, 8))
    attach(time_signature, staff[0])
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
            marktools.TimeSignatureMark)
        assert time_signature is None
