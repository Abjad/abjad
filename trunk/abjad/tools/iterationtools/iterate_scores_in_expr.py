# -*- encoding: utf-8 -*-
from abjad.tools import scoretools


def iterate_scores_in_expr(expr, reverse=False, start=0, stop=None):
    '''Iterate scores forward in `expr`:

    ::

        >>> score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
        >>> score_2 = Score([Staff("c'1"), Staff("g'1")])
        >>> scores = [score_1, score_2]

    ::

        >>> for score in iterationtools.iterate_scores_in_expr(scores):
        ...   score
        Score<<1>>
        Score<<2>>

    Iterate scores backward in `expr`:

    ::

    ::

        >>> for score in iterationtools.iterate_scores_in_expr(scores, reverse=True):
        ...   score
        Score<<2>>
        Score<<1>>

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr,
        component_class=scoretools.Score,
        reverse=reverse,
        start=start,
        stop=stop,
        )
