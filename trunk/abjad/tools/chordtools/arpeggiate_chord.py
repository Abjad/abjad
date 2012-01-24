from abjad.tools.chordtools.Chord import Chord
from abjad.decorators import requires


@requires(Chord)
def arpeggiate_chord(chord):
    '''.. versionadded:: 1.1

    Arpeggiate `chord`::

        abjad> chord = Chord("<c' d'' ef''>8")

    ::

        abjad> chordtools.arpeggiate_chord(chord)
        [Note("c'8"), Note("d''8"), Note("ef''8")]

    Arpeggiated notes inherit `chord` written duration.

    Arpeggiated notes do not inherit other `chord` attributes.

    Return list of newly constructed notes.

    .. versionchanged:: 2.0
        renamed ``chordtools.arpeggiate()`` to
        ``chordtools.arpeggiate_chord()``.
    '''
    from abjad.tools.notetools.Note import Note

    result = []
    chord_written_duration = chord.written_duration
    for pitch in chord.written_pitches:
        result.append(Note(pitch, chord_written_duration))

    return result
