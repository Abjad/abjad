import abjad
import pytest


def test_scoretools_Inspection_get_effective_01():
    r'''Clef defaults to none.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    for note in staff:
        clef = abjad.inspect(note).get_effective(abjad.Clef)
        assert clef is None


def test_scoretools_Inspection_get_effective_02():
    r'''Clefs carry over to notes following.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[0])
    for note in staff:
        clef = abjad.inspect(note).get_effective(abjad.Clef)
        assert clef == abjad.Clef('treble')


def test_scoretools_Inspection_get_effective_03():
    r'''Clef defaults to none. abjad.Clefs carry over to notes following.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff[4])
    for i, note in enumerate(staff):
        if i in (0, 1, 2, 3):
            clef = abjad.inspect(note).get_effective(abjad.Clef)
            assert clef is None
        else:
            clef = abjad.inspect(note).get_effective(abjad.Clef)
            assert clef == abjad.Clef('bass')


def test_scoretools_Inspection_get_effective_04():
    r'''Clefs carry over to notes following.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[0])
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff[4])
    result = [
        abjad.inspect(note).get_effective(abjad.Clef)
        for note in staff
        ]
    clef_names = [
        'treble', 'treble', 'treble', 'treble',
        'bass', 'bass', 'bass', 'bass',
        ]
    clefs = [abjad.Clef(name) for name in clef_names]
    assert result == clefs


def test_scoretools_Inspection_get_effective_05():
    r'''None cancels an explicit clef.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[0])
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff[4])
    clef = abjad.inspect(staff[4]).get_effective(abjad.Clef)
    abjad.detach(clef, staff[4])

    for note in staff:
        clef = abjad.inspect(note).get_effective(abjad.Clef)
        assert clef == abjad.Clef('treble')


def test_scoretools_Inspection_get_effective_06():
    r'''Redudant clefs are allowed.
    '''

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[0])
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[4])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Inspection_get_effective_07():
    r'''Clefs with transposition are allowed and work as expected.
    '''

    staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    clef = abjad.Clef('treble_8')
    abjad.attach(clef, staff[0])
    clef = abjad.Clef('treble')
    abjad.attach(clef, staff[4])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Inspection_get_effective_08():
    r'''Attaching and then abjad.detaching works as expected.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    clef = abjad.Clef('alto')
    abjad.attach(clef, staff[0])
    clef = abjad.inspect(staff[0]).get_effective(abjad.Clef)
    abjad.detach(clef, staff[0])

    for leaf in staff:
        clef = abjad.inspect(leaf).get_effective(abjad.Clef)
        assert clef is None


def test_scoretools_Inspection_get_effective_09():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, staff[2])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8
            d'8
            e'8 \f
            f'8
        }
        '''
        )

    assert abjad.inspect(staff).get_effective(abjad.Dynamic) is None
    assert abjad.inspect(staff[0]).get_effective(abjad.Dynamic) is None
    assert abjad.inspect(staff[1]).get_effective(abjad.Dynamic) is None
    assert abjad.inspect(staff[2]).get_effective(abjad.Dynamic) == abjad.Dynamic('f')
    assert abjad.inspect(staff[3]).get_effective(abjad.Dynamic) == abjad.Dynamic('f')


def test_scoretools_Inspection_get_effective_10():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    flute = abjad.instrumenttools.Flute()
    abjad.attach(flute, staff[0])

    assert format(staff) == abjad.String.normalize(
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

    flute = abjad.instrumenttools.Flute()
    assert abjad.inspect(staff).get_effective(abjad.instrumenttools.Instrument) == flute
    assert abjad.inspect(staff[0]).get_effective(abjad.instrumenttools.Instrument) == flute
    assert abjad.inspect(staff[1]).get_effective(abjad.instrumenttools.Instrument) == flute
    assert abjad.inspect(staff[2]).get_effective(abjad.instrumenttools.Instrument) == flute
    assert abjad.inspect(staff[3]).get_effective(abjad.instrumenttools.Instrument) == flute


def test_scoretools_Inspection_get_effective_11():
    r'''Attach key signature.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    key_signature = abjad.KeySignature('c', 'major')
    abjad.attach(key_signature, staff[0])

    key_signature = abjad.inspect(staff).get_effective(abjad.KeySignature)
    assert key_signature == abjad.KeySignature('c', 'major')

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Inspection_get_effective_12():
    r'''There is no default key signature.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    key_signature = abjad.inspect(staff).get_effective(abjad.KeySignature)
    assert key_signature is None


def test_scoretools_Inspection_get_effective_13():
    r'''Attaches metronome mark to staff.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark_1 = abjad.MetronomeMark(abjad.Duration(1, 8), 38)
    abjad.attach(mark_1, staff[0], context='Staff')
    mark_2 = abjad.MetronomeMark(abjad.Duration(1, 8), 42)
    abjad.attach(mark_2, staff[2], context='Staff')

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()

    assert abjad.inspect(staff[0]).get_effective(abjad.MetronomeMark) == mark_1
    assert abjad.inspect(staff[1]).get_effective(abjad.MetronomeMark) == mark_1
    assert abjad.inspect(staff[2]).get_effective(abjad.MetronomeMark) == mark_2
    assert abjad.inspect(staff[3]).get_effective(abjad.MetronomeMark) == mark_2


