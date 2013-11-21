# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_effective_indicator_01():
    r'''Clef defaults to none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in staff:
        clef = inspect(note).get_effective_context_mark(Clef)
        assert clef is None


def test_agenttools_InspectionAgent_get_effective_indicator_02():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff)
    for note in staff:
        clef = inspect(note).get_effective_context_mark(Clef)
        assert clef == Clef('treble')


def test_agenttools_InspectionAgent_get_effective_indicator_03():
    r'''Clef defaults to none.
    Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('bass')
    attach(clef, staff[4])
    for i, note in enumerate(staff):
        if i in (0, 1, 2, 3):
            clef = inspect(note).get_effective_context_mark(
                Clef)
            assert clef is None
        else:
            clef = inspect(note).get_effective_context_mark(
                Clef)
            assert clef == Clef('bass')


def test_agenttools_InspectionAgent_get_effective_indicator_04():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    result = [
        inspect(note).get_effective_context_mark(Clef)
        for note in staff
        ]
    clef_names = [
        'treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass',
        ]
    clefs = [Clef(name) for name in clef_names]
    assert result == clefs


def test_agenttools_InspectionAgent_get_effective_indicator_05():
    r'''None cancels an explicit clef.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    clef = inspect(staff[4]).get_effective_context_mark(Clef)
    detach(clef, staff[4])

    for note in staff:
        clef = inspect(note).get_effective_context_mark(Clef)
        assert clef == Clef('treble')


def test_agenttools_InspectionAgent_get_effective_indicator_06():
    r'''Redudant clefs are allowed.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('treble')
    attach(clef, staff[4])

    assert systemtools.TestManager.compare(
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


def test_agenttools_InspectionAgent_get_effective_indicator_07():
    r'''Clefs with transposition are allowed and work as expected.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble_8')
    attach(clef, staff[0])
    clef = Clef('treble')
    attach(clef, staff[4])

    assert systemtools.TestManager.compare(
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


def test_agenttools_InspectionAgent_get_effective_indicator_08():
    r'''Attaching and then detaching works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('alto')
    attach(clef, staff[0])
    clef = inspect(staff[0]).get_effective_context_mark(Clef)
    detach(clef, staff[0])

    for leaf in staff:
        clef = inspect(leaf).get_effective_context_mark(Clef)
        assert clef is None


def test_agenttools_InspectionAgent_get_effective_indicator_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    dynamic = Dynamic('f')
    attach(dynamic, staff[2])

    assert systemtools.TestManager.compare(
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
        Dynamic) is None
    assert inspect(staff[0]).get_effective_context_mark(
        Dynamic) is None
    assert inspect(staff[1]).get_effective_context_mark(
        Dynamic) is None
    assert inspect(staff[2]).get_effective_context_mark(
        Dynamic) == Dynamic('f')
    assert inspect(staff[3]).get_effective_context_mark(
        Dynamic) == Dynamic('f')


def test_agenttools_InspectionAgent_get_effective_indicator_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    flute = instrumenttools.Flute()
    attach(flute, staff)

    assert systemtools.TestManager.compare(
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


def test_agenttools_InspectionAgent_get_effective_indicator_11():
    r'''Apply key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = KeySignature('c', 'major')
    attach(key_signature, staff)

    key_signature = inspect(staff).get_effective_context_mark(KeySignature)
    assert key_signature == KeySignature('c', 'major')

    assert systemtools.TestManager.compare(
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


def test_agenttools_InspectionAgent_get_effective_indicator_12():
    r'''There is no default key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = inspect(staff).get_effective_context_mark(KeySignature)
    assert key_signature is None


def test_agenttools_InspectionAgent_get_effective_indicator_13():
    r'''Attaches tempo to staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff, scope=Staff)
    tempo = Tempo(Duration(1, 8), 42)
    attach(tempo, staff[2], scope=Staff)

    assert systemtools.TestManager.compare(
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
        Tempo) == Tempo(Duration(1, 8), 38)
    assert inspect(staff[1]).get_effective_context_mark(
        Tempo) == Tempo(Duration(1, 8), 38)
    assert inspect(staff[2]).get_effective_context_mark(
        Tempo) == Tempo(Duration(1, 8), 42)
    assert inspect(staff[3]).get_effective_context_mark(
        Tempo) == Tempo(Duration(1, 8), 42)


def test_agenttools_InspectionAgent_get_effective_indicator_14():
    r'''Attaches tempo to chord in staff.
    '''

    staff = Staff([Chord([2, 3, 4], (1, 4))])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            <d' ef' e'>4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_indicator_15():

    staff = Staff([Note("c'4")])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=38
            c'4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_indicator_16():
    r'''Detaches tempo.
    '''

    staff = Staff([Note("c'4")])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)
    detach(tempo, staff[0])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_indicator_17():
    r'''The default effective time signature is none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        time_signature = inspect(leaf).get_effective_context_mark(
            TimeSignature)
        assert time_signature is None


def test_agenttools_InspectionAgent_get_effective_indicator_18():
    r'''Forced time signature settings propagate to later leaves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((2, 8))
    attach(time_signature, staff[0])

    assert systemtools.TestManager.compare(
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
            TimeSignature)
        assert time_signature == TimeSignature((2, 8))


def test_agenttools_InspectionAgent_get_effective_indicator_19():
    r'''Attach then detach.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((2, 8))
    attach(time_signature, staff[0])
    detach(time_signature, staff[0])

    assert systemtools.TestManager.compare(
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
            TimeSignature)
        assert time_signature is None
