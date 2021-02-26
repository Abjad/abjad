import copy
import typing

from ..bundle import LilyPondFormatBundle
from ..markups import Markup
from ..new import new
from ..overrides import TweakInterface
from ..storage import StorageFormatManager


class RehearsalMark:
    r"""
    Rehearsal mark.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.RehearsalMark(number=1)
        >>> abjad.attach(mark, staff[0])
        >>> scheme = "#format-mark-box-alphabet"
        >>> abjad.setting(score).markFormatter = scheme
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            \with
            {
                markFormatter = #format-mark-box-alphabet
            }
            <<
                \new Staff
                {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_markup", "_number", "_tweaks")

    _context = "Score"

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        markup: typing.Union[Markup, str] = None,
        number: int = None,
        tweaks: TweakInterface = None,
    ) -> None:
        self._tweaks = None
        self._markup = markup
        self._number = number
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        r"""
        Copies rehearsal mark.

        >>> import copy

        ..  container:: example

            Preserves tweaks:

            >>> mark = abjad.RehearsalMark(number=1)
            >>> abjad.tweak(mark).color = "#red"
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \tweak color #red
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> mark = copy.copy(mark)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \tweak color #red
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }

        """
        mark_ = new(self)
        mark_._tweaks = copy.copy(self.tweaks)
        return mark_

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        r"""
        Gets string representation of rehearsal mark.

        ..  container:: example

            >>> mark = abjad.RehearsalMark(number=1)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }

            >>> str(mark)
            '\\mark #1'

        """
        return self._get_lilypond_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        if self.markup is not None:
            result = rf"\mark {self.markup}"
        elif self.number is not None:
            result = rf"\mark #{self.number}"
        else:
            result = r"\mark \default"
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(directed=False)
            bundle.opening.commands.extend(tweaks)
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Is ``'Score'``.

        ..  container:: example

            >>> abjad.RehearsalMark(number=1).context
            'Score'

        """
        return self._context

    @property
    def markup(self) -> typing.Union[Markup, str, None]:
        r"""
        Gets rehearsal mark markup.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold { \italic { A } }')
            >>> mark = abjad.RehearsalMark(markup=markup)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \mark \markup {
                        \bold
                            {
                                \italic
                                    {
                                        A
                                    }
                            }
                        }
                    c'4
                    d'4
                    e'4
                    f'4
                }

        """
        return self._markup

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets rehearsal mark number.

        ..  container:: example

            >>> abjad.RehearsalMark(number=1).number
            1

        """
        return self._number

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> note = abjad.Note("c'4")
            >>> mark = abjad.RehearsalMark(markup='A')
            >>> abjad.tweak(mark).color = "#blue"
            >>> abjad.attach(mark, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                \tweak color #blue
                \mark A
                c'4

        """
        return self._tweaks

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string) -> "RehearsalMark":
        """
        Makes rehearsal mark from ``string``.

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('A')
            RehearsalMark(number=1)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AA')
            RehearsalMark(number=27)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AB')
            RehearsalMark(number=28)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BA')
            RehearsalMark(number=53)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BB')
            RehearsalMark(number=54)

        """
        number = 0
        for place, letter in enumerate(reversed(string)):
            integer = ord(letter) - ord("A") + 1
            multiplier = 26 ** place
            integer *= multiplier
            number += integer
        return RehearsalMark(number=number)
