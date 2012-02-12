from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet
from abjad.tools.pitchtools.PitchRange import PitchRange
from abjad.tools.pitchtools.transpose_pitch_carrier_by_melodic_interval import transpose_pitch_carrier_by_melodic_interval
import copy


# TODO: Reimplement pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range() to work on Abjad PitchSet, Note and Chord objects only. #

# TODO: Reimplement pitchtools.octave_transposition() with diatonic transposition. #

def list_octave_transpositions_of_pitch_carrier_within_pitch_range(pitch_carrier, pitch_range):
    r""".. versionadded:: 1.1

    List octave transpositions of `pitch_carrier` in `pitch_range`::

        abjad> chord = Chord([0, 2, 4], (1, 4))
        abjad> pitch_range = pitchtools.PitchRange(0, 48)
        abjad> pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range(chord, pitch_range)
        [Chord("<c' d' e'>4"), Chord("<c'' d'' e''>4"), Chord("<c''' d''' e'''>4"), Chord("<c'''' d'''' e''''>4")]

    Return list of newly created `pitch_carrier` objects.
    """
    from abjad.tools.chordtools.Chord import Chord

    if not isinstance(pitch_range, PitchRange):
        raise TypeError('must be pitch range.')

    if all([isinstance(x, (int, long, float)) for x in pitch_carrier]):
        return _pitch_number_list_octave_transpositions(pitch_carrier, pitch_range)

    if not isinstance(pitch_carrier, (Chord, NamedChromaticPitchSet)):
        raise TypeError('must be chord or named chromatic pitch set.')

    result = []

    interval = MelodicChromaticInterval(-12)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = transpose_pitch_carrier_by_melodic_interval(pitch_carrier_copy, interval)
        if candidate in pitch_range:
            result.append(candidate)
            interval -= MelodicChromaticInterval(12)
        else:
            break

    result.reverse()

    interval = MelodicChromaticInterval(0)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = transpose_pitch_carrier_by_melodic_interval(pitch_carrier_copy, interval)
        if candidate in pitch_range:
            result.append(candidate)
            interval += MelodicChromaticInterval(12)
        else:
            break

    return result


def _pitch_number_list_octave_transpositions(pitch_number_list, pitch_range):
    result = []
    ps = set(pitch_number_list)
    start_pitch_number = abs(pitch_range.start_pitch.numbered_chromatic_pitch)
    stop_pitch_number = abs(pitch_range.stop_pitch.numbered_chromatic_pitch)
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
