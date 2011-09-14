from abjad import *
from abjad.demos.bach.chorale import es_ist_genug


def build_chorale():

    soprano = Voice(iotools.parse_lilypond_input_string(es_ist_genug['soprano'])[:])
    alto = Voice(iotools.parse_lilypond_input_string(es_ist_genug['alto'])[:])
    tenor = Voice(iotools.parse_lilypond_input_string(es_ist_genug['tenor'])[:])
    bass = Voice(iotools.parse_lilypond_input_string(es_ist_genug['bass'])[:])

    treble_staff = Staff([soprano, alto])
    bass_staff = Staff([tenor, bass])

    treble_staff.is_parallel = True
    bass_staff.is_parallel = True

    contexttools.KeySignatureMark(*es_ist_genug['key'])(treble_staff)
    contexttools.KeySignatureMark(*es_ist_genug['key'])(bass_staff)
    contexttools.ClefMark('bass')(bass_staff)

    marktools.Barline('|.')(treble_staff)
    marktools.Barline('|.')(bass_staff)

    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])

    return paino_staff
