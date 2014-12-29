# -*- encoding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class BowContactPoint(AbjadValueObject):
    r'''Bow contact point.

    ..  container:: example

        Contact point exactly halfway from frog to tip of bow:

        ::

            >>> point = indicatortools.BowContactPoint((1, 2))
            >>> print(format(point))
            indicatortools.BowContactPoint(
                contact_point=durationtools.Multiplier(1, 2),
                )

    Contact points are measured from frog to tip as a fraction between ``0`` 
    and ``1``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        contact_point=None,
        ):
        if contact_point is not None:
            contact_point = durationtools.Multiplier(contact_point)
            assert 0 <= contact_point <= 1
        self._contact_point = contact_point

    ### SPECIAL METHODS ###

    def __lt__(self, expr):
        r'''Is true if `expr` is a bow contact point and this bow contact point
        is less than `expr`.

        ..  container:: example

            ::

                >>> point_1 = indicatortools.BowContactPoint((1, 2))
                >>> point_2 = indicatortools.BowContactPoint((1, 2))
                >>> point_3 = indicatortools.BowContactPoint((2, 3))

            ::

                >>> point_1 < point_1
                False
                >>> point_1 < point_2
                False
                >>> point_1 < point_3
                True

            ::

                >>> point_2 < point_1
                False
                >>> point_2 < point_2
                False
                >>> point_2 < point_3
                True

            ::

                >>> point_3 < point_1
                False
                >>> point_3 < point_2
                False
                >>> point_3 < point_3
                False

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self.contact_point < expr.contact_point
        raise TypeError('unorderable types')

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point of bow contact point.

        ..  container:: example

            ::

                >>> point = indicatortools.BowContactPoint((1, 4))
                >>> point.contact_point
                Multiplier(1, 4)

        Returns multiplier.
        '''
        return self._contact_point

    @property
    def markup(self):
        r'''Gets markup of bow contact point.

        ..  container:: example

            ::

                >>> indicator = indicatortools.BowContactPoint((3, 4))
                >>> print(format(indicator.markup, 'lilypond'))
                \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }

        Returns markup.
        '''
        markup = markuptools.Markup.fraction(
            self.contact_point.numerator,
            self.contact_point.denominator,
            )
        markup = markup.vcenter()
        markup = markup.center_align()
        return markup