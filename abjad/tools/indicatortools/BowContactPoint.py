# -*- encoding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadObject


@functools.total_ordering
class BowContactPoint(AbjadObject):
    r'''Bow contact point indicator.

    Contact points are measured from frog to tip as a fraction between 0 and 1.

    ::

        >>> indicator = indicatortools.BowContactPoint((1, 2))
        >>> print(format(indicator))
        indicatortools.BowContactPoint(
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

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true if `expr` is a bow contact point with the same contact
        point as this bow contact point.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self.contact_point == expr.contact_point
        raise TypeError('unorderable types')

    def __hash__(self):
        r'''Hashes bow contact point.
        '''
        from abjad.tools import systemtools
        return hash(systemtools.StorageFormatManager.get_hash_values(self))

    def __lt__(self, expr):
        r'''Is true if `expr` is a bow contact point and this bow contact point
        is less than `expr`.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self.contact_point < expr.contact_point
        raise TypeError('unorderable types')

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point.

        ::

            >>> indicator = indicatortools.BowContactPoint((1, 4))
            >>> indicator.contact_point
            Multiplier(1, 4)

        Returns multiplier.
        '''
        return self._contact_point

    @property
    def markup(self):
        r'''Gets bow contact point markup.

        ::

            >>> indicator = indicatortools.BowContactPoint((3, 4))
            >>> print(format(indicator.markup, 'lilypond'))
            \markup {
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
        markup = markuptools.Markup(string)
        return markup
