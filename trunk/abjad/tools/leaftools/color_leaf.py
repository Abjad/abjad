def color_leaf(leaf, color):
    r'''.. versionadded:: 2.0

    Color note::

        abjad> note = Note("c'4")

    ::

        abjad> leaftools.color_leaf(note, 'red')
        Note("c'4")

    ::

        abjad> f(note)
        \once \override Accidental #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        c'4

    Color rest::

        abjad> rest = Rest('r4')

    ::

        abjad> leaftools.color_leaf(rest, 'red')
        Rest('r4')

    ::

        abjad> f(rest)
        \once \override Dots #'color = #red
        \once \override Rest #'color = #red
        r4

    Color chord::

        abjad> chord = Chord("<c' e' bf'>4")

    ::

        abjad> leaftools.color_leaf(chord, 'red')
        Chord("<c' e' bf'>4")

    ::

        abjad> f(chord)
        \once \override Accidental #'color = #red
        \once \override Dots #'color = #red
        \once \override NoteHead #'color = #red
        <c' e' bf'>4

    Return `leaf`.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools.resttools.Rest import Rest

    # color leaf
    if isinstance(leaf, (Note, Chord)):
        leaf.override.accidental.color = color
        leaf.override.dots.color = color
        leaf.override.note_head.color = color
    elif isinstance(leaf, Rest):
        leaf.override.dots.color = color
        leaf.override.rest.color = color

    # return leaf
    return leaf
