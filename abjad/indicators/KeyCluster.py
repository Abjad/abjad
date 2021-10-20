import dataclasses
import typing

from .. import bundle as _bundle
from .. import enums as _enums
from .. import markups as _markups


@dataclasses.dataclass
class KeyCluster:
    r"""
    Key cluster.

    ..  container:: example

        Default values:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

    ..  container:: example

        Includes flat markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_flat_markup=True)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Default behavior.

    ..  container:: example

        Does not include flat markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_flat_markup=False)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \natural
            }

    ..  container:: example

        Includes natural markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_natural_markup=True)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Does not include natural markup:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(include_natural_markup=False)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \flat
            }

    ..  container:: example

        Key cluster formats LilyPond overrides instead of tweaks:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord)
        >>> string = abjad.lilypond(chord)
        >>> print(string)
        \once \override Accidental.stencil = ##f
        \once \override AccidentalCautionary.stencil = ##f
        \once \override Arpeggio.X-offset = #-2
        \once \override NoteHead.stencil = #ly:text-interface::print
        \once \override NoteHead.text =
        \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
        <c' e' g' b' d'' f''>8
        ^ \markup \center-align \concat { \natural \flat }

        The reason for this is that chords contain multiple note-heads: if key cluster
        formatted tweaks instead of overrides, the five format commands shown above would
        need to be duplicated immediately before each note-head.

    ..  container:: example

        Positions markup up:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(markup_direction=abjad.Up)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                ^ \markup \center-align \concat { \natural \flat }
            }

        Positions markup down:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster(markup_direction=abjad.Down)
        >>> abjad.attach(key_cluster, chord)
        >>> staff = abjad.Staff([chord])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text =
                \markup \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                <c' e' g' b' d'' f''>8
                _ \markup \center-align \concat { \natural \flat }
            }

    """

    include_flat_markup: bool = True
    include_natural_markup: bool = True
    markup_direction: typing.Union[int, _enums.VerticalAlignment] = _enums.Up

    _is_dataclass = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        bundle.grob_overrides.append(
            "\\once \\override Accidental.stencil = ##f\n"
            "\\once \\override AccidentalCautionary.stencil = ##f\n"
            "\\once \\override Arpeggio.X-offset = #-2\n"
            "\\once \\override NoteHead.stencil = #ly:text-interface::print\n"
            "\\once \\override NoteHead.text =\n"
            "\\markup \\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25"
        )
        if self.include_flat_markup and self.include_natural_markup:
            string = r"\center-align \concat { \natural \flat }"
        elif self.include_flat_markup:
            string = r"\center-align \flat"
        else:
            string = r"\center-align \natural"
        markup = _markups.Markup(rf"\markup {string}", direction=self.markup_direction)
        markup_format_pieces = markup._get_format_pieces()
        bundle.after.markup.extend(markup_format_pieces)
        return bundle
