from abjad.tools import decoratortools
from abjad.tools import leaftools


@decoratortools.requires(leaftools.Leaf)
def change_defective_chord_to_note_or_rest(chord):
    '''.. versionadded:: 1.1

    Change zero-length `chord` to rest::

        >>> chord = Chord([], (3, 16))

    ::

        >>> chord
        Chord('<>8.')

    ::

        >>> chordtools.change_defective_chord_to_note_or_rest(chord)
        Rest('r8.')

    Change length-one chord to note::

        >>> chord = Chord("<cs''>8.")

    ::

        >>> chord
        Chord("<cs''>8.")

    ::

        >>> chordtools.change_defective_chord_to_note_or_rest(chord)
        Note("cs''8.")

    Return chords with length greater than one unchanged::

        >>> chord = Chord("<c' c'' cs''>8.")

    ::

        >>> chord
        Chord("<c' c'' cs''>8.")

    ::

        >>> chordtools.change_defective_chord_to_note_or_rest(chord)
        Chord("<c' c'' cs''>8.")

    Return notes unchanged::

        >>> note = Note("c'4")

    ::

        >>> note
        Note("c'4")

    ::

        >>> chordtools.change_defective_chord_to_note_or_rest(note)
        Note("c'4")

    Return rests unchanged::

        >>> rest = Rest('r4')

    ::

        >>> rest
        Rest('r4')

    ::

        >>> chordtools.change_defective_chord_to_note_or_rest(rest)
        Rest('r4')

    Return note, rest, chord or none.

    .. versionchanged:: 2.0
        renamed ``chordtools.cast_defective()`` to
        ``chordtools.change_defective_chord_to_note_or_rest()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import resttools

    if isinstance(chord, chordtools.Chord):
        if len(chord) == 0:
            return resttools.Rest(chord)
        elif len(chord) == 1:
            return notetools.Note(chord)

    return chord
