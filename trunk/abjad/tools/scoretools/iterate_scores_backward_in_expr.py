from abjad.tools import componenttools


def iterate_scores_backward_in_expr(expr, start=0, stop=None):
    '''.. versionadded:: 2.0

    Iterate scores backward in `expr`::

        >>> score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
        >>> score_2 = Score([Staff("c'1"), Staff("g'1")])
        >>> scores = [score_1, score_2]

    ::

        >>> for score in scoretools.iterate_scores_backward_in_expr(scores):
        ...   score
        Score<<2>>
        Score<<1>>

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import scoretools

    return componenttools.iterate_components_backward_in_expr(
        expr, scoretools.Score, start=start, stop=stop)
