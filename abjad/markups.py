"""
Tools for modeling LilyPond's markup and postscript.
"""
import collections
import typing

from . import enums as _enums
from . import format as _format
from . import math as _math
from . import new as _new
from . import overrides as _overrides
from . import string as _string


class Markup:
    r"""
    LilyPond markup.

    ..  container:: example

        Initializes from string:

        >>> string = r'\markup \italic "Allegro assai"'
        >>> markup = abjad.Markup(string)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        \markup \italic "Allegro assai"

        >>> abjad.show(markup) # doctest: +SKIP

        >>> markup = abjad.Markup(r'\markup \italic "Allegro assai"', direction=abjad.Up)
        >>> markup = abjad.Markup(markup.string, direction=abjad.Down)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        _ \markup \italic "Allegro assai"

        >>> abjad.show(markup) # doctest: +SKIP

    ..  container:: example

        Attaches markup to score components:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> string = r'\markup \italic "Allegro assai"'
        >>> markup = abjad.Markup(string, direction=abjad.Up)
        >>> string = abjad.lilypond(markup)
        >>> print(string)
        ^ \markup \italic "Allegro assai"

        >>> abjad.attach(markup, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8
                ^ \markup \italic "Allegro assai"
                d'8
                e'8
                f'8
            }

    Set ``direction`` to ``Up``, ``Down``, ``"neutral"``, ``"^"``, ``"_"``, ``"-"`` or
    None.

    ..  container:: example

        Markup can be tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro", direction=abjad.Up)
        >>> abjad.attach(markup, staff[0], tag=abjad.Tag("RED:M1"))
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! RED
            %! M1
            ^ \markup \italic Allegro
            d'4
            e'4
            f'4
        }

    ..  container:: example

        Markup can be deactively tagged:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro", direction=abjad.Up)
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag=abjad.Tag("RED:M1"),
        ... )
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff, tags=True)
        >>> print(string)
        \new Staff
        {
            c'4
            %! RED
            %! M1
            %@% ^ \markup \italic Allegro
            d'4
            e'4
            f'4
        }

    ..  container:: example

        REGRESSION: make sure the first italic markup doesn't disappear after the second
        italic markup is attached:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r"\markup \italic Allegro", direction=abjad.Up)
        >>> markup_2 = abjad.Markup(r'\markup \italic "non troppo"', direction=abjad.Up)
        >>> abjad.attach(markup_1, staff[0])
        >>> abjad.attach(markup_2, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            c'4
            ^ \markup \italic Allegro
            ^ \markup \italic "non troppo"
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_annotation",
        "_string",
        "_direction",
        "_tweaks",
    )

    _private_attributes_to_copy = ("_tweaks",)

    ### INITIALIZER ###

    def __init__(
        self,
        string,
        *,
        direction: typing.Union[int, _enums.VerticalAlignment] = None,
        tweaks: _overrides.TweakInterface = None,
    ) -> None:
        self._annotation = None
        assert isinstance(string, str), repr(string)
        self._string = string
        direction_ = _string.String.to_tridirectional_ordinal_constant(direction)
        if direction_ is not None:
            assert isinstance(direction_, _enums.VerticalAlignment), repr(direction_)
        self._direction = direction_
        if tweaks is not None:
            assert isinstance(tweaks, _overrides.TweakInterface), repr(tweaks)
        self._tweaks = _overrides.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        r"""
        Copies markup.

        >>> import copy

        ..  container:: example

            >>> markup_1 = abjad.Markup(r"\markup Allegro assai", direction=abjad.Up)
            >>> markup_2 = copy.copy(markup_1)

            >>> markup_1
            Markup('\\markup Allegro assai', direction=Up)

            >>> markup_2
            Markup('\\markup Allegro assai', direction=Up)

            >>> markup_1 == markup_2
            True

            >>> markup_1 is markup_2
            False

        Returns new markup.
        """
        return _new.new(self)

    def __eq__(self, argument):
        r"""
        Is true markup equals ``argument``.

        ..  container:: example

            Without keywords:

            >>> markup_1 = abjad.Markup(r"\markup Allegro")
            >>> markup_2 = abjad.Markup(r"\markup Allegro")
            >>> markup_3 = abjad.Markup(r'\markup "Allegro assai"')

            >>> markup_1 == markup_1
            True
            >>> markup_1 == markup_2
            True
            >>> markup_1 == markup_3
            False
            >>> markup_2 == markup_1
            True
            >>> markup_2 == markup_2
            True
            >>> markup_2 == markup_3
            False
            >>> markup_3 == markup_1
            False
            >>> markup_3 == markup_2
            False
            >>> markup_3 == markup_3
            True

        ..  container:: example

            With keywords:

            >>> markup_1 = abjad.Markup(r"\markup Allegro")
            >>> markup_2 = abjad.Markup(r"\markup Allegro", direction=abjad.Up)

            >>> markup_1 == markup_1
            True
            >>> markup_1 == markup_2
            False
            >>> markup_2 == markup_1
            False
            >>> markup_2 == markup_2
            True

        Returns new markup.
        """
        return _format.compare_objects(self, argument)

    def __hash__(self):
        r"""
        Hashes markup.

        ..  container:: example

            Without keywords:

            >>> hash_1 = hash(abjad.Markup(r"\markup Allegro"))
            >>> hash_2 = hash(abjad.Markup(r"\markup Allegro"))
            >>> hash_3 = hash(abjad.Markup(r'\markup "Allegro assai"'))

            >>> hash_1 == hash_1
            True
            >>> hash_1 == hash_2
            True
            >>> hash_1 == hash_3
            False
            >>> hash_2 == hash_1
            True
            >>> hash_2 == hash_2
            True
            >>> hash_2 == hash_3
            False
            >>> hash_3 == hash_1
            False
            >>> hash_3 == hash_2
            False
            >>> hash_3 == hash_3
            True

        ..  container:: example

            With keywords:

            >>> hash_1 = hash(abjad.Markup(r"\markup Allegro"))
            >>> string = r"\markup Allegro"
            >>> hash_2 = hash(abjad.Markup(string, direction=abjad.Up))

            >>> hash_1 == hash_1
            True
            >>> hash_1 == hash_2
            False
            >>> hash_2 == hash_1
            False
            >>> hash_2 == hash_2
            True

        """
        return hash(self.__class__.__name__ + str(self))

    def __lt__(self, argument):
        r"""
        Is true when markup string compare less than ``argument`` string.

        ..  container:: example

            >>> markup_1 = abjad.Markup(r"\markup Allegro")
            >>> markup_2 = abjad.Markup(r"\markup assai")

            >>> markup_1 < markup_2
            True
            >>> markup_2 < markup_1
            False

        Raises type error when ``argument`` is not markup.

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            raise TypeError(f"can only compare markup to markup: {argument!r}.")
        return self.string < argument.string

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    def __str__(self):
        r"""
        Gets string representation of markup.

        ..  container:: example

            >>> markup = abjad.Markup(rf'\markup \italic "Allegro assai"')
            >>> print(str(markup))
            \markup \italic "Allegro assai"

            >>> abjad.show(markup) # doctest: +SKIP

        Returns string.
        """
        return self._get_lilypond_format()

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        tweaks = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
        direction = ""
        if self.direction is not None:
            direction = _string.String.to_tridirectional_lilypond_symbol(self.direction)
        if direction:
            string = rf"{direction} {self.string}"
        else:
            string = self.string
        return tweaks + [string]

    def _get_format_specification(self):
        result = _format._inspect_signature(self)
        signature_keyword_names = result[1]
        return _format.FormatSpecification(
            storage_format_keyword_names=list(signature_keyword_names),
        )

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())

    ### PUBLIC PROPERTIES ###

    @property
    def string(self) -> str:
        r"""
        Gets string of markup.

        ..  container:: example

            Initializes string positionally:

            >>> abjad.Markup(r"\markup Allegro")
            Markup('\\markup Allegro')

            Initializes string from keyword:

            >>> abjad.Markup(r"\markup Allegro")
            Markup('\\markup Allegro')

        """
        assert isinstance(self._string, str), repr(self._string)
        return self._string

    @property
    def direction(self) -> typing.Optional[_enums.VerticalAlignment]:
        r"""
        Gets direction of markup.

        ..  container:: example

            With ``direction`` unset:

            >>> markup = abjad.Markup(r"\markup Allegro")
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \markup Allegro

            With ``direction=abjad.Up``:

            >>> string = r"\markup Allegro"
            >>> markup = abjad.Markup(string, direction=abjad.Up)
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                ^ \markup Allegro


            With ``direction=abjad.Down``:

            >>> string = r"\markup Allegro"
            >>> markup = abjad.Markup(string, direction=abjad.Down)
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                _ \markup Allegro

        ..  container:: example

            REGRESSSION #806. Markup preserves tweaks when ``direction=None``:

            >>> markup = abjad.Markup(r"\markup Allegro")
            >>> abjad.tweak(markup).color = "#red"
            >>> note = abjad.Note("c'4")
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                - \tweak color #red
                - \markup Allegro

        """
        return self._direction

    @property
    def tweaks(self) -> typing.Optional[_overrides.TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> string = r'\markup \bold "Allegro assai"'
            >>> markup = abjad.Markup(string, direction=abjad.Up)
            >>> abjad.tweak(markup).color = "#blue"
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    ^ \markup \bold "Allegro assai"
                    d'4
                    e'4
                    f'4
                }

            REGRESSION: tweaks format even markup has no direction:

            >>> string = r'\markup \bold "Allegro assai"'
            >>> markup = abjad.Markup(string)
            >>> abjad.tweak(markup).color = "#blue"
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    - \markup \bold "Allegro assai"
                    d'4
                    e'4
                    f'4
                }

        """
        return self._tweaks


def _format_postscript_argument(argument):
    if isinstance(argument, str):
        if argument.startswith("/"):
            return argument
        return f"({argument})"
    elif isinstance(argument, collections.abc.Sequence):
        if not argument:
            return "[ ]"
        string = " ".join(_format_postscript_argument(_) for _ in argument)
        return f"[ {string} ]"
    elif isinstance(argument, bool):
        return str(argument).lower()
    elif isinstance(argument, (int, float)):
        argument = _math.integer_equivalent_number_to_integer(argument)
        return str(argument)
    return str(argument)


_fpa = _format_postscript_argument
