from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools


def label_leaves_in_expr_with_melodic_counterpoint_intervals(expr, markup_direction=Up):
    r""".. versionadded:: 2.0

    Label leaves in `expr` with melodic counterpoint intervals::

        >>> notes = notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)])
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_melodic_counterpoint_intervals(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { +15 }
            cs'''8 ^ \markup { -9 }
            b'8 ^ \markup { -9 }
            af8 ^ \markup { -7 }
            bf,8 ^ \markup { 1 }
            b,8 ^ \markup { +14 }
            a'8 ^ \markup { +2 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { 1 }
            f'8
        }

    Return none.
    """

    for note in iterationtools.iterate_notes_in_expr(expr):
        thread_iterator = iterationtools.iterate_thread_from_component(note, leaftools.Leaf)
        try:
            thread_iterator.next()
            next_leaf = thread_iterator.next()
            if isinstance(next_leaf, notetools.Note):
                cpi = \
                    pitchtools.calculate_melodic_counterpoint_interval(
                    note, next_leaf)
                markuptools.Markup(cpi, markup_direction)(note)
        except StopIteration:
            pass
