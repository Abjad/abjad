from abjad.tools import marktools


def add_double_bar_to_end_of_score(score):
    r'''.. versionadded:: 2.0

    Add double bar to end of `score`::

        abjad> staff = Staff("c'4 d'4 e'4 f'4")

    ::

        abjad> scoretools.add_double_bar_to_end_of_score(staff)
        BarLine('|.')(f'4)

    ::

        abjad> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }

    Return double bar.
    '''
    from abjad.tools import leaftools

    last_leaf = leaftools.get_nth_leaf_in_expr(score, -1)
    double_bar = marktools.BarLine('|.')(last_leaf)

    return double_bar
