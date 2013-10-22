# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools


def label_leaves_in_expr_with_named_interval_classes(expr, markup_direction=Up):
    r"""Label leaves in `expr` with named interval classes:

    ::

        >>> notes = notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)])
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_named_interval_classes(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { +aug8 }
            cs'''8 ^ \markup { -M2 }
            b'8 ^ \markup { -aug2 }
            af8 ^ \markup { -m7 }
            bf,8 ^ \markup { aug1 }
            b,8 ^ \markup { +m7 }
            a'8 ^ \markup { +m2 }
            bf'8 ^ \markup { -dim4 }
            fs'8 ^ \markup { aug1 }
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """

    for note in iterationtools.iterate_notes_in_expr(expr):
        logical_voice_iterator = iterationtools.iterate_logical_voice_from_component(note, leaftools.Leaf)
        try:
            logical_voice_iterator.next()
            next_leaf = logical_voice_iterator.next()
            if isinstance(next_leaf, notetools.Note):
                mdi = pitchtools.NamedInterval.from_pitch_carriers(
                    note, next_leaf)
                mdic = pitchtools.NamedIntervalClass(mdi)
                markuptools.Markup(mdic, markup_direction)(note)
        except StopIteration:
            pass
