# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___contains___01():
    r'''Closed / closed range.
    '''

    range_ = pitchtools.PitchRange('[A0, C8]')
    assert -99 not in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___02():
    r'''Closed / open range.
    '''

    range_ = pitchtools.PitchRange('[A0, C8)')
    assert -99 not in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 not in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___03():
    r'''Closed / infinite range.
    '''

    #range_ = pitchtools.PitchRange((-39, 'inclusive'), None)
    range_ = pitchtools.PitchRange('[-39, +inf]')
    assert -99 not in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 in range_


def test_pitchtools_PitchRange___contains___04():
    r'''Open / closed range.
    '''

    range_ = pitchtools.PitchRange('(A0, C8]')
    assert -99 not in range_
    assert -39 not in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___05():
    r'''Open / open range.
    '''

    range_ = pitchtools.PitchRange('(-39, 48)')
    assert -99 not in range_
    assert -39 not in range_
    assert 0 in range_
    assert 48 not in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___06():
    r'''Open / infinite range.
    '''

    #range_ = pitchtools.PitchRange((-39, 'exclusive'), None)
    range_ = pitchtools.PitchRange('(-39, +inf]')
    assert -99 not in range_
    assert -39 not in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 in range_


def test_pitchtools_PitchRange___contains___07():
    r'''Infinite / closed range.
    '''

    #range_ = pitchtools.PitchRange(None, (48, 'inclusive'))
    range_ = pitchtools.PitchRange('[-inf, C8]')
    assert -99 in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___08():
    r'''Infinite / open range.
    '''

    #range_ = pitchtools.PitchRange(None, (48, 'exclusive'))
    range_ = pitchtools.PitchRange('[-inf, C8)')
    assert -99 in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 not in range_
    assert 99 not in range_


def test_pitchtools_PitchRange___contains___09():
    r'''Infinite / infinite range.
    '''

    #range_ = pitchtools.PitchRange(None, None)
    range_ = pitchtools.PitchRange('[-inf, +inf]')
    assert -99 in range_
    assert -39 in range_
    assert 0 in range_
    assert 48 in range_
    assert 99 in range_


def test_pitchtools_PitchRange___contains___10():
    r'''Chord containement.
    '''

    #range_ = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
    range_ = pitchtools.PitchRange('[-39, 48]')
    assert Chord([-99, -98, -97], (1, 4)) not in range_
    assert Chord([-39, -38, -37], (1, 4)) in range_
    assert Chord([0, 2, 3], (1, 4)) in range_
    assert Chord([46, 47, 48], (1, 4)) in range_
    assert Chord([48, 49, 50], (1, 4)) not in range_


def test_pitchtools_PitchRange___contains___11():
    r'''Note containement.
    '''

    #range_ = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
    range_ = pitchtools.PitchRange('[-39, 48]')
    assert Note(-99, (1, 4)) not in range_
    assert Note(-39, (1, 4)) in range_
    assert Note(  0, (1, 4)) in range_
    assert Note( 48, (1, 4)) in range_
    assert Note( 99, (1, 4)) not in range_


def test_pitchtools_PitchRange___contains___12():
    r'''Rest and skip containement.
    '''

    #range_ = pitchtools.PitchRange((-39, 'inclusive'), (48, 'inclusive'))
    range_ = pitchtools.PitchRange('[-39, 48]')
    assert Rest((1, 4)) in range_
    assert scoretools.Skip((1, 4)) in range_


def test_pitchtools_PitchRange___contains___13():
    r'''Iterable containment.
    '''

    pitch_numbers = range(10)

    assert pitch_numbers in pitchtools.PitchRange.from_pitches(-39, 48)
    assert not pitch_numbers in pitchtools.PitchRange.from_pitches(36, 48)


def test_pitchtools_PitchRange___contains___14():
    r'''Works with transposed pitches.
    '''

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()
    attach(glockenspiel, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        '''
        )

    assert staff[0] in glockenspiel.pitch_range
    assert staff[1] in glockenspiel.pitch_range
    assert staff in glockenspiel.pitch_range

    assert not Note("c'4") in glockenspiel.pitch_range


def test_pitchtools_PitchRange___contains___15():
    r'''Unpitched notes and chords are evaluated as in-range by definition.
    '''

    staff = Staff("c'4 d'4 c4 d4")
    flute = instrumenttools.Flute()
    attach(flute, staff)
    indicator = indicatortools.IsUnpitched()
    attach(indicator, staff[2])
    attach(indicator, staff[3])
    override(staff[2]).note_head.style = 'cross'
    override(staff[3]).note_head.style = 'cross'

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'4
            d'4
            \once \override NoteHead.style = #'cross
            c4
            \once \override NoteHead.style = #'cross
            d4
        }
        '''
        )

    assert staff in flute.pitch_range
