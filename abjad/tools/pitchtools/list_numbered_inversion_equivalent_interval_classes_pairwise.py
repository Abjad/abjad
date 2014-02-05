# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


def list_numbered_inversion_equivalent_interval_classes_pairwise(pitch_carriers, wrap=False):
    r'''List numbered inversion-equivalent interval-classes pairwise between
    `pitch_carriers`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    ..  doctest::

        >>> print format(staff)
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

        >>> result = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        ... staff, wrap=False)

    ::

        >>> for x in result: x
        ...
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)

    ::

        >>> result = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        ... staff, wrap=True)

    ::

        >>> for x in result: x
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(0)

    ::

        >>> notes = staff.select_leaves()
        >>> notes = list(reversed(notes))

    ::

        >>> result = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        ... notes, wrap=False)

    ::

        >>> for x in result: x
        ...
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)

    ::

        >>> result = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        ... notes, wrap=True)

    ::

        >>> for x in result: x
        ...
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(2)
        NumberedInversionEquivalentIntervalClass(0)

    When ``wrap=False`` do not return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    When ``wrap=True`` do return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    Returns list.
    '''
    from abjad.tools import pitchtools

    result = []

    if len(pitch_carriers) == 0:
        return result
    elif len(pitch_carriers) == 1:
        if pitchtools.Pitch.is_pitch_carrier(pitch_carriers[0]):
            return result
        else:
            message = 'must be pitch, note, note-head or chord.'
            raise TypeError(message)

    if wrap:
        pairs = sequencetools.iterate_sequence_nwise_wrapped(pitch_carriers)
    else:
        pairs = sequencetools.iterate_sequence_nwise_strict(pitch_carriers)

    for first_carrier, second_carrier in pairs:
        first_pitch = pitchtools.get_named_pitch_from_pitch_carrier(first_carrier)
        second_pitch = pitchtools.get_named_pitch_from_pitch_carrier(second_carrier)
        mdi = second_pitch - first_pitch
        iecic = pitchtools.NumberedInversionEquivalentIntervalClass(mdi)
        result.append(iecic)

    return result
