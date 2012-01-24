from abjad.tools.chordtools._divide_chord import _divide_chord
from abjad.tools.chordtools.Chord import Chord
from abjad.decorators import requires
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


@requires(Chord, NamedChromaticPitch)
def divide_chord_by_diatonic_pitch_number(chord, pitch=NamedChromaticPitch('b', 3)):
    r'''.. versionadded:: 1.1

    Divide `chord` by diatonic `pitch` number::

        abjad> chord = Chord(range(12), Duration(1, 4))

    ::

        abjad> chord
        Chord("<c' cs' d' ef' e' f' fs' g' af' a' bf' b'>4")

    ::

        abjad> chordtools.divide_chord_by_diatonic_pitch_number(chord, pitchtools.NamedChromaticPitch(6))
        (Chord("<f' fs' g' af' a' bf' b'>4"), Chord("<c' cs' d' ef' e'>4"))

    Input `chord` may be a note, rest or chord but not a skip.

    Zero-length parts return as rests, length-one parts return as notes and
    other parts return as chords.

    Return pair of newly constructed leaves.

    .. versionchanged:: 2.0
        renamed ``chordtools.split_by_altitude()`` to
        ``chordtools.divide_chord_by_diatonic_pitch_number()``.
    '''

    treble_chord, bass_chord = _divide_chord(chord, pitch = pitch, attr = 'numbered_diatonic_pitch')

    return treble_chord, bass_chord
