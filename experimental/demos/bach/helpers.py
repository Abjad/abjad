import abjad
from experimental.demos.bach.chorale import es_ist_genug


def build_chorale():

    soprano = abjad.parse(r'\new Voice = "soprano" {{ {} }}'.format(
        es_ist_genug['soprano']))
    alto = abjad.parse(r'\new Voice = "alto" {{ {} }}'.format(
        es_ist_genug['alto']))
    tenor = abjad.parse(r'\new Voice = "tenor" {{ {} }}'.format(
        es_ist_genug['tenor']))
    bass = abjad.parse(r'\new Voice = "bass" {{ {} }}'.format(
        es_ist_genug['bass']))

    treble_staff = abjad.Staff([soprano, alto])
    bass_staff = abjad.Staff([tenor, bass])

    treble_staff.is_simultaneous = True
    bass_staff.is_simultaneous = True

    key_signature = abjad.KeySignature(*es_ist_genug['key'])
    #abjad.attach(key_signature, treble_staff)
    key_signature = abjad.KeySignature(*es_ist_genug['key'])
    #abjad.attach(key_signature, bass_staff)
    clef = abjad.Clef('bass')
    #abjad.attach(clef, bass_staff)

    bar_line = abjad.BarLine('|.')
    #attach(bar_line, treble_staff)
    bar_line = abjad.BarLine('|.')
    #abjad.attach(bar_line, bass_staff)

    staff_group = abjad.StaffGroup([treble_staff, bass_staff])
    staff_group.context_name = 'PianoStaff'

    return staff_group
