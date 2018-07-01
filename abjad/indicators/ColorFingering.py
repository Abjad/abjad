import functools
import typing
from abjad import enums
from abjad import mathtools
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.markups import Markup
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.top.new import new


@functools.total_ordering
class ColorFingering(AbjadValueObject):
    r"""
    Color fingering.

    ..  container:: example

        First color fingering:

        >>> fingering = abjad.ColorFingering(1)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
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

            >>> abjad.f(note)
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

    __slots__ = (
        '_number',
        '_tweaks',
        )

    _format_slot = 'after'

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        number: int = None,
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        if number is not None:
            assert mathtools.is_positive_integer(number)
        self._number = number
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ##

    def __format__(self, format_specification='') -> str:
        r"""
        Formats color fingering.

        Set ``format_specification`` to ``''``, ``'lilypond'`` or
        ``'storage'``. Interprets ``''`` equal to ``'storage'``.

        ..  container:: example

            >>> fingering = abjad.ColorFingering(1)
            >>> abjad.f(fingering)
            abjad.ColorFingering(
                number=1,
                )

        """
        if format_specification == 'lilypond':
            return self._get_lilypond_format()
        return super().__format__(
            format_specification=format_specification
            )

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
        raise TypeError('unorderable types')

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return format(self.markup, 'lilypond')

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
            >>> print(format(fingering.markup, 'lilypond'))
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
            >>> print(format(fingering.markup, 'lilypond'))
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
        markup = Markup(str(self.number))
        markup = markup.finger()
        markup = markup.circle()
        markup = markup.override(('circle-padding', 0.25))
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
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> fingering = abjad.ColorFingering(1)
            >>> abjad.tweak(fingering).color = 'blue'
            >>> abjad.attach(fingering, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> fingering = abjad.ColorFingering(1, tweaks=[('color', 'blue')])
            >>> abjad.attach(fingering, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
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