def test_scoretools_Inspection_get_effective_14():
    r'''Attaches metronome mark to chord in staff.
    '''

    staff = abjad.Staff([abjad.Chord([2, 3, 4], (1, 4))])
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 38)
    abjad.attach(mark, staff[0], context='Staff')

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \tempo 8=38
            <d' ef' e'>4
        }
        '''
        )


def test_scoretools_Inspection_get_effective_15():

    staff = abjad.Staff([abjad.Note("c'4")])
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 38)
    abjad.attach(mark, staff[0], context='Staff')

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \tempo 8=38
            c'4
        }
        '''
        )


def test_scoretools_Inspection_get_effective_16():
    r'''Detaches metronome mark.
    '''

    staff = abjad.Staff([abjad.Note("c'4")])
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 38)
    abjad.attach(mark, staff[0], context='Staff')
    abjad.detach(mark, staff[0])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4
        }
        '''
        )


def test_scoretools_Inspection_get_effective_17():
    r'''The default effective time signature is none.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    for leaf in staff:
        time_signature = abjad.inspect(leaf).get_effective(abjad.TimeSignature)
        assert time_signature is None


def test_scoretools_Inspection_get_effective_18():
    r'''Forced time signature abjad.settings propagate to later leaves.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    time_signature = abjad.TimeSignature((2, 8))
    abjad.attach(time_signature, staff[0])

    assert format(staff) == abjad.String.normalize(
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
        time_signature = abjad.inspect(leaf).get_effective(abjad.TimeSignature)
        assert time_signature == abjad.TimeSignature((2, 8))


def test_scoretools_Inspection_get_effective_19():
    r'''Attach then abjad.detach.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    time_signature = abjad.TimeSignature((2, 8))
    abjad.attach(time_signature, staff[0])
    abjad.detach(time_signature, staff[0])

    assert format(staff) == abjad.String.normalize(
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
        time_signature = abjad.inspect(leaf).get_effective(abjad.TimeSignature)
        assert time_signature is None


def test_scoretools_Inspection_get_effective_20():
    r'''Effective value of arbitrary object.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach('color', staff[1], context='Staff')

    assert abjad.inspect(staff).get_effective(str) is None
    assert abjad.inspect(staff[0]).get_effective(str) is None
    assert abjad.inspect(staff[1]).get_effective(str) == 'color'
    assert abjad.inspect(staff[2]).get_effective(str) == 'color'
    assert abjad.inspect(staff[3]).get_effective(str) == 'color'


def test_scoretools_Inspection_get_effective_21():
    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8")
    abjad.attach('red', staff[0], context='Staff')
    abjad.attach('blue', staff[2], context='Staff')
    abjad.attach('yellow', staff[4], context='Staff')

    assert abjad.inspect(staff[0]).get_effective(str, n=-1) is None
    assert abjad.inspect(staff[0]).get_effective(str, n=0) == 'red'
    assert abjad.inspect(staff[0]).get_effective(str, n=1) is 'blue'

    assert abjad.inspect(staff[1]).get_effective(str, n=-1) is None
    assert abjad.inspect(staff[1]).get_effective(str, n=0) == 'red'
    assert abjad.inspect(staff[1]).get_effective(str, n=1) == 'blue'

    assert abjad.inspect(staff[2]).get_effective(str, n=-1) == 'red'
    assert abjad.inspect(staff[2]).get_effective(str, n=0) == 'blue'
    assert abjad.inspect(staff[2]).get_effective(str, n=1) == 'yellow'

    assert abjad.inspect(staff[3]).get_effective(str, n=-1) == 'red'
    assert abjad.inspect(staff[3]).get_effective(str, n=0) == 'blue'
    assert abjad.inspect(staff[3]).get_effective(str, n=1) == 'yellow'

    assert abjad.inspect(staff[4]).get_effective(str, n=-1) == 'blue'
    assert abjad.inspect(staff[4]).get_effective(str, n=0) == 'yellow'
    assert abjad.inspect(staff[4]).get_effective(str, n=1) is None


def test_scoretools_Inspection_get_effective_22():
    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach('red', staff[-1], context='Staff', synthetic_offset=-1)
    abjad.attach('blue', staff[0], context='Staff')
    assert abjad.inspect(staff).get_effective(str) == 'blue'
    assert abjad.inspect(staff).get_effective(str, n=-1) == 'red'
