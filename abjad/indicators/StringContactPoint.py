from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.markups import Markup


class StringContactPoint(AbjadValueObject):
    """
    String contact point.

    ..  container:: example

        Sul ponticello:

        >>> indicator = abjad.StringContactPoint('sul ponticello')
        >>> abjad.f(indicator)
        abjad.StringContactPoint(
            contact_point='sul ponticello',
            )

    ..  container:: example

        Sul tasto:

        >>> indicator = abjad.StringContactPoint('sul tasto')
        >>> abjad.f(indicator)
        abjad.StringContactPoint(
            contact_point='sul tasto',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contact_point',
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

    _parameter = True

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        contact_point: str = 'ordinario',
        ) -> None:
        contact_point = str(contact_point)
        assert contact_point in self._contact_points
        self._contact_point = contact_point

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

                >>> abjad.f(indicator.markup)
                \markup {
                    \caps
                        S.P.
                    }

        ..  container:: example

            Sul tasto:

            >>> indicator = abjad.StringContactPoint('sul tasto')
            >>> abjad.show(indicator.markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(indicator.markup)
                \markup {
                    \caps
                        S.T.
                    }

        """
        string = self._contact_point_abbreviations[self.contact_point]
        string = string.title()
        markup = Markup(string)
        markup = markup.caps()
        return markup

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StringContactPoint('sul tasto').parameter
            True

        """
        return self._parameter

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on string contact point.
        """
        pass
