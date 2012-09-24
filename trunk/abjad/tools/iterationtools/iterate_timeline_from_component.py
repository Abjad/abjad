from abjad.tools import componenttools
from abjad.tools import leaftools


def iterate_timeline_from_component(expr, klass=None, reverse=False):
    r'''.. versionadded:: 2.10

    Iterate timeline forward from `component`::

        >>> score = Score([])
        >>> score.append(Staff(notetools.make_repeated_notes(4, Duration(1, 4))))
        >>> score.append(Staff(notetools.make_repeated_notes(4)))
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(score)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>

    ::

        >>> for leaf in iterationtools.iterate_timeline_from_component(score[1][2]):
        ...     leaf
        ...
        Note("b'8")
        Note("c''8")
        Note("e'4")
        Note("f'4")

    Iterate timeline backward from `component`::

    ::

        >>> for leaf in iterationtools.iterate_timeline_from_component(score[1][2], reverse=True):
        ...     leaf
        ...
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Yield components sorted backward by score offset stop time when `reverse` is True.

    Iterate leaves when `klass` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools import iterationtools

    if klass is None:
        klass = leaftools.Leaf

    root = componenttools.component_to_score_root(expr)
    component_generator = iterationtools.iterate_timeline_in_expr(
        root, klass=klass, reverse=reverse)

    yielded_expr = False
    for component in component_generator:
        if yielded_expr:
            yield component
        elif component is expr:
            yield component
            yielded_expr = True
