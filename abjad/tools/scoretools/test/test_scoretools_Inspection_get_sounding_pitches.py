import abjad


def test_scoretools_Inspection_get_sounding_pitches_01():

    staff = abjad.Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = abjad.instrumenttools.Glockenspiel()
    abjad.attach(glockenspiel, staff[0])
    abjad.Instrument.transpose_from_sounding_pitch(staff)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        '''
        )

    sounding_pitches = abjad.inspect(staff[0]).get_sounding_pitches()
    assert sounding_pitches == (
        abjad.NamedPitch("c'''"),
        abjad.NamedPitch("e'''"),
        )
