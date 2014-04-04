from abjad import *
from experimental.demos.bach.chorale import es_ist_genug


def build_chorale():

    soprano = parse(r'\new Voice = "soprano" {{ {} }}'.format(es_ist_genug['soprano']))
    alto =    parse(r'\new Voice = "alto" {{ {} }}'.format(es_ist_genug['alto']))
    tenor =   parse(r'\new Voice = "tenor" {{ {} }}'.format(es_ist_genug['tenor']))
    bass =    parse(r'\new Voice = "bass" {{ {} }}'.format(es_ist_genug['bass']))

    treble_staff = Staff([soprano, alto])
    bass_staff = Staff([tenor, bass])

    treble_staff.is_simultaneous = True
    bass_staff.is_simultaneous = True

    key_signature = KeySignature(*es_ist_genug['key'])
    attach(key_signature, treble_staff)
    key_signature = KeySignature(*es_ist_genug['key'])
    attach(key_signature, bass_staff)
    clef = indicatortools.Clef('bass')
    attach(clef, bass_staff)

    bar_line = indicatortools.BarLine('|.')
    attach(bar_line, treble_staff)
    bar_line = indicatortools.BarLine('|.')
    attach(bar_line, bass_staff)

    staff_group = StaffGroup([treble_staff, bass_staff])
    staff_group.context_name = 'PianoStaff'

    return staff_group