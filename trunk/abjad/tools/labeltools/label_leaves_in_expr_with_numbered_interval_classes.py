# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools.scoretools import attach


def label_leaves_in_expr_with_numbered_interval_classes(expr, markup_direction=Up):
    r"""Label leaves in `expr` with numbered interval classes:

    ::

        >>> notes = notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)])
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_numbered_interval_classes(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { +1 }
            cs'''8 ^ \markup { -2 }
            b'8 ^ \markup { -3 }
            af8 ^ \markup { -10 }
            bf,8 ^ \markup { +1 }
            b,8 ^ \markup { +10 }
            a'8 ^ \markup { +1 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { -1 }
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """

    for note in iterationtools.iterate_notes_in_expr(expr):
        logical_voice_iterator = \
            iterationtools.iterate_logical_voice_from_component(
            note, leaftools.Leaf)
        try:
            logical_voice_iterator.next()
            next_leaf = logical_voice_iterator.next()
            if isinstance(next_leaf, notetools.Note):
                mdi = note.written_pitch - next_leaf.written_pitch
                mci = pitchtools.NumberedInterval(mdi)
                mcic = pitchtools.NumberedIntervalClass(mci)
                markup = markuptools.Markup(mcic, markup_direction)
                attach(markup, note)
        except StopIteration:
            pass
