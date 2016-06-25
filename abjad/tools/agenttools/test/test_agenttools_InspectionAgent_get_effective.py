# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_effective_01():
    r'''Clef defaults to none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in staff:
        clef = inspect_(note).get_effective(Clef)
        assert clef is None


def test_agenttools_InspectionAgent_get_effective_02():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff)
    for note in staff:
        clef = inspect_(note).get_effective(Clef)
        assert clef == Clef('treble')


def test_agenttools_InspectionAgent_get_effective_03():
    r'''Clef defaults to none. Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('bass')
    attach(clef, staff[4])
    for i, note in enumerate(staff):
        if i in (0, 1, 2, 3):
            clef = inspect_(note).get_effective(Clef)
            assert clef is None
        else:
            clef = inspect_(note).get_effective(Clef)
            assert clef == Clef('bass')


def test_agenttools_InspectionAgent_get_effective_04():
    r'''Clefs carry over to notes following.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    result = [
        inspect_(note).get_effective(Clef)
        for note in staff
        ]
    clef_names = [
        'treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass',
        ]
    clefs = [Clef(name) for name in clef_names]
    assert result == clefs


def test_agenttools_InspectionAgent_get_effective_05():
    r'''None cancels an explicit clef.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('bass')
    attach(clef, staff[4])
    clef = inspect_(staff[4]).get_effective(Clef)
    detach(clef, staff[4])

    for note in staff:
        clef = inspect_(note).get_effective(Clef)
        assert clef == Clef('treble')


def test_agenttools_InspectionAgent_get_effective_06():
    r'''Redudant clefs are allowed.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble')
    attach(clef, staff[0])
    clef = Clef('treble')
    attach(clef, staff[4])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_07():
    r'''Clefs with transposition are allowed and work as expected.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = Clef('treble_8')
    attach(clef, staff[0])
    clef = Clef('treble')
    attach(clef, staff[4])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_08():
    r'''Attaching and then detaching works as expected.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = Clef('alto')
    attach(clef, staff[0])
    clef = inspect_(staff[0]).get_effective(Clef)
    detach(clef, staff[0])

    for leaf in staff:
        clef = inspect_(leaf).get_effective(Clef)
        assert clef is None


def test_agenttools_InspectionAgent_get_effective_09():

    staff = Staff("c'8 d'8 e'8 f'8")
    dynamic = Dynamic('f')
    attach(dynamic, staff[2])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8 \f
            f'8
        }
        '''
        )

    assert inspect_(staff).get_effective(Dynamic) is None
    assert inspect_(staff[0]).get_effective(Dynamic) is None
    assert inspect_(staff[1]).get_effective(Dynamic) is None
    assert inspect_(staff[2]).get_effective(Dynamic) == Dynamic('f')
    assert inspect_(staff[3]).get_effective(Dynamic) == Dynamic('f')


def test_agenttools_InspectionAgent_get_effective_10():

    staff = Staff("c'8 d'8 e'8 f'8")
    flute = instrumenttools.Flute()
    attach(flute, staff)

    assert format(staff) == stringtools.normalize(
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
    assert inspect_(staff).get_effective(instrumenttools.Instrument) == flute
    assert inspect_(staff[0]).get_effective(instrumenttools.Instrument) == flute
    assert inspect_(staff[1]).get_effective(instrumenttools.Instrument) == flute
    assert inspect_(staff[2]).get_effective(instrumenttools.Instrument) == flute
    assert inspect_(staff[3]).get_effective(instrumenttools.Instrument) == flute


def test_agenttools_InspectionAgent_get_effective_11():
    r'''Attach key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = KeySignature('c', 'major')
    attach(key_signature, staff)

    key_signature = inspect_(staff).get_effective(KeySignature)
    assert key_signature == KeySignature('c', 'major')

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_agenttools_InspectionAgent_get_effective_12():
    r'''There is no default key signature.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    key_signature = inspect_(staff).get_effective(KeySignature)
    assert key_signature is None


def test_agenttools_InspectionAgent_get_effective_13():
    r'''Attaches tempo to staff.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo_1 = Tempo(Duration(1, 8), 38)
    attach(tempo_1, staff, scope=Staff)
    tempo_2 = Tempo(Duration(1, 8), 42)
    attach(tempo_2, staff[2], scope=Staff)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()

    assert inspect_(staff[0]).get_effective(Tempo) == tempo_1
    assert inspect_(staff[1]).get_effective(Tempo) == tempo_1
    assert inspect_(staff[2]).get_effective(Tempo) == tempo_2
    assert inspect_(staff[3]).get_effective(Tempo) == tempo_2


def test_agenttools_InspectionAgent_get_effective_14():
    r'''Attaches tempo to chord in staff.
    '''

    staff = Staff([Chord([2, 3, 4], (1, 4))])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \tempo 8=38
            <d' ef' e'>4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_15():

    staff = Staff([Note("c'4")])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \tempo 8=38
            c'4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_16():
    r'''Detaches tempo.
    '''

    staff = Staff([Note("c'4")])
    tempo = Tempo(Duration(1, 8), 38)
    attach(tempo, staff[0], scope=Staff)
    detach(tempo, staff[0])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4
        }
        '''
        )


