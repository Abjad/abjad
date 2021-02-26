import functools
import typing

from .. import enums, math
from ..bundle import LilyPondFormatBundle
from ..markups import Markup
from ..new import new
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


@functools.total_ordering
class ColorFingering:
    r"""
    Color fingering.

    ..  container:: example

        First color fingering:

        >>> fingering = abjad.ColorFingering(1)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            1
                }

    ..  container:: example

        Second color fingering:

        >>> fingering = abjad.ColorFingering(2)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            ^ \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            2
                }

    Color fingerings indicate alternate woodwind fingerings by amount of pitch
    of timbre deviation.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_number", "_tweaks")

    _format_slot = "after"

    ### INITIALIZER ###

    def __init__(self, number: int = None, *, tweaks: TweakInterface = None) -> None:
        if number is not None:
            assert math.is_positive_integer(number)
        self._number = number
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ##

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __lt__(self, argument) -> bool:
        """
        Is true if ``argument`` is a color fingering and the number of this
        color fingering is less than that of ``argument``.

        ..  container:: example

            >>> fingering_1 = abjad.ColorFingering(1)
            >>> fingering_2 = abjad.ColorFingering(1)
            >>> fingering_3 = abjad.ColorFingering(2)

            >>> fingering_1 < fingering_1
            False
            >>> fingering_1 < fingering_2
            False
            >>> fingering_1 < fingering_3
            True

            >>> fingering_2 < fingering_1
            False
            >>> fingering_2 < fingering_2
            False
            >>> fingering_2 < fingering_3
            True

            >>> fingering_3 < fingering_1
            False
            >>> fingering_3 < fingering_2
            False
            >>> fingering_3 < fingering_3
            False

        """
        if isinstance(argument, type(self)):
            return (self.number or 0) < (argument.number or 0)
        raise TypeError("unorderable types")

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return self.markup._get_lilypond_format()

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.markup.extend(tweaks)
        markup = self.markup
        markup = new(markup, direction=enums.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.after.markup.extend(markup_format_pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self) -> typing.Optional[Markup]:
        r"""
        Gets markup of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> print(abjad.lilypond(fingering.markup))
            \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            1
                }
            >>> abjad.show(fingering.markup) # doctest: +SKIP

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> print(abjad.lilypond(fingering.markup))
            \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            2
                }
            >>> abjad.show(fingering.markup) # doctest: +SKIP

        """
        if self.number is None:
            return None
        string = rf"\override #'(circle-padding . 0.25) \circle \finger {self.number}"
        string = rf"\markup {{ {string} }}"
        markup = Markup(string, literal=True)
        return markup

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets number of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> fingering.number
            1

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> fingering.number
            2

        """
        return self._number

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> fingering = abjad.ColorFingering(1)
            >>> abjad.tweak(fingering).color = "#blue"
            >>> abjad.attach(fingering, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    ^ \markup {
                        \override
                            #'(circle-padding . 0.25)
                            \circle
                                \finger
                                    1
                        }
                    d'4
                    e'4
                    f'4
                }

        """
        return self._tweaks
