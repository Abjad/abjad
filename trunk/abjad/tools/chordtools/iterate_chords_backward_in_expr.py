from abjad.tools import componenttools
from abjad.tools import decoratortools


@decoratortools.requires(object)
def iterate_chords_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate chords backward in `expr`::

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

        >>> for chord in chordtools.iterate_chords_backward_in_expr(staff):
        ...   chord
        Chord("<d' f' b'>8")
        Chord("<e' g' c''>8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import chordtools

    return componenttools.iterate_components_backward_in_expr(
        expr, chordtools.Chord, start=start, stop=stop)
