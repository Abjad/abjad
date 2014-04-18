# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadObject


class BowHairContactPoint(AbjadObject):
    r'''Bow hair contact point indicator.

    Contact points are measured from frog to tip as a fraction between 0 and 1.

    ::

        >>> indicator = indicatortools.BowHairContactPoint((1, 2))
        >>> print(format(indicator))
        indicatortools.BowHairContactPoint(
            contact_point=durationtools.Multiplier(1, 2),
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
        )

    ### INITIALIZER ###

    def __init__(self,
        contact_point=None,
        ):
        if contact_point is not None:
            contact_point = durationtools.Multiplier(contact_point)
            assert 0 <= contact_point <= 1
        self._contact_point = contact_point

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets bow hair contact point markup.

        ::

            >>> indicator = indicatortools.BowHairContactPoint((3, 4))
            >>> print(format(indicator.markup, 'lilypond'))
            ^ \markup {
                \vcenter
                    \fraction
                        3
                        4
                }

        '''
        string = r'\vcenter \fraction {} {}'.format(
            self.contact_point.numerator,
            self.contact_point.denominator,
            )
        markup = markuptools.Markup(string, Up)
        return markup

    @property
    def contact_point(self):
        r'''Gets contact point.

        ::

            >>> indicator = indicatortools.BowHairContactPoint((1, 4))
            >>> indicator.contact_point
            Multiplier(1, 4)

        Returns multiplier.
        '''
        return self._contact_point

