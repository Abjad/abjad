# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondnametools
from abjad.tools import markuptools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import override


class TextSpanner(Spanner):
    r'''Text spanner.

    ..  container:: example

        **Example 1.** A text spanner with no grob overrides:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> text_spanner = spannertools.TextSpanner()
            >>> attach(text_spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
            }

        This is (notationally unlikely) default behavior.

    ..  container:: example

        **Example 2.** A text spanner with a grob override for left text:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> text_spanner = spannertools.TextSpanner()
            >>> markup = Markup('foo').italic().bold()
            >>> override(text_spanner).text_spanner.bound_details__left__text = markup
            >>> override(text_spanner).text_spanner.bound_details__left__stencil_align_dir_y = 0
            >>> attach(text_spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \override TextSpanner.bound-details.left.stencil-align-dir-y = #0
                \override TextSpanner.bound-details.left.text = \markup {
                    \bold
                        \italic
                            foo
                    }
                c'4 \startTextSpan
                d'4
                e'4
                f'4 \stopTextSpan
                \revert TextSpanner.bound-details
            }

    ..  container:: example

        **Example 3.** Text spanner interacting with annotated markup.
        At the beginning of the spanner:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> markup = Markup('pont.')
            >>> attach(markup, staff[0], is_annotation=True)
            >>> text_spanner = spannertools.TextSpanner()
            >>> attach(text_spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4
            }

        Text spanner is suppresssed and only the markup appears.

    ..  container:: example

        **Example 4.** Text spanner interacting with annotated markup.
        At the end of the spanner:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> markup = Markup('tasto')
            >>> attach(markup, staff[-1], is_annotation=True)
            >>> text_spanner = spannertools.TextSpanner()
            >>> attach(text_spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4 ^ \markup { tasto }
            }

        Text spanner is suppresssed and only the markup appears.

    ..  container:: example

        **Example 5.** Text spanner interacting with annotated markup.
        At the beginning and the end of the spanner:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> markup = Markup('pont.')
            >>> attach(markup, staff[0], is_annotation=True)
            >>> markup = Markup('tasto')
            >>> attach(markup, staff[-1], is_annotation=True)
            >>> text_spanner = spannertools.TextSpanner()
            >>> attach(text_spanner, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ^ \markup { pont. }
                d'4
                e'4
                f'4 ^ \markup { tasto }
            }

        Text spanner is suppresssed and only the markup appear.
        
    ..  container:: example

        **Example 6.** Requires at least two leaves:

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> text_spanner = spannertools.TextSpanner()
            >>> attach(text_spanner, staff[:1])
            Traceback (most recent call last):
            ...
            Exception: TextSpanner() attachment test fails for Selection([Note("c'4")]).

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, overrides=None):
        Spanner.__init__(self, overrides=overrides)

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, expr):
        return self._at_least_two_leaves(expr)

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        markups = []
        prototype = markuptools.Markup
        if inspector.has_indicator(prototype):
            indicator_expressions = inspector.get_indicators(
                markuptools.Markup,
                unwrap=False,
                )
            for indicator_expression in indicator_expressions:
                if indicator_expression.is_annotation:
                    markups.append(indicator_expression.indicator)
        markups = markups or None
        line_segment = None
        prototype = indicatortools.LineSegment
        if inspector.has_indicator(prototype):
            line_segment = inspector.get_indicator(prototype)
        return (
            markups,
            line_segment,
            )

    def _get_lilypond_format_bundle(self, component=None):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(
            component,
            )
        current_annotations = self._get_annotations(component)
        current_markups = current_annotations[0]
        current_markup = bool(current_markups)
        current_line_segment = current_annotations[1]
        start_spanner = self._spanner_starts_on_leaf(component)
        stop_spanner = self._spanner_stops_on_leaf(component)
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
                override_string = override_.override_string
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
                override_string = override_.override_string
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

    def _leaf_has_current_event(self, leaf):
        annotations = self._get_annotations(leaf)
        markup = bool(annotations[0])
        line_segment = bool(annotations[1])
        return markup or line_segment

    def _leaf_has_markup(self, leaf):
        annotations = self._get_annotations(leaf)
        markup = bool(annotations[0])
        return markup

    def _spanner_has_smart_events(self):
        leaves = self._get_leaves()
        for leaf in leaves:
            if self._leaf_has_current_event(leaf):
                return True
        return False

    def _spanner_is_open_immediately_before_leaf(self, leaf):
        from abjad.tools import scoretools
        if not isinstance(leaf, scoretools.Leaf):
            return False
        leaves = self._get_leaves()
        index = leaves.index(leaf)
        for index in reversed(range(index)):
            previous_leaf = leaves[index]
            if self._spanner_starts_on_leaf(previous_leaf):
                return True
            if self._leaf_has_markup(previous_leaf):
                return False
        return False

    def _spanner_starts_on_leaf(self, leaf):
        annotations = self._get_annotations(leaf)
        markup = bool(annotations[0])
        line_segment = annotations[1]
        has_smart_events = self._spanner_has_smart_events()
        if not has_smart_events and self._is_my_first_leaf(leaf):
            return True
        if line_segment:
            return True
        return False

    def _spanner_stops_on_leaf(self, leaf):
        annotations = self._get_annotations(leaf)
        markup = bool(annotations[0])
        line_segment = annotations[1]
        spanner_is_open = self._spanner_is_open_immediately_before_leaf(leaf)
        if spanner_is_open and self._leaf_has_current_event(leaf):
            return True
        if spanner_is_open and self._is_my_last_leaf(leaf):
            return True
        return False
