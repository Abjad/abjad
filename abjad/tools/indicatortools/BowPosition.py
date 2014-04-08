# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadObject


class BowPosition(AbjadObject):
    r'''Bow position indicator.

    Bow position is measured from frog to tip as a fraction between 0 and 1.

    ::

        >>> indicator = indicatortools.BowPosition((1, 2))
        >>> print format(indicator)
        indicatortools.BowPosition(
            position=durationtools.Multiplier(1, 2),
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_position',
        )

    ### INITIALIZER ###

    def __init__(self,
        position=None,
        ):
        if position is not None:
            position = durationtools.Multiplier(position)
            assert 0 <= position <= 1
        self._position = position

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets bow position markup.

        ::

            >>> indicator = indicatortools.BowPosition((3, 4))
            >>> print format(indicator.markup, 'lilypond')
            ^ \markup {
                \vcenter
                    \fraction
                        3
                        4
                }

        '''
        string = r'\vcenter \fraction {} {}'.format(
            self.position.numerator,
            self.position.denominator,
            )
        markup = markuptools.Markup(string, Up)
        return markup

    @property
    def position(self):
        r'''Gets bow position.

        ::

            >>> indicator = indicatortools.BowPosition((1, 4))
            >>> indicator.position
            Multiplier(1, 4)

        Returns multiplier.
        '''
        return self._position
