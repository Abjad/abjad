# -*- encoding: utf-8 -*-


def make_n_middle_c_centered_pitches(n):
    '''Make `n` middle-c centered pitches, where 0 < `n`:

    ::

        >>> for p in pitchtools.make_n_middle_c_centered_pitches(5): p
        NamedPitch('f')
        NamedPitch('a')
        NamedPitch("c'")
        NamedPitch("e'")
        NamedPitch("g'")

    ::

        >>> for p in pitchtools.make_n_middle_c_centered_pitches(4): p
        NamedPitch('g')
        NamedPitch('b')
        NamedPitch("d'")
        NamedPitch("f'")

    Return list of zero or more named pitches.
    '''
    from abjad.tools import pitchtools

    if n == 0:
        return []
    indices = range(0, 2 * abs(n), 2)
    if n < 0:
        indices.reverse()
    average = int(sum(indices) / float(abs(n)))
    centered = [x - average for x in indices]
    letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    tups = [divmod(x, 7) for x in centered]
    pitch_names = [
        letters[x[1]] + str(pitchtools.OctaveIndication(x[0] + 4)) 
        for x in tups]
    return [pitchtools.NamedPitch(x) for x in pitch_names]
