# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_numbered_intervals(expr, markup_direction=Up):
    r"""Label leaves in `expr` with numbered intervals:

    ::

        >>> notes = scoretools.make_notes(
        ...     [0, 25, 11, -4, -14, -13, 9, 10, 6, 5],
        ...     [Duration(1, 8)],
        ...     )
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_numbered_intervals(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { +25 }
            cs'''8 ^ \markup { -14 }
            b'8 ^ \markup { -15 }
            af8 ^ \markup { -10 }
            bf,8 ^ \markup { +1 }
            b,8 ^ \markup { +22 }
            a'8 ^ \markup { +1 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { -1 }
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """

    for note in iterate(expr).by_class(scoretools.Note):
        logical_voice_iterator = \
            iterationtools.iterate_logical_voice_from_component(
            note, scoretools.Leaf)
        try:
            logical_voice_iterator.next()
            next_leaf = logical_voice_iterator.next()
            if isinstance(next_leaf, scoretools.Note):
                mci = pitchtools.NumberedInterval.from_pitch_carriers(
                    note, next_leaf)
                markup = markuptools.Markup(mci, markup_direction)
                attach(markup, note)
        except StopIteration:
            pass
