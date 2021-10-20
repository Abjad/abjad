import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import overrides as _overrides
from .. import string as _string


@dataclasses.dataclass
class Articulation:
    r"""
    Articulation.

    ..  container:: example

        Initializes from string:

        >>> abjad.Articulation("staccato")
        Articulation(name='staccato', direction=None, tweaks=None)

        >>> abjad.Articulation(".")
        Articulation(name='.', direction=None, tweaks=None)

        With direction:

        >>> abjad.Articulation("staccato", direction=abjad.Up)
        Articulation(name='staccato', direction=Up, tweaks=None)

    ..  container:: example

        New:

        >>> abjad.new(abjad.Articulation("."))
        Articulation(name='.', direction=None, tweaks=None)

    ..  container:: example

        Tweaks:

        >>> note = abjad.Note("c'4")
        >>> articulation = abjad.Articulation("marcato")
        >>> abjad.tweak(articulation).color = "#blue"
        >>> abjad.attach(articulation, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            c'4
            - \tweak color #blue
            - \marcato

    """

    name: str
    direction: typing.Union[int, _enums.VerticalAlignment, None] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None

    _is_dataclass = True

    _shortcut_to_word = {
        "^": "marcato",
        "+": "stopped",
        "-": "tenuto",
        "|": "staccatissimo",
        ">": "accent",
        ".": "staccato",
        "_": "portato",
    }

    def __post_init__(self):
        assert isinstance(self.name, str), repr(self.name)
        self.direction = _string.String.to_tridirectional_ordinal_constant(
            self.direction
        )
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    # TODO: eventually remove
    def __str__(self) -> str:
        """
        Gets string representation of articulation.
        """
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = _string.String("-")
            else:
                direction_ = _string.String.to_tridirectional_lilypond_symbol(
                    self.direction
                )
                assert isinstance(direction_, _string.String), repr(direction)
                direction = direction_
            return fr"{direction} \{string}"
        else:
            return ""

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle
