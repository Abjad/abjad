from abjad.tools import componenttools


def iterate_notes_and_chords_forward_in_expr(expr, start = 0, stop = None):
    r'''.. versionadded:: 2.0

    Iterate notes and chords forward in `expr`::

        abjad> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    ::

        abjad> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            r8
            <d' f' b'>8
            r2
        }

    ::

        abjad> for leaf in leaftools.iterate_notes_and_chords_forward_in_expr(staff):
        ...   leaf
        Chord("<e' g' c''>8")
        Note("a'8")
        Chord("<d' f' b'>8")

    Ignore threads.

    Return generator.

    .. versionchanged:: 2.0
        renamed ``pitchtools.iterate_notes_and_chords_forward_in_expr()`` to
        ``leaftools.iterate_notes_and_chords_forward_in_expr()``.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note

    return componenttools.iterate_components_forward_in_expr(
        expr, (Note, Chord), start = start, stop = stop)