def test_agenttools_InspectionAgent_get_effective_17():
    r'''The default effective time signature is none.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        time_signature = inspect_(leaf).get_effective(TimeSignature)
        assert time_signature is None


def test_agenttools_InspectionAgent_get_effective_18():
    r'''Forced time signature settings propagate to later leaves.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((2, 8))
    attach(time_signature, staff[0])

    assert format(staff) == stringtools.normalize(
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
        time_signature = inspect_(leaf).get_effective(TimeSignature)
        assert time_signature == TimeSignature((2, 8))


def test_agenttools_InspectionAgent_get_effective_19():
    r'''Attach then detach.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    time_signature = TimeSignature((2, 8))
    attach(time_signature, staff[0])
    detach(time_signature, staff[0])

    assert format(staff) == stringtools.normalize(
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
        time_signature = inspect_(leaf).get_effective(TimeSignature)
        assert time_signature is None


def test_agenttools_InspectionAgent_get_effective_20():
    r'''Effective value of arbitrary object.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('color', staff[1], scope=Staff)

    assert inspect_(staff).get_effective(str) is None
    assert inspect_(staff[0]).get_effective(str) is None
    assert inspect_(staff[1]).get_effective(str) == 'color'
    assert inspect_(staff[2]).get_effective(str) == 'color'
    assert inspect_(staff[3]).get_effective(str) == 'color'


def test_agenttools_InspectionAgent_get_effective_21():
    staff = Staff("c'8 d'8 e'8 f'8 g'8")
    attach('red', staff[0], scope=Staff)
    attach('blue', staff[2], scope=Staff)
    attach('yellow', staff[4], scope=Staff)

    assert inspect_(staff[0]).get_effective(str, n=-1) is None
    assert inspect_(staff[0]).get_effective(str, n=0) == 'red'
    assert inspect_(staff[0]).get_effective(str, n=1) is 'blue'

    assert inspect_(staff[1]).get_effective(str, n=-1) is None
    assert inspect_(staff[1]).get_effective(str, n=0) == 'red'
    assert inspect_(staff[1]).get_effective(str, n=1) == 'blue'

    assert inspect_(staff[2]).get_effective(str, n=-1) == 'red'
    assert inspect_(staff[2]).get_effective(str, n=0) == 'blue'
    assert inspect_(staff[2]).get_effective(str, n=1) == 'yellow'

    assert inspect_(staff[3]).get_effective(str, n=-1) == 'red'
    assert inspect_(staff[3]).get_effective(str, n=0) == 'blue'
    assert inspect_(staff[3]).get_effective(str, n=1) == 'yellow'

    assert inspect_(staff[4]).get_effective(str, n=-1) == 'blue'
    assert inspect_(staff[4]).get_effective(str, n=0) == 'yellow'
    assert inspect_(staff[4]).get_effective(str, n=1) is None


def test_agenttools_InspectionAgent_get_effective_22():
    staff = Staff("c'8 d'8 e'8 f'8")
    attach('red', staff[-1], scope=Staff, synthetic_offset=-1)
    attach('blue', staff[0], scope=Staff)
    assert inspect_(staff).get_effective(str) == 'blue'
    assert inspect_(staff).get_effective(str, n=-1) == 'red'
