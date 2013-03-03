from abjad.tools import decoratortools
from abjad.tools.chordtools.Chord import Chord


def arpeggiate_chord(chord):
    '''.. versionadded:: 1.1

    Arpeggiate `chord`:

    ::

        >>> chord = Chord("<c' d'' eqf''>8")

    ::

        >>> arpeggio = chordtools.arpeggiate_chord(chord)
        >>> arpeggio
        [Note("c'8"), Note("d''8"), Note("eqf''8")]

    ::

        >>> staff = Staff([chord])
        >>> staff.extend(arpeggio)
        >>> show(staff) # doctest: +SKIP

    Arpeggiated notes inherit `chord` written duration.

    Arpeggiated notes do not inherit other `chord` attributes.

    Return list of newly constructed notes.
    '''
    from abjad.tools import notetools

    result = []
    chord_written_duration = chord.written_duration
    for pitch in chord.written_pitches:
        result.append(notetools.Note(pitch, chord_written_duration))

    return result
