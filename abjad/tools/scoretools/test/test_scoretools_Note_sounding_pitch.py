# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Note_sounding_pitch_01():


    staff = Staff("d''8 e''8 f''8 g''8")
    piccolo = instrumenttools.Piccolo()
    attach(piccolo, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert systemtools.TestManager.compare(
        staff,
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

    assert inspect(staff[0]).get_sounding_pitch() == "d''"
    assert inspect(staff[1]).get_sounding_pitch() == "e''"
    assert inspect(staff[2]).get_sounding_pitch() == "f''"
    assert inspect(staff[3]).get_sounding_pitch() == "g''"
