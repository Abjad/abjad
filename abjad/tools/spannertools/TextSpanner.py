# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class TextSpanner(Spanner):
    r'''A text spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> text_spanner = spannertools.TextSpanner()
            >>> grob = override(text_spanner).text_spanner
            >>> markup_command = markuptools.MarkupCommand('italic', 'foo')
            >>> markup_command = markuptools.MarkupCommand('bold', markup_command)
            >>> left_markup = markuptools.Markup(markup_command)
            >>> grob.bound_details__left__text = left_markup
            >>> pair = schemetools.SchemePair(0, -1)
            >>> markup_command = markuptools.MarkupCommand('draw-line', pair)
            >>> right_markup = markuptools.Markup(markup_command)
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
        '_dynamic_text',
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

    def _get_lilypond_format_bundle(self, leaf):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        if self._is_my_first_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'override',
                is_once=False,
                )
            lilypond_format_bundle.grob_overrides.extend(contributions)
            string = r'\startTextSpan'
            lilypond_format_bundle.right.spanner_starts.append(string)
        if self._is_my_last_leaf(leaf):
            contributions = override(self)._list_format_contributions(
                'revert',
                )
            lilypond_format_bundle.grob_reverts.extend(contributions)
            string = r'\stopTextSpan'
            lilypond_format_bundle.right.spanner_stops.append(string)
        return lilypond_format_bundle
