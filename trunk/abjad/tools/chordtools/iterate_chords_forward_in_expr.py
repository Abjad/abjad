def iterate_chords_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``chordtools.iterate_chords_in_expr()`` instead.

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

        >>> for chord in chordtools.iterate_chords_forward_in_expr(staff):
        ...   chord
        Chord("<e' g' c''>8")
        Chord("<d' f' b'>8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import chordtools

    return chordtools.iterate_chords_in_expr(
        expr, start=start, stop=stop)
