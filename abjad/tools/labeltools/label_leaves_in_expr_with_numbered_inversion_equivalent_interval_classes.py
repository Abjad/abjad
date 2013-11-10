# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import iterationtools
from abjad.tools import scoretools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_numbered_inversion_equivalent_interval_classes(
    expr, markup_direction=Up):
    r"""Label leaves in `expr` with numbered inversion-equivalent interval classes:

    ::

        >>> notes = scoretools.make_notes(
        ...     [0, 25, 11, -4, -14, -13, 9, 10, 6, 5],
        ...     [Duration(1, 8)],
        ...     )
        >>> staff = Staff(notes)
        >>> labeltools.label_leaves_in_expr_with_numbered_inversion_equivalent_interval_classes(
        ...     staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 ^ \markup { 1 }
            cs'''8 ^ \markup { 2 }
            b'8 ^ \markup { 3 }
            af8 ^ \markup { 2 }
            bf,8 ^ \markup { 1 }
            b,8 ^ \markup { 2 }
            a'8 ^ \markup { 1 }
            bf'8 ^ \markup { 4 }
            fs'8 ^ \markup { 1 }
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """

    for note in iterate(expr).by_class(scoretools.Note):
        logical_voice_iterator = iterate(note).by_logical_voice_from_component(
            scoretools.Leaf,
            )
        try:
            logical_voice_iterator.next()
            next_leaf = logical_voice_iterator.next()
            if isinstance(next_leaf, scoretools.Note):
                mdi = note.written_pitch - next_leaf.written_pitch
                iecic = \
                    pitchtools.NumberedInversionEquivalentIntervalClass(mdi)
                markup = markuptools.Markup(iecic, markup_direction)
                attach(markup, note)
        except StopIteration:
            pass
