from abjad.tools import componenttools


def iterate_notes_and_chords_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate notes and chords backward in `expr`::

        >>> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    ::

        >>> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            r8
            <d' f' b'>8
            r2
        }

    ::

        >>> for leaf in leaftools.iterate_notes_and_chords_backward_in_expr(staff):
        ...   leaf
        Chord("<d' f' b'>8")
        Note("a'8")
        Chord("<e' g' c''>8")

    Ignore threads.

    Return generator.

    .. versionchanged:: 2.0
        renamed ``pitchtools.iterate_notes_and_chords_backward_in_expr()`` to
        ``leaftools.iterate_notes_and_chords_backward_in_expr()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools

    return componenttools.iterate_components_backward_in_expr(
        expr, (notetools.Note, chordtools.Chord), start=start, stop=stop)
