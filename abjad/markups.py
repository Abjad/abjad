"""
Markup.
"""
import copy
import dataclasses
import typing

from . import string as _string
from . import tweaks as tweaksmodule


@dataclasses.dataclass(order=True, slots=True, unsafe_hash=True)
class Markup:
    r"""
    LilyPond markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> markup = abjad.Markup(r'\markup \italic "Allegro assai"')
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
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

    ..  container:: example

        Tweak markup like this:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\markup \bold "Allegro assai"')
        >>> abjad.tweak(markup, r"- \tweak color #blue")
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
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

        Works even when markup has no direction:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r'\markup \bold "Allegro assai"')
        >>> abjad.tweak(markup, r"- \tweak color #blue")
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

        Tag markup like this:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro")
        >>> abjad.attach(markup, staff[0], direction=abjad.UP, tag=abjad.Tag("RED:M1"))
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

        Tag deactivated markup like this:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup(r"\markup \italic Allegro")
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     direction=abjad.UP,
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

        REGRESSION: markup 1 doesn't disappear after markup 2 is attached:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup_1 = abjad.Markup(r"\markup \italic Allegro")
        >>> markup_2 = abjad.Markup(r'\markup \italic "non troppo"')
        >>> abjad.attach(markup_1, staff[0], direction=abjad.UP)
        >>> abjad.attach(markup_2, staff[0], direction=abjad.UP)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

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

        Tweak markup like this:

        >>> markup = abjad.Markup(r'\markup \bold "Allegro assai"')
        >>> abjad.tweak(markup, r"- \tweak color #blue")
        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(markup, staff[0], direction=abjad.UP)
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

        Works even when markup has no direction:

        >>> markup = abjad.Markup(r'\markup \bold "Allegro assai"')
        >>> abjad.tweak(markup, r"- \tweak color #blue")
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

    string: str
    tweaks: tuple[tweaksmodule.Tweak, ...] = dataclasses.field(
        default_factory=tuple, compare=False
    )

    directed: typing.ClassVar[bool] = True
    post_event: typing.ClassVar[bool] = True

    def __post_init__(self):
        self.tweaks = tuple(tweaksmodule.Tweak(_) for _ in self.tweaks)

    def __copy__(self, *arguments):
        result = type(self)(string=self.string)
        result.tweaks = tuple(list(copy.deepcopy(self.tweaks)))
        return result

    def _get_format_pieces(self, *, wrapper=None):
        tweaks = []
        for tweak in sorted(self.tweaks):
            strings = tweak._list_contributions()
            tweaks.extend(strings)
        if wrapper:
            direction = wrapper.direction or "-"
            direction = _string.to_tridirectional_lilypond_symbol(direction)
            string = rf"{direction} {self.string}"
        else:
            string = self.string
        return tweaks + [string]

    def _get_lilypond_format(self, *, wrapper=None):
        pieces = self._get_format_pieces(wrapper=wrapper)
        return "\n".join(pieces)
