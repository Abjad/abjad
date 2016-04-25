# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class StringContactPoint(AbjadValueObject):
    r'''String contact point indicator.

    ..  container:: example

        **Example 1.** Sul ponticello:

        ::

            >>> indicator = indicatortools.StringContactPoint('sul ponticello')
            >>> print(format(indicator))
            indicatortools.StringContactPoint(
                contact_point='sul ponticello',
                )

    ..  container:: example

        **Example 2.** Sul tasto:

        ::

            >>> indicator = indicatortools.StringContactPoint('sul tasto')
            >>> print(format(indicator))
            indicatortools.StringContactPoint(
                contact_point='sul tasto',
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
        '_default_scope',
        )

    _contact_points = (
        'dietro ponticello',
        'molto sul ponticello',
        'molto sul tasto',
        'ordinario',
        'pizzicato',
        'ponticello',
        'sul ponticello',
        'sul tasto',
        )

    _contact_point_abbreviations = {
        'dietro ponticello': 'd.p.',
        'molto sul ponticello': 'm.s.p',
        'molto sul tasto': 'm.s.t.',
        'ordinario': 'ord.',
        'pizzicato': 'pizz.',
        'ponticello': 'p.',
        'sul ponticello': 's.p.',
        'sul tasto': 's.t.',
        }

    ### INITIALIZER ###

    def __init__(
        self,
        contact_point='ordinario',
        ):
        contact_point = str(contact_point)
        assert contact_point in self._contact_points
        self._contact_point = contact_point
        self._default_scope = None

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point of string contact point.

        ..  container:: example

            **Example 1.** Sul ponticello:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul ponticello')
                >>> indicator.contact_point
                'sul ponticello'

        ..  container:: example

            **Example 2.** Sul tasto:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul tasto')
                >>> indicator.contact_point
                'sul tasto'

        Set to known string.

        Defaults to ``'ordinario'``.

        Returns known string.
        '''
        return self._contact_point


    @property
    def default_scope(self):
        r'''Gets default scope of string contact point.

        ..  container:: example

            **Example 1.** Sul ponticello:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul ponticello')
                >>> indicator.default_scope is None
                True

        ..  container:: example

            **Example 2.** Sul tasto:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul tasto')
                >>> indicator.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def markup(self):
        r'''Gets markup of string contact point.

        ..  container:: example

            **Example 1.** Sul ponticello:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul ponticello')
                >>> show(indicator.markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(indicator.markup))
                \markup {
                    \caps
                        S.P.
                    }

        ..  container:: example

            **Example 2.** Sul tasto:

            ::

                >>> indicator = indicatortools.StringContactPoint('sul tasto')
                >>> show(indicator.markup) # doctest: +SKIP

            ..  doctest::

                >>> print(format(indicator.markup))
                \markup {
                    \caps
                        S.T.
                    }

        Returns abbreviation markup.
        '''
        from abjad.tools import markuptools
        markup = self._contact_point_abbreviations[self.contact_point]
        markup = markup.title()
        markup = markuptools.Markup(markup)
        markup = markup.caps()
        return markup
