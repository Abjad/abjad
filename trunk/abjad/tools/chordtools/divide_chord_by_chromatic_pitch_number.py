from abjad.tools import decoratortools
from abjad.tools import leaftools
from abjad.tools import pitchtools


@decoratortools.requires(
    leaftools.Leaf,
    pitchtools.is_named_chromatic_pitch_token,
    )
def divide_chord_by_chromatic_pitch_number(chord, pitch=None):
    r'''.. versionadded:: 1.1

    Divide `chord` by chromatic `pitch` number:

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

        >>> chordtools.divide_chord_by_chromatic_pitch_number(chord, pitch)
        (Chord("<fs' g' af' a' bf' b'>4"), Chord("<c' cs' d' ef' e' f'>4"))

    Function interprets `pitch` equals to none 
    as pitch equal to ``B3``.

    Input `chord` may be a note, rest or chord but not a skip.

    Zero-length parts return rests, length-one parts return notes and
    other parts return chords.

    Return pair of newly constructed leaves.
    '''
    from abjad.tools.chordtools._divide_chord import _divide_chord

    pitch = pitch or pitchtools.NamedChromaticPitch('b', 3)

    treble_chord, bass_chord = _divide_chord(
        chord, pitch=pitch, attr='numbered_chromatic_pitch')

    return treble_chord, bass_chord
