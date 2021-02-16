import functools
import typing

from .. import typings
from ..duration import Multiplier
from ..markups import Markup
from ..storage import StorageFormatManager


@functools.total_ordering
class BowContactPoint:
    """
    Bow contact point.

    ..  container:: example

        Contact point exactly halfway from frog to tip of bow:

        >>> point = abjad.BowContactPoint((1, 2))
        >>> string = abjad.storage(point)
        >>> print(string)
        abjad.BowContactPoint(
            contact_point=abjad.Multiplier(1, 2),
            )

    ..  container:: example

        Contact point 3/5 of the way from frog to tip of bow:

        >>> point = abjad.BowContactPoint((3, 5))
        >>> string = abjad.storage(point)
        >>> print(string)
        abjad.BowContactPoint(
            contact_point=abjad.Multiplier(3, 5),
            )

    Contact points are measured from frog to tip as a fraction between ``0``
    and ``1``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_contact_point",)

    ### INITIALIZER ###

    def __init__(self, contact_point: typings.IntegerPair = None) -> None:
        contact_point_ = None
        if contact_point is not None:
            contact_point_ = Multiplier(contact_point)
            assert 0 <= contact_point_ <= 1
        self._contact_point = contact_point_

    ### SPECIAL METHODS ###

    def __lt__(self, argument) -> bool:
        """
        Is true if ``argument`` is a bow contact point and this bow contact
        point is less than ``argument``.

        ..  container:: example

            >>> point_1 = abjad.BowContactPoint((1, 2))
            >>> point_2 = abjad.BowContactPoint((1, 2))
            >>> point_3 = abjad.BowContactPoint((2, 3))

            >>> point_1 < point_1
            False
            >>> point_1 < point_2
            False
            >>> point_1 < point_3
            True

            >>> point_2 < point_1
            False
            >>> point_2 < point_2
            False
            >>> point_2 < point_3
            True

            >>> point_3 < point_1
            False
            >>> point_3 < point_2
            False
            >>> point_3 < point_3
            False

        """
        if isinstance(argument, type(self)):
            self_contact_point = self.contact_point or 0
            argument_contact_point = argument.contact_point or 0
            return self_contact_point < argument_contact_point
        raise TypeError("unorderable types")

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self) -> typing.Optional[Multiplier]:
        """
        Gets contact point of bow contact point.

        ..  container:: example

            One quarter of the way from frog to point:

            >>> point = abjad.BowContactPoint((1, 4))
            >>> point.contact_point
            Multiplier(1, 4)

        ..  container:: example

            Three fifths of the way from frog to point:

            >>> point = abjad.BowContactPoint((3, 5))
            >>> point.contact_point
            Multiplier(3, 5)

        """
        return self._contact_point

    @property
    def markup(self) -> Markup:
        r"""
        Gets markup of bow contact point.

        ..  container:: example

            One quarter of the way from frog to point:

            >>> indicator = abjad.BowContactPoint((1, 4))
            >>> print(abjad.lilypond(indicator.markup))
            \markup {
                \center-align
                    \vcenter
                        \fraction
                            1
                            4
                }
            >>> abjad.show(indicator.markup) # doctest: +SKIP

        ..  container:: example

            Three fifths of the way from frog to point:

            >>> indicator = abjad.BowContactPoint((3, 5))
            >>> print(abjad.lilypond(indicator.markup))
            \markup {
                \center-align
                    \vcenter
                        \fraction
                            3
                            5
                }
            >>> abjad.show(indicator.markup) # doctest: +SKIP

        """
        if self.contact_point is None:
            contact_point = Multiplier(0, 1)
        else:
            contact_point = self.contact_point
        fraction = fr"\fraction {contact_point.numerator} {contact_point.denominator}"
        string = rf"\center-align \vcenter {fraction}"
        markup = Markup(string)
        return markup

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on bow contact point.
        """
        pass
