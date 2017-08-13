import abjad


def test_scoretools_Note_sounding_pitch_01():


    staff = abjad.Staff("d''8 e''8 f''8 g''8")
    piccolo = abjad.instrumenttools.Piccolo()
    abjad.attach(piccolo, staff[0])
    abjad.Instrument.transpose_from_sounding_pitch(staff)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            d'8
            e'8
            f'8
            g'8
        }
        '''
        )

    assert abjad.inspect(staff[0]).get_sounding_pitch() == "d''"
    assert abjad.inspect(staff[1]).get_sounding_pitch() == "e''"
    assert abjad.inspect(staff[2]).get_sounding_pitch() == "f''"
    assert abjad.inspect(staff[3]).get_sounding_pitch() == "g''"
