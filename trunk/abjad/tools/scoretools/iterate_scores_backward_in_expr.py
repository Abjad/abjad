from abjad.tools.scoretools.Score import Score
from abjad.tools import componenttools


def iterate_scores_backward_in_expr(expr, start = 0, stop = None):
    '''.. versionadded:: 2.0

    Iterate scores backward in `expr`::

        abjad> score_1 = Score([Staff("c'8 d'8 e'8 f'8")])
        abjad> score_2 = Score([Staff("c'1"), Staff("g'1")])
        abjad> scores = [score_1, score_2]

    ::

        abjad> for score in scoretools.iterate_scores_backward_in_expr(scores):
        ...   score
        Score<<2>>
        Score<<1>>

    Ignore threads.

    Return generator.
    '''

    return componenttools.iterate_components_backward_in_expr(expr, Score, start = start, stop = stop)
