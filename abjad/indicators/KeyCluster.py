from abjad import enums
from abjad.markups import Markup
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class KeyCluster(AbjadValueObject):
    r"""
    Key cluster.

    ..  container:: example

        Default values:

        >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = abjad.KeyCluster()
        >>> abjad.attach(key_cluster, chord)
        >>> abjad.show(chord) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(chord)
            \once \override Accidental.stencil = ##f
            \once \override AccidentalCautionary.stencil = ##f
            \once \override Arpeggio.X-offset = #-2
            \once \override NoteHead.stencil = #ly:text-interface::print
            \once \override NoteHead.text = \markup {
            	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
            }
            <c' e' g' b' d'' f''>8
            ^ \markup {
                \center-align
                    \concat
                        {
                            \natural
                            \flat
                        }
                }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_hide',
        '_include_black_keys',
        '_include_white_keys',
        '_markup_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        include_black_keys: bool = True,
        include_white_keys: bool = True,
        hide: bool = False,
        markup_direction: enums.VerticalAlignment = enums.Up,
        ) -> None:
        assert include_black_keys or include_white_keys
        self._include_black_keys = bool(include_black_keys)
        self._include_white_keys = bool(include_white_keys)
        assert markup_direction in (enums.Up, enums.Center, enums.Down)
        self._markup_direction = markup_direction
        self._hide = bool(hide)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        bundle.grob_overrides.append(
            '\\once \\override Accidental.stencil = ##f\n'
            '\\once \\override AccidentalCautionary.stencil = ##f\n'
            '\\once \\override Arpeggio.X-offset = #-2\n'
            '\\once \\override NoteHead.stencil = #ly:text-interface::print\n'
            '\\once \\override NoteHead.text = \markup {\n'
            "\t\\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25\n"
            '}'
            )
        if not self.hide:
            if self.include_black_keys and self.include_white_keys:
                string = r'\center-align \concat { \natural \flat }'
            elif self.include_black_keys:
                string = r'\center-align \flat'
            else:
                string = r'\center-align \natural'
            markup = Markup(
                string,
                direction=self.markup_direction,
                )
            markup_format_pieces = markup._get_format_pieces()
            bundle.after.markup.extend(markup_format_pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def hide(self) -> bool:
        r"""
        Is true if key cluster hidees key markup.

        ..  container:: example

            Does not hide markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(hide=False)
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \concat
                            {
                                \natural
                                \flat
                            }
                    }

            Default behavior.

        ..  container:: example

            Does not hide markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(hide=True)
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8

        ..  todo:: Remove?

        """
        return self._hide

    @property
    def include_black_keys(self) -> bool:
        r"""
        Is true if key cluster includes black keys.

        ..  container:: example

            Includes flat markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     include_black_keys=True,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \concat
                            {
                                \natural
                                \flat
                            }
                    }

            Default behavior.

        ..  container:: example

            Does not include flat markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     include_black_keys=False,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \natural
                    }

        ..  todo:: Rename to ``include_flat_markup``.

        """
        return self._include_black_keys

    @property
    def include_white_keys(self) -> bool:
        r"""
        Is true if key cluster includes white keys.

        ..  container:: example

            Includes natural markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     include_white_keys=True,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \concat
                            {
                                \natural
                                \flat
                            }
                    }

            Default behavior.

        ..  container:: example

            Does not include natural markup:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     include_white_keys=False,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \flat
                    }

        ..  todo:: Rename to ``include_natural_markup``.

        """
        return self._include_white_keys

    @property
    def markup_direction(self) -> enums.VerticalAlignment:
        r"""
        Gets markup direction.

        ..  container:: example

            Positions markup up:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     markup_direction=abjad.Up,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                ^ \markup {
                    \center-align
                        \concat
                            {
                                \natural
                                \flat
                            }
                    }

            Default behavior.

        ..  container:: example

            Positions markup down:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster(
            ...     markup_direction=abjad.Down,
            ...     )
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.show(chord) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8
                _ \markup {
                    \center-align
                        \concat
                            {
                                \natural
                                \flat
                            }
                    }

        """
        return self._markup_direction

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on key cluster.

        ..  container:: example

            Key cluster formats LilyPond overrides instead of tweaks:

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster()
            >>> abjad.attach(key_cluster, chord)
            >>> abjad.f(chord)
            \once \override Accidental.stencil = ##f
            \once \override AccidentalCautionary.stencil = ##f
            \once \override Arpeggio.X-offset = #-2
            \once \override NoteHead.stencil = #ly:text-interface::print
            \once \override NoteHead.text = \markup {
                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
            }
            <c' e' g' b' d'' f''>8
            ^ \markup {
                \center-align
                    \concat
                        {
                            \natural
                            \flat
                        }
                }

            The reason for this is that chords contain multiple note-heads: if
            key cluster formatted tweaks instead of overrides, the five format
            commands shown above would need to be duplicated immediately before
            each note-head.

        """
        pass
