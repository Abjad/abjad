from abjad.tools import sequencetools


def list_inversion_equivalent_chromatic_interval_classes_pairwise(pitch_carriers, wrap=False):
    r'''.. versionadded:: 2.0

    List inversion-equivalent chromatic interval-classes pairwise between `pitch_carriers`::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    ::

        >>> f(staff)
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

        >>> result = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise(
        ... staff, wrap=False)
        
    ::

        >>> for x in result: x
        ...
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)

    ::

        >>> result = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise(
        ... staff, wrap=True)

    ::

        >>> for x in result: x
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(0)

    ::

        >>> notes = staff.leaves
        >>> notes = list(reversed(notes))

    ::

        >>> result = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise(
        ... notes, wrap=False)

    ::

        >>> for x in result: x
        ...
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)

    ::

        >>> result = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise(
        ... notes, wrap=True)

    ::

        >>> for x in result: x
        ...
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(2)
        InversionEquivalentChromaticIntervalClass(0)

    When ``wrap=False`` do not return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    When ``wrap=True`` do return ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

    Return list.
    '''
    from abjad.tools import pitchtools

    result = []

    if len(pitch_carriers) == 0:
        return result
    elif len(pitch_carriers) == 1:
        if pitchtools.is_pitch_carrier(pitch_carriers[0]):
            return result
        else:
            raise TypeError('must be Abjad pitch, note, note head or chord.')

    if wrap:
        pairs = sequencetools.iterate_sequence_pairwise_wrapped(pitch_carriers)
    else:
        pairs = sequencetools.iterate_sequence_pairwise_strict(pitch_carriers)

    for first_carrier, second_carrier in pairs:
        first_pitch = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(first_carrier)
        second_pitch = pitchtools.get_named_chromatic_pitch_from_pitch_carrier(second_carrier)
        mdi = second_pitch - first_pitch
        iecic = mdi.inversion_equivalent_chromatic_interval_class
        result.append(iecic)

    return result
