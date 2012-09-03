from abjad.tools import decoratortools
from abjad.tools import leaftools
from abjad.tools import pitchtools


@decoratortools.requires(leaftools.Leaf, pitchtools.is_named_chromatic_pitch_token)
def divide_chord_by_chromatic_pitch_number(chord, pitch=pitchtools.NamedChromaticPitch('b', 3)):
    r'''.. versionadded:: 1.1

    Divide `chord` by chromatic `pitch` number::

        >>> chord = Chord(range(12), Duration(1, 4))

    ::

        >>> chord
        Chord("<c' cs' d' ef' e' f' fs' g' af' a' bf' b'>4")

    ::

        >>> chordtools.divide_chord_by_chromatic_pitch_number(chord, pitchtools.NamedChromaticPitch(6))
        (Chord("<fs' g' af' a' bf' b'>4"), Chord("<c' cs' d' ef' e' f'>4"))

    Input `chord` may be a note, rest or chord but not a skip.

    Zero-length parts return rests, length-one parts return notes and
    other parts return chords.

    Return pair of newly constructed leaves.

    .. versionchanged:: 2.0
        renamed ``chordtools.split_by_pitch_number()`` to
        ``chordtools.divide_chord_by_chromatic_pitch_number()``.
    '''
    from abjad.tools.chordtools._divide_chord import _divide_chord

    treble_chord, bass_chord = _divide_chord(chord, pitch=pitch, attr='numbered_chromatic_pitch')

    return treble_chord, bass_chord
