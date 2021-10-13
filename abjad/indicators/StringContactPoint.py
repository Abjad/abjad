from .. import format as _format
from ..markups import Markup


class StringContactPoint:
    """
    String contact point.

    ..  container:: example

        Sul ponticello:

        >>> indicator = abjad.StringContactPoint('sul ponticello')
        >>> string = abjad.storage(indicator)
        >>> print(string)
        abjad.StringContactPoint(
            contact_point='sul ponticello',
            )

    ..  container:: example

        Sul tasto:

        >>> indicator = abjad.StringContactPoint('sul tasto')
        >>> string = abjad.storage(indicator)
        >>> print(string)
        abjad.StringContactPoint(
            contact_point='sul tasto',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_contact_point",)

    _contact_point_abbreviations = {
        "dietro ponticello": "d.p.",
        "molto sul ponticello": "m.s.p",
        "molto sul tasto": "m.s.t.",
        "ordinario": "ord.",
        "pizzicato": "pizz.",
        "ponticello": "p.",
        "sul ponticello": "s.p.",
        "sul tasto": "s.t.",
    }

    _contact_points = (
        "dietro ponticello",
        "molto sul ponticello",
        "molto sul tasto",
        "ordinario",
        "pizzicato",
        "ponticello",
        "sul ponticello",
        "sul tasto",
    )

    _parameter = "SCP"

    _persistent = True

    ### INITIALIZER ###

    def __init__(self, contact_point: str = "ordinario") -> None:
        contact_point = str(contact_point)
        assert contact_point in self._contact_points
        self._contact_point = contact_point

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes string contact point.
        """
        return hash(self.__class__.__name__ + str(self))

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PUBLIC PROPERTIES ###

    @property
    def contact_point(self) -> str:
        """
        Gets contact point of string contact point.

        ..  container:: example

            Sul ponticello:

            >>> indicator = abjad.StringContactPoint('sul ponticello')
            >>> indicator.contact_point
            'sul ponticello'

        ..  container:: example

            Sul tasto:

            >>> indicator = abjad.StringContactPoint('sul tasto')
            >>> indicator.contact_point
            'sul tasto'

        Set to known string.
        """
        return self._contact_point

    @property
    def markup(self) -> Markup:
        r"""
        Gets markup of string contact point.

        ..  container:: example

            Sul ponticello:

            >>> indicator = abjad.StringContactPoint('sul ponticello')
            >>> abjad.show(indicator.markup) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(indicator.markup)
                >>> print(string)
                \markup \caps S.P.

        ..  container:: example

            Sul tasto:

            >>> indicator = abjad.StringContactPoint('sul tasto')
            >>> abjad.show(indicator.markup) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(indicator.markup)
                >>> print(string)
                \markup \caps S.T.

        """
        string = self._contact_point_abbreviations[self.contact_point]
        string = rf"\markup \caps {string.title()}"
        markup = Markup(string)
        return markup

    @property
    def parameter(self) -> str:
        """
        Returns ``'SCP'``.

        ..  container:: example

            >>> abjad.StringContactPoint('sul tasto').parameter
            'SCP'

        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StringContactPoint('sul tasto').persistent
            True

        """
        return self._persistent

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on string contact point.
        """
        pass
