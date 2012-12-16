from abjad import *
from abjad.demos.bach.chorale import es_ist_genug


def build_chorale():

    soprano = p(r'\new Voice = "soprano" {{ {} }}'.format(es_ist_genug['soprano']))
    alto =    p(r'\new Voice = "alto" {{ {} }}'.format(es_ist_genug['alto']))
    tenor =   p(r'\new Voice = "tenor" {{ {} }}'.format(es_ist_genug['tenor']))
    bass =    p(r'\new Voice = "bass" {{ {} }}'.format(es_ist_genug['bass']))

    treble_staff = Staff([soprano, alto])
    bass_staff = Staff([tenor, bass])

    treble_staff.is_parallel = True
    bass_staff.is_parallel = True

    contexttools.KeySignatureMark(*es_ist_genug['key'])(treble_staff)
    contexttools.KeySignatureMark(*es_ist_genug['key'])(bass_staff)
    contexttools.ClefMark('bass')(bass_staff)

    marktools.BarLine('|.')(treble_staff)
    marktools.BarLine('|.')(bass_staff)

    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])

    return piano_staff
