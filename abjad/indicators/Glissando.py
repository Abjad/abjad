import dataclasses
import typing

from .. import bundle as _bundle
from .. import overrides as _overrides


@dataclasses.dataclass
class Glissando:
    r"""
    LilyPond ``\glissando`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> glissando = abjad.Glissando()
        >>> abjad.tweak(glissando).color = "#blue"
        >>> abjad.attach(glissando, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    ..  container:: example

        >>> abjad.Glissando()
        Glissando(allow_repeats=False, allow_ties=False, parenthesize_repeats=False, stems=False, style=None, tweaks=None, zero_padding=False)

    ..  container:: example

        Tweaks;

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> glissando = abjad.Glissando()
        >>> abjad.tweak(glissando).color = "#blue"
        >>> abjad.attach(glissando, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set ``zero_padding=True`` when glissando formats with zero padding and no extra
        space for dots:

        >>> staff = abjad.Staff("d'8 d'4. d'4. d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=True,
        ...     zero_padding=True,
        ... )
        >>> for note in staff[1:]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                d'8
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8
            }

        >>> staff = abjad.Staff("c'8. d'8. e'8. f'8.")
        >>> abjad.glissando(
        ...     staff[:],
        ...     zero_padding=True,
        ... )
        >>> for note in staff[1:-1]:
        ...     abjad.override(note).NoteHead.transparent = True
        ...     abjad.override(note).NoteHead.X_extent = "#'(0 . 0)"
        ...
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'8.
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                e'8.
                - \abjad-zero-padding-glissando
                \glissando
                f'8.
            }

    """

    allow_repeats: bool = False
    allow_ties: bool = False
    parenthesize_repeats: bool = False
    stems: bool = False
    style: typing.Optional[str] = None
    tweaks: typing.Optional[_overrides.TweakInterface] = None
    zero_padding: bool = False

    _is_dataclass = True

    context = "Voice"
    persistent = True

    def __post_init__(self):
        self.tweaks = _overrides.TweakInterface.set_dataclass_tweaks(self, self.tweaks)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        strings = []
        if self.zero_padding:
            strings.append(r"- \abjad-zero-padding-glissando")
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            strings.extend(tweaks)
        strings.append(r"\glissando")
        bundle.after.spanner_starts.extend(strings)
        return bundle
