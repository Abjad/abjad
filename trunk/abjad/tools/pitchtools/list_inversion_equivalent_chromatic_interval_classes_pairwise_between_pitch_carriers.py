from abjad.tools import sequencetools
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.pitchtools.is_pitch_carrier import is_pitch_carrier


def list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(
    pitch_carriers, wrap = False):
    r'''.. versionadded:: 2.0

    List inversion-equivalent chromatic interval-classes pairwise between `pitch_carriers`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }

    ::

        abjad> pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(staff, wrap = False)
        [InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(1),
        InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(1)]

    ::

        abjad> pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(staff, wrap = True)
        [InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(1),
        InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(1), InversionEquivalentChromaticIntervalClass(0)]


    ::

        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")]
        abjad> notes.reverse()
        abjad> notes
        [Note("c''8"), Note("b'8"), Note("a'8"), Note("g'8"), Note("f'8"), Note("e'8"), Note("d'8"), Note("c'8")]

    ::

        abjad> pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(notes, wrap = False)
        [InversionEquivalentChromaticIntervalClass(1), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(1), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(2)]

    ::

        abjad> pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(notes, wrap = True)
        [InversionEquivalentChromaticIntervalClass(1), InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(1), InversionEquivalentChromaticIntervalClass(2),
        InversionEquivalentChromaticIntervalClass(2), InversionEquivalentChromaticIntervalClass(0)]

    When ``wrap = False`` do not return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    When ``wrap = True`` do return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    Return list.
    '''

    result = []

    if len(pitch_carriers) == 0:
        return result
    elif len(pitch_carriers) == 1:
        if is_pitch_carrier(pitch_carriers[0]):
            return result
        else:
            raise TypeError('must be Abjad Pitch, Note, NoteHead or Chord.')

    if wrap:
        pairs = sequencetools.iterate_sequence_pairwise_wrapped(pitch_carriers)
    else:
        pairs = sequencetools.iterate_sequence_pairwise_strict(pitch_carriers)

    for first_carrier, second_carrier in pairs:
        first_pitch = get_named_chromatic_pitch_from_pitch_carrier(first_carrier)
        second_pitch = get_named_chromatic_pitch_from_pitch_carrier(second_carrier)
        #signed_interval = abs(second_pitch.numbered_chromatic_pitch) - \
        #   abs(first_pitch.numbered_chromatic_pitch)
        #result.append(signed_interval)
        mdi = second_pitch - first_pitch
        iecic = mdi.inversion_equivalent_chromatic_interval_class
        result.append(iecic)

    return result
