# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_leaf_durations(
    expr,
    label_durations=True,
    label_written_durations=True,
    markup_direction=Down,
    ):
    r'''Label leaves in expression with leaf durations.
    
    ..  container:: example

        **Example 1.** Label leaves with written durations:

        ::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> staff = scoretools.RhythmicStaff([tuplet])
            >>> override(staff).text_script.staff_padding = 2.5
            >>> override(staff).time_signature.stencil = False
            >>> labeltools.label_leaves_in_expr_with_leaf_durations(
            ...     tuplet, 
            ...     label_durations=False,
            ...     label_written_durations=True)

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

    ..  container:: example
    
        **Example 2.** Label leaves with actual durations:

        ::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> staff = scoretools.RhythmicStaff([tuplet])
            >>> override(staff).text_script.staff_padding = 2.5
            >>> override(staff).time_signature.stencil = False
            >>> labeltools.label_leaves_in_expr_with_leaf_durations(
            ...     tuplet, 
            ...     label_durations=True,
            ...     label_written_durations=False)

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

    ..  container:: example

        **Example 3.** Label leaves in tuplet with both written and actual
        durations:

        ::

            >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
            >>> staff = scoretools.RhythmicStaff([tuplet])
            >>> override(staff).text_script.staff_padding = 2.5
            >>> override(staff).time_signature.stencil = False
            >>> labeltools.label_leaves_in_expr_with_leaf_durations(
            ...     tuplet, 
            ...     label_durations=True,
            ...     label_written_durations=True)

        ::

            >>> show(staff) # doctest: +SKIP

        ..  doctest::

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

    Returns none.
    '''

    spanner_classes = (spannertools.Tie,)
    for leaf in iterate(expr).by_class(scoretools.Leaf):
        tie_spanners = leaf._get_spanners(spanner_classes)
        if not tie_spanners:
            if leaf.lilypond_duration_multiplier is not None:
                multiplier = '* %s' % str(leaf.lilypond_duration_multiplier)
            else:
                multiplier = ''
            if label_written_durations:
                label = markuptools.MarkupCommand(
                    'small', '{}{}'.format(
                        str(leaf.written_duration), multiplier))
                markup = markuptools.Markup(label, markup_direction)
                attach(markup, leaf)
            if label_durations:
                label = markuptools.MarkupCommand(
                    'small', str(leaf._get_duration()))
                markup = markuptools.Markup(label, markup_direction)
                attach(markup, leaf)
        elif tuple(tie_spanners)[0]._is_my_first_leaf(leaf):
            tie = tie_spanners.pop()
            if label_written_durations:
                written = sum([x.written_duration for x in tie])
                label = markuptools.MarkupCommand('small', str(written))
                markup = markuptools.Markup(label, markup_direction)
                attach(markup, leaf)
            if label_durations:
                prolated = sum([x._get_duration() for x in tie])
                label = markuptools.MarkupCommand('small', str(prolated))
                markup = markuptools.Markup(label, markup_direction)
                attach(markup, leaf)
