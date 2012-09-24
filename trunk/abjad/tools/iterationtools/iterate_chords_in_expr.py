from abjad.tools import chordtools


def iterate_chords_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Iterate chords forward in `expr`::

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

        >>> for chord in iterationtools.iterate_chords_in_expr(staff):
        ...   chord
        Chord("<e' g' c''>8")
        Chord("<d' f' b'>8")

    Iterate chords backward in `expr`::

    ::

        >>> for chord in iterationtools.iterate_chords_in_expr(staff, reverse=True):
        ...   chord
        Chord("<d' f' b'>8")
        Chord("<e' g' c''>8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr, klass=chordtools.Chord, reverse=reverse, start=start, stop=stop)
