from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools import resttools


def color_leaf(leaf, color):
    r'''.. versionadded:: 2.0

    Color note::

        >>> note = Note("c'4")

    ::

        >>> labeltools.color_leaf(note, 'red')
        Note("c'4")

    ::

        >>> f(note)
        \once \override Accidental #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        c'4

    Color rest::

        >>> rest = Rest('r4')

    ::

        >>> labeltools.color_leaf(rest, 'red')
        Rest('r4')

    ::

        >>> f(rest)
        \once \override Dots #'color = #red
        \once \override Rest #'color = #red
        r4

    Color chord::

        >>> chord = Chord("<c' e' bf'>4")

    ::

        >>> labeltools.color_leaf(chord, 'red')
        Chord("<c' e' bf'>4")

    ::

        >>> f(chord)
        \once \override Accidental #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        <c' e' bf'>4

    Return `leaf`.
    '''

    # color leaf
    if isinstance(leaf, (notetools.Note, chordtools.Chord)):
        leaf.override.accidental.color = color
        leaf.override.dots.color = color
        leaf.override.note_head.color = color
    elif isinstance(leaf, resttools.Rest):
        leaf.override.dots.color = color
        leaf.override.rest.color = color

    # return leaf
    return leaf
