# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class TextSpanner(Spanner):
    r'''A text spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> text_spanner = spannertools.TextSpanner()
        >>> grob = text_spanner.override.text_spanner
        >>> markup_command = markuptools.MarkupCommand('italic', 'foo')
        >>> markup_command = markuptools.MarkupCommand('bold', markup_command)
        >>> left_markup = markuptools.Markup(markup_command)
        >>> grob.bound_details__left__text = left_markup
        >>> pair = schemetools.SchemePair(0, -1)
        >>> markup_command = markuptools.MarkupCommand('draw-line', pair)
        >>> right_markup = markuptools.Markup(markup_command)
        >>> grob.bound_details__right__text = right_markup
        >>> text_spanner.override.text_spanner.dash_fraction = 1
        >>> text_spanner.attach([staff])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
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
            \revert TextSpanner #'bound-details #'left #'text
            \revert TextSpanner #'bound-details #'right #'text
            \revert TextSpanner #'dash-fraction
        }

    '''

    ### INITIALIZER ###

    def __init__(self, components=None, overrides=None):
        Spanner.__init__(self, components)
        overrides = overrides or {}
        self._apply_overrides(overrides)

    ### PRIVATE METHODS ###

    def _apply_overrides(self, overrides):
        from abjad.tools import markuptools
        exec('from abjad import *')
        for grob_attribute_string in overrides:
            grob_value_string = overrides[grob_attribute_string]
            statement = 'self.override.{} = {}'
            grob_attribute_string = grob_attribute_string.replace('__', '.', 1)
            grob_value_string = grob_value_string.replace('\t', '')
            strings = (grob_attribute_string, grob_value_string)
            statement = statement.format(*strings)
            print statement
            exec(statement)
            
    def _copy_keyword_args(self, new):
        pass

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r'\startTextSpan')
        if self._is_my_last_leaf(leaf):
            result.append(r'\stopTextSpan')
        return result
