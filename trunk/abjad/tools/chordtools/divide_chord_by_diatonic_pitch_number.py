from abjad.tools import decoratortools
from abjad.tools import pitchtools
from abjad.tools.chordtools.Chord import Chord


# TODO: remove in favor of chordtools.divide_chord()
@decoratortools.requires(Chord, pitchtools.NamedChromaticPitch)
def divide_chord_by_diatonic_pitch_number(chord, pitch=None):
    r'''.. versionadded:: 1.1

    Divide `chord` by diatonic `pitch` number:

    ::

        >>> chord = Chord(range(12), Duration(1, 4))
        >>> pitch = pitchtools.NamedChromaticPitch("fs'")

    ::

        >>> chord
        Chord("<c' cs' d' ef' e' f' fs' g' af' a' bf' b'>4")

    ::

        >>> pitch
        NamedChromaticPitch("fs'")

    ::

        >>> chordtools.divide_chord_by_diatonic_pitch_number(chord, pitch)
        (Chord("<f' fs' g' af' a' bf' b'>4"), Chord("<c' cs' d' ef' e'>4"))

    Function interprets none-valued `pitch` as ``B3``.

    Input `chord` may be a note, rest or chord but not a skip.

    Zero-length parts return as rests, length-one parts return as notes and
    other parts return as chords.

    Return pair of newly constructed leaves.
    '''
    from abjad.tools import chordtools

    pitch = pitch or pitchtools.NamedChromaticPitch('b', 3)

    treble_chord, bass_chord = chordtools.divide_chord(
        chord, pitch=pitch, attr='numbered_diatonic_pitch')

    return treble_chord, bass_chord
