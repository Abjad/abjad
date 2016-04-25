# -*- coding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class BowContactPoint(AbjadValueObject):
    r'''Bow contact point.

    ..  container:: example

        **Example 1.** Contact point exactly halfway from frog to tip of bow:

        ::

            >>> point = indicatortools.BowContactPoint((1, 2))
            >>> print(format(point))
            indicatortools.BowContactPoint(
                contact_point=durationtools.Multiplier(1, 2),
                )

    ..  container:: example

        **Example 2.** Contact point 3/5 of the way from frog to tip of bow:

        ::

            >>> point = indicatortools.BowContactPoint((3, 5))
            >>> print(format(point))
            indicatortools.BowContactPoint(
                contact_point=durationtools.Multiplier(3, 5),
                )

    Contact points are measured from frog to tip as a fraction between ``0`` 
    and ``1``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
        '_default_scope'
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
        self._default_scope = None

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

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self.contact_point < expr.contact_point
        raise TypeError('unorderable types')

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self):
        r'''Gets contact point of bow contact point.

        ..  container:: example

            **Example 1.** One quarter of the way from frog to point:

            ::

                >>> point = indicatortools.BowContactPoint((1, 4))
                >>> point.contact_point
                Multiplier(1, 4)

        ..  container:: example

            **Example 2.** Three fifths of the way from frog to point:

            ::

                >>> point = indicatortools.BowContactPoint((3, 5))
                >>> point.contact_point
                Multiplier(3, 5)

        Returns multiplier.
        '''
        return self._contact_point

    @property
    def markup(self):
        r'''Gets markup of bow contact point.

        ..  container:: example

            **Example 1.** One quarter of the way from frog to point:

            ::

                >>> indicator = indicatortools.BowContactPoint((1, 4))
                >>> print(format(indicator.markup, 'lilypond'))
                \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                4
                    }
                >>> show(indicator.markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.** Three fifths of the way from frog to point:

            ::

                >>> indicator = indicatortools.BowContactPoint((3, 5))
                >>> print(format(indicator.markup, 'lilypond'))
                \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                5
                    }
                >>> show(indicator.markup) # doctest: +SKIP

        Returns markup.
        '''
        markup = markuptools.Markup.fraction(
            self.contact_point.numerator,
            self.contact_point.denominator,
            )
        markup = markup.vcenter()
        markup = markup.center_align()
        return markup
