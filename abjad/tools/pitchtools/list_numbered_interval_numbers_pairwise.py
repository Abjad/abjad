# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


def list_numbered_interval_numbers_pairwise(pitch_carriers, wrap=False):
    r'''List numbered interval numbers pairwise between `pitch_carriers`:

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

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... staff)
        [2, 2, 1, 2, 2, 2, 1]

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... staff, wrap=True)
        [2, 2, 1, 2, 2, 2, 1, -12]

    ::

        >>> notes = [
        ...     Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"),
        ...     Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8")]

    ::

        >>> notes.reverse()

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... notes)
        [-1, -2, -2, -2, -1, -2, -2]

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... notes, wrap=True)
        [-1, -2, -2, -2, -1, -2, -2, 12]

    When ``wrap = False`` do not return ``pitch_carriers[-1] - pitch_carriers[0]``
    as last in series.

    When ``wrap = True`` do return ``pitch_carriers[-1] - pitch_carriers[0]``
    as last in series.

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
            message = 'must be pitch, not, note-head or chord.'
            raise TypeError(message)

    if wrap:
        pairs = sequencetools.iterate_sequence_pairwise_wrapped(pitch_carriers)
    else:
        pairs = sequencetools.iterate_sequence_pairwise_strict(pitch_carriers)

    for first_carrier, second_carrier in pairs:
        first_pitch = pitchtools.get_named_pitch_from_pitch_carrier(first_carrier)
        second_pitch = pitchtools.get_named_pitch_from_pitch_carrier(second_carrier)
        signed_interval = abs(pitchtools.NumberedPitch(second_pitch)) - \
            abs(pitchtools.NumberedPitch(first_pitch))
        result.append(signed_interval)

    return result
