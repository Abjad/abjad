"""
Tools for modeling LilyPond markup.
"""
import collections
import dataclasses
import typing

from . import enums as _enums
from . import math as _math
from . import overrides as _overrides
from . import string as _string


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
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

    ..  container:: example

        Works with tweaks:

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

        Even if markup has no direction:

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

    ..  container:: example

        Equality:

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

    ..  container:: example

        Unsafe hash:

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


    ..  container:: example

        Order:

        >>> markup_1 = abjad.Markup(r"\markup Allegro")
        >>> markup_2 = abjad.Markup(r"\markup assai")

        >>> markup_1 < markup_2
        True
        >>> markup_2 < markup_1
        False

    ..  container:: example

        Copy:

        >>> import copy
        >>> markup_1 = abjad.Markup(r"\markup Allegro assai", direction=abjad.Up)
        >>> markup_2 = copy.copy(markup_1)

        >>> markup_1
        Markup(string='\\markup Allegro assai', direction=Up, tweaks=None)

        >>> markup_2
        Markup(string='\\markup Allegro assai', direction=Up, tweaks=None)

        >>> markup_1 == markup_2
        True

        >>> markup_1 is markup_2
        False

    ..  container:: example

        String:

        >>> markup = abjad.Markup(rf'\markup \italic "Allegro assai"')
        >>> print(str(markup))
        \markup \italic "Allegro assai"

        >>> abjad.show(markup) # doctest: +SKIP

    """

    string: str
    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None
    _annotation: typing.Any = dataclasses.field(default=None, init=False, repr=False)

    def __post_init__(self):
        self._annotation = None
        self.direction = _string.to_tridirectional_ordinal_constant(self.direction)
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    _is_dataclass = True

    # TODO: remove eventually
    def __str__(self) -> str:
        """
        Gets string representation of markup.
        """
        return self._get_lilypond_format()

    def _get_format_pieces(self):
        tweaks = []
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
        direction = ""
        if self.direction is not None:
            direction = _string.to_tridirectional_lilypond_symbol(self.direction)
        if direction:
            string = rf"{direction} {self.string}"
        else:
            string = self.string
        return tweaks + [string]

    def _get_lilypond_format(self):
        return "\n".join(self._get_format_pieces())


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
