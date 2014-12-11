# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import markuptools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import override


class TextSpanner(Spanner):
    r'''A text spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> text_spanner = spannertools.TextSpanner()
            >>> grob = override(text_spanner).text_spanner
            >>> left_markup = Markup('foo').italic().bold()
            >>> grob.bound_details__left__text = left_markup
            >>> right_markup = Markup.draw_line(0, -1)
            >>> grob.bound_details__right__text = right_markup
            >>> override(text_spanner).text_spanner.dash_fraction = 1
            >>> attach(text_spanner, [staff])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \override TextSpanner #'bound-details #'left #'text = \markup {
                    \bold \italic foo }
                \override TextSpanner #'bound-details #'right #'text = \markup {
                    \draw-line #'(0 . -1) }
                \override TextSpanner #'dash-fraction = #1
                c'8 \startTextSpan
                d'8
                e'8
                f'8 \stopTextSpan
                \revert TextSpanner #'bound-details
                \revert TextSpanner #'dash-fraction
            }

    Formats LilyPond ``\startTextSpan`` command on first leaf in spanner.

    Formats LilyPond ``\stopTextSpan`` command on last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        markups = None
        prototype = markuptools.Markup
        if inspector.has_indicator(prototype):
            markups = inspector.get_indicators(markuptools.Markup)
        line_segment = None
        prototype = indicatortools.LineSegment
        if inspector.has_indicator(prototype):
            line_segment = inspector.get_indicator(prototype)
        return (
            markups,
            line_segment,
            )

    def _get_lilypond_format_bundle(self, component):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(
            component,
            )
        previous_annotations = self._get_previous_annotations(component)
        previous_markups = previous_annotations[0]
        previous_line_segment = previous_annotations[1]
        previous_segment = (previous_markups is not None or 
            previous_line_segment is not None)
        current_annotations = self._get_annotations(component)
        current_markups = current_annotations[0]
        current_markup = bool(current_markups)
        current_line_segment = current_annotations[1]
        current_event = (current_markups is not None or 
            current_line_segment is not None)
        start_spanner, stop_spanner = False, False
        # stop any previous segment
        if previous_segment and current_event:
            stop_spanner = True
        # start spanner if no markup
        if self._is_my_first_leaf(component) and not current_markup:
            start_spanner = True
        # start spanner if existing line segment
        elif current_line_segment:
            start_spanner = True
        # stop spanner if last component
        if self._is_my_last_leaf(component):
            stop_spanner = True
        if start_spanner:
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
            string = r'\startTextSpan'
            lilypond_format_bundle.right.spanner_starts.append(string)
        if stop_spanner:
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
            string = r'\stopTextSpan'
            lilypond_format_bundle.right.spanner_stops.append(string)
        if current_markups is not None:
            # assign markup to spanner left text
            if start_spanner:
                markup = current_markups[0]
                if current_line_segment:
                    if current_line_segment.left_hspace is not None:
                        hspace = current_line_segment.left_hspace
                        hspace = markuptools.Markup.hspace(hspace)
                        markup = markuptools.Markup.concat([markup, hspace])
                override_ = lilypondnametools.LilyPondGrobOverride(
                    grob_name='TextSpanner',
                    is_once=True,
                    property_path=(
                        'bound-details',
                        'left',
                        'text',
                        ),
                    value=markup,
                    )
                override_string = '\n'.join(override_._override_format_pieces)
                lilypond_format_bundle.grob_overrides.append(override_string)
            # format markup normally
            else:
                current_markup = current_markups[0]
                markup = new(current_markup, direction=Up)
                string = format(markup, 'lilypond')
                lilypond_format_bundle.right.markup.append(string)
        if current_line_segment is not None:
            overrides = current_line_segment._get_lilypond_grob_overrides()
            for override_ in overrides:
                override_string = '\n'.join(override_._override_format_pieces)
                lilypond_format_bundle.grob_overrides.append(override_string)
        return lilypond_format_bundle

    def _get_previous_annotations(self, component):
        from abjad.tools import scoretools
        if not isinstance(component, scoretools.Leaf):
            return None, None
        leaves = self._get_leaves()
        index = leaves.index(component)
        for index in reversed(range(index)):
            previous_leaf = leaves[index]
            annotations = self._get_annotations(previous_leaf)
            if any(_ is not None for _ in annotations):
                return annotations
        return None, None