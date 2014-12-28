# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class StringContactPoint(AbjadValueObject):
    r'''String contact point indicator.

    ::

        >>> indicator = indicatortools.StringContactPoint('sul ponticello')
        >>> print(format(indicator))
        indicatortools.StringContactPoint(
            contact_point='sul ponticello',
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
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

    def __init__(self,
        contact_point='ordinario',
        ):
        contact_point = str(contact_point)
        assert contact_point in self._contact_points
        self._contact_point = contact_point

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point.

        ::

            >>> indicator = indicatortools.StringContactPoint('sul tasto')
            >>> indicator.contact_point
            'sul tasto'

        Returns string.
        '''
        return self._contact_point

    @property
    def markup(self):
        r'''Gets contact point markup.

        ::

            >>> indicator = indicatortools.StringContactPoint('sul tasto')
            >>> print(format(indicator.markup))
            \markup {
                \caps
                    S.T.
                }

        Returns markup.
        '''
        from abjad.tools import markuptools
        markup = self._contact_point_abbreviations[self.contact_point]
        markup = markup.title()
        markup = markuptools.Markup(markup)
        markup = markup.caps()
        return markup