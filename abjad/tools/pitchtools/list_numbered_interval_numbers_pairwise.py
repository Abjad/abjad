# -*- coding: utf-8 -*-
from abjad.tools import sequencetools


def list_numbered_interval_numbers_pairwise(pitch_carriers, wrap=False):
    r'''Lists numbered interval numbers pairwise between `pitch_carriers`.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    ..  doctest::

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

        >>> pitchtools.list_numbered_interval_numbers_pairwise(staff[:])
        [2, 2, 1, 2, 2, 2, 1]

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... staff[:], wrap=True)
        [2, 2, 1, 2, 2, 2, 1, -12]

    ::

        >>> notes = [
        ...     Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"),
        ...     Note("g'8"), Note("a'8"), Note("b'8"), Note("c''8"),
        ...     ]

    ::

        >>> notes.reverse()

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(notes)
        [-1, -2, -2, -2, -1, -2, -2]

    ::

        >>> pitchtools.list_numbered_interval_numbers_pairwise(
        ... notes, wrap=True)
        [-1, -2, -2, -2, -1, -2, -2, 12]

    When ``wrap = False`` do not return
    ``pitch_carriers[-1] - pitch_carriers[0]`` as last in series.

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

    pairs = sequencetools.iterate_sequence_nwise(pitch_carriers, wrapped=wrap)
    pairs = list(pairs)

    for first_carrier, second_carrier in pairs:
        first_pitch = pitchtools.NamedPitch.from_pitch_carrier(first_carrier)
        second_pitch = pitchtools.NamedPitch.from_pitch_carrier(second_carrier)
        signed_interval = \
            pitchtools.NumberedPitch(second_pitch).pitch_number - \
            pitchtools.NumberedPitch(first_pitch).pitch_number
        result.append(signed_interval)

    return result