# -*- encoding: utf-8 -*-
import copy


# TODO: Reimplement to work on Abjad PitchSet, Note and Chord objects only.
# TODO: Reimplement to work with diatonic transposition. #
def list_octave_transpositions_of_pitch_carrier_within_pitch_range(pitch_carrier, pitch_range):
    r"""List octave transpositions of `pitch_carrier` in `pitch_range`:

    ::

        >>> chord = Chord("<c' d' e'>4")
        >>> pitch_range = pitchtools.PitchRange(0, 48)

    ::

        >>> result = pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range(
        ...     chord, pitch_range)

    ::

        >>> for chord in result:
        ...     chord
        ...
        Chord("<c' d' e'>4")
        Chord("<c'' d'' e''>4")
        Chord("<c''' d''' e'''>4")
        Chord("<c'''' d'''' e''''>4")

    Returns list of newly created `pitch_carrier` objects.
    """
    from abjad.tools import scoretools
    from abjad.tools import pitchtools

    if not isinstance(pitch_range, pitchtools.PitchRange):
        raise TypeError('must be pitch range.')

    if all(isinstance(x, (int, long, float)) for x in pitch_carrier):
        return _pitch_number_list_octave_transpositions(pitch_carrier, pitch_range)

    if not isinstance(pitch_carrier, (scoretools.Chord, pitchtools.PitchSet)):
        raise TypeError('must be chord or pitch set.')

    result = []

    interval = pitchtools.NumberedInterval(-12)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = pitchtools.transpose_pitch_carrier_by_interval(pitch_carrier_copy, interval)
        if candidate in pitch_range:
            result.append(candidate)
            interval -= pitchtools.NumberedInterval(12)
        else:
            break

    result.reverse()

    interval = pitchtools.NumberedInterval(0)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = pitchtools.transpose_pitch_carrier_by_interval(pitch_carrier_copy, interval)
        if candidate in pitch_range:
            result.append(candidate)
            interval += pitchtools.NumberedInterval(12)
        else:
            break

    return result


# TODO: make public
def _pitch_number_list_octave_transpositions(pitch_number_list, pitch_range):
    result = []
    ps = set(pitch_number_list)
    start_pitch_number = pitch_range.start_pitch.pitch_number
    stop_pitch_number = pitch_range.stop_pitch.pitch_number
    R = set(range(start_pitch_number, stop_pitch_number + 1))
    while ps.issubset(R):
        next_pitch_number = list(ps)
        next_pitch_number.sort()
        result.extend([next_pitch_number])
        ps = set([p + 12 for p in ps])

    ps = set([p - 12 for p in pitch_number_list])
    while ps.issubset(R):
        next_pitch_number = list(ps)
        next_pitch_number.sort()
        result.extend([next_pitch_number])
        ps = set([p - 12 for p in ps])

    result.sort()
    return result
