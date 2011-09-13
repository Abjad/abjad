from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.octave_number_to_octave_tick_string import octave_number_to_octave_tick_string


def make_n_middle_c_centered_pitches(n):
    '''.. versionadded:: 2.0

    Make `n` middle-c centered pitches, where 0 < `n`::

        abjad> for p in pitchtools.make_n_middle_c_centered_pitches(5): p
        NamedChromaticPitch('f')
        NamedChromaticPitch('a')
        NamedChromaticPitch("c'")
        NamedChromaticPitch("e'")
        NamedChromaticPitch("g'")

    ::

        abjad> for p in pitchtools.make_n_middle_c_centered_pitches(4): p
        NamedChromaticPitch('g')
        NamedChromaticPitch('b')
        NamedChromaticPitch("d'")
        NamedChromaticPitch("f'")

    Return list of zero or more named chromatic pitches.
    '''

    if n == 0:
        return []
    indices = range(0, 2 * abs(n), 2)
    if n < 0:
        indices.reverse()
    average = int(sum(indices) / float(abs(n)))
    centered = [x - average for x in indices]
    letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    tups = [divmod(x, 7) for x in centered]
    pitch_names = [letters[x[1]] + octave_number_to_octave_tick_string(x[0] + 4) for x in tups]
    return [NamedChromaticPitch(x) for x in pitch_names]
