# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import markuptools
from abjad.tools import spannertools


def label_leaves_in_expr_with_leaf_durations(
    expr,
    label_durations=True,
    label_written_durations=True,
    markup_direction=Down,
    ):
    r'''.. versionadded:: 1.1

    Example 1. Label leaves with written durations:

    ::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
        >>> staff = stafftools.RhythmicStaff([tuplet])
        >>> staff.override.text_script.staff_padding = 2.5
        >>> staff.override.time_signature.stencil = False
        >>> labeltools.label_leaves_in_expr_with_leaf_durations(
        ...     tuplet, 
        ...     label_durations=False,
        ...     label_written_durations=True)

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> f(staff)
        \new RhythmicStaff \with {
            \override TextScript #'staff-padding = #2.5
            \override TimeSignature #'stencil = ##f
        } {
            \times 2/3 {
                c'8 _ \markup { \small 1/8 }
                d'8 _ \markup { \small 1/8 }
                e'8 _ \markup { \small 1/8 }
            }
        }

    Example 2. Label leaves with actual durations:

    ::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
        >>> staff = stafftools.RhythmicStaff([tuplet])
        >>> staff.override.text_script.staff_padding = 2.5
        >>> staff.override.time_signature.stencil = False
        >>> labeltools.label_leaves_in_expr_with_leaf_durations(
        ...     tuplet, 
        ...     label_durations=True,
        ...     label_written_durations=False)

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> f(staff)
        \new RhythmicStaff \with {
            \override TextScript #'staff-padding = #2.5
            \override TimeSignature #'stencil = ##f
        } {
            \times 2/3 {
                c'8 _ \markup { \small 1/12 }
                d'8 _ \markup { \small 1/12 }
                e'8 _ \markup { \small 1/12 }
            }
        }

    Example 3. Label leaves in tuplet with both written and actual
    durations:

    ::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
        >>> staff = stafftools.RhythmicStaff([tuplet])
        >>> staff.override.text_script.staff_padding = 2.5
        >>> staff.override.time_signature.stencil = False
        >>> labeltools.label_leaves_in_expr_with_leaf_durations(
        ...     tuplet, 
        ...     label_durations=True,
        ...     label_written_durations=True)

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> f(staff)
        \new RhythmicStaff \with {
            \override TextScript #'staff-padding = #2.5
            \override TimeSignature #'stencil = ##f
        } {
            \times 2/3 {
                c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
                d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
                e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
            }
        }

    Return none.
    '''

    spanner_classes = (spannertools.TieSpanner, )
    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        tie_spanners = spannertools.get_spanners_attached_to_component(
            leaf, spanner_classes=spanner_classes)
        if not tie_spanners:
            if leaf.duration_multiplier is not None:
                multiplier = '* %s' % str(leaf.duration_multiplier)
            else:
                multiplier = ''
            if label_written_durations:
                label = markuptools.MarkupCommand(
                    'small', '{}{}'.format(
                        str(leaf.written_duration), multiplier))
                markuptools.Markup(label, markup_direction)(leaf)
            if label_durations:
                label = markuptools.MarkupCommand(
                    'small', str(leaf.duration))
                markuptools.Markup(label, markup_direction)(leaf)
        elif tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
            tie = tie_spanners.pop()
            if label_written_durations:
                written = sum([x.written_duration for x in tie])
                label = markuptools.MarkupCommand('small', str(written))
                markuptools.Markup(label, markup_direction)(leaf)
            if label_durations:
                prolated = sum([x.duration for x in tie])
                label = markuptools.MarkupCommand('small', str(prolated))
                markuptools.Markup(label, markup_direction)(leaf)
