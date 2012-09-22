from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools


def label_leaves_in_expr_with_melodic_diatonic_intervals(expr, markup_direction=Up):
    r""".. versionadded:: 2.0

    Label leaves in `expr` with melodic diatonic intervals::

        >>> notes = notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)])
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_melodic_diatonic_intervals(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { +aug15 }
            cs'''8 ^ \markup { -M9 }
            b'8 ^ \markup { -aug9 }
            af8 ^ \markup { -m7 }
            bf,8 ^ \markup { +aug1 }
            b,8 ^ \markup { +m14 }
            a'8 ^ \markup { +m2 }
            bf'8 ^ \markup { -dim4 }
            fs'8 ^ \markup { -aug1 }
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
                mdi = pitchtools.calculate_melodic_diatonic_interval(
                    note, next_leaf)
                markuptools.Markup(mdi, markup_direction)(note)
        except StopIteration:
            pass
