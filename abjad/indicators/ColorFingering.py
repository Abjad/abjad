import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import markups as _markups
from .. import new as _new
from .. import overrides as _overrides


@dataclasses.dataclass(order=True, unsafe_hash=True)
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
            ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

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
            ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }

    Color fingerings indicate alternate woodwind fingerings by amount of pitch of timbre
    deviation.

    ..  container:: example

        Tweaks:

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
                ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                d'4
                e'4
                f'4
            }

    """

    number: int
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _format_slot = "after"

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    #    def __eq__(self, argument) -> bool:
    #        """
    #        Delegates to ``abjad.format.compare_objects()``.
    #        """
    #        return _format.compare_objects(self, argument)
    #
    #    def __hash__(self) -> int:
    #        """
    #        Hashes color fingering.
    #        """
    #        return hash(self.__class__.__name__ + str(self))
    #
    #    def __lt__(self, argument) -> bool:
    #        """
    #        Is true if ``argument`` is a color fingering and the number of this
    #        color fingering is less than that of ``argument``.
    #
    #        ..  container:: example
    #
    #            >>> fingering_1 = abjad.ColorFingering(1)
    #            >>> fingering_2 = abjad.ColorFingering(1)
    #            >>> fingering_3 = abjad.ColorFingering(2)
    #
    #            >>> fingering_1 < fingering_1
    #            False
    #            >>> fingering_1 < fingering_2
    #            False
    #            >>> fingering_1 < fingering_3
    #            True
    #
    #            >>> fingering_2 < fingering_1
    #            False
    #            >>> fingering_2 < fingering_2
    #            False
    #            >>> fingering_2 < fingering_3
    #            True
    #
    #            >>> fingering_3 < fingering_1
    #            False
    #            >>> fingering_3 < fingering_2
    #            False
    #            >>> fingering_3 < fingering_3
    #            False
    #
    #        """
    #        if isinstance(argument, type(self)):
    #            return (self.number or 0) < (argument.number or 0)
    #        raise TypeError("unorderable types")
    #
    #    def __repr__(self) -> str:
    #        """
    #        Gets interpreter representation.
    #        """
    #        return _format.get_repr(self)

    def _get_lilypond_format(self):
        return self.markup._get_lilypond_format()

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.markup.extend(tweaks)
        markup = self.markup
        markup = _new.new(markup, direction=_enums.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.after.markup.extend(markup_format_pieces)
        return bundle

    @property
    def markup(self) -> typing.Optional[_markups.Markup]:
        r"""
        Gets markup of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> string = abjad.lilypond(fingering.markup)
            >>> print(string)
            \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> string = abjad.lilypond(fingering.markup)
            >>> print(string)
            \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }

        """
        if self.number is None:
            return None
        string = rf"\override #'(circle-padding . 0.25) \circle \finger {self.number}"
        string = rf"\markup {{ {string} }}"
        markup = _markups.Markup(string)
        return markup


#    @property
#    def number(self) -> typing.Optional[int]:
#        """
#        Gets number of color fingering.
#
#        ..  container:: example
#
#            First color fingering:
#
#            >>> fingering = abjad.ColorFingering(1)
#            >>> fingering.number
#            1
#
#        ..  container:: example
#
#            Second color fingering:
#
#            >>> fingering = abjad.ColorFingering(2)
#            >>> fingering.number
#            2
#
#        """
#        return self._number
#
#    @property
#    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
#        r"""
#        """
#        return self._tweaks
