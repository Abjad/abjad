# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import override


def color_leaf(leaf, color):
    r'''Color note:

    ::

        >>> note = Note("c'4")

    ::

        >>> labeltools.color_leaf(note, 'red')
        Note("c'4")

    ..  doctest::

        >>> f(note)
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        c'4

    ::

        >>> show(note) # doctest: +SKIP

    Color rest:

    ::

        >>> rest = Rest('r4')

    ::

        >>> labeltools.color_leaf(rest, 'red')
        Rest('r4')

    ..  doctest::

        >>> f(rest)
        \once \override Dots #'color = #red
        \once \override Rest #'color = #red
        r4

    ::

        >>> show(rest) # doctest: +SKIP

    Color chord:

    ::

        >>> chord = Chord("<c' e' bf'>4")

    ::

        >>> labeltools.color_leaf(chord, 'red')
        Chord("<c' e' bf'>4")

    ..  doctest::

        >>> f(chord)
        \once \override Accidental #'color = #red
        \once \override Beam #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        \once \override Stem #'color = #red
        <c' e' bf'>4

    ::

        >>> show(chord) # doctest: +SKIP

    Return `leaf`.
    '''

    # color leaf
    if isinstance(leaf, (scoretools.Note, scoretools.Chord)):
        override(leaf).accidental.color = color
        override(leaf).beam.color = color
        override(leaf).dots.color = color
        override(leaf).note_head.color = color
        override(leaf).stem.color = color
    elif isinstance(leaf, scoretools.Rest):
        override(leaf).dots.color = color
        override(leaf).rest.color = color

    # return leaf
    return leaf
