# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class KeyCluster(AbjadValueObject):
    r'''Key cluster.

    ::

        >>> import abjad

    ..  container:: example

        
        Default values:

        ::

            >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = abjad.KeyCluster()
            >>> abjad.attach(key_cluster, chord)
            >>> show(chord) # doctest: +SKIP

        ..  docs::

            >>> f(chord)
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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_black_keys',
        '_include_white_keys',
        '_markup_direction',
        '_suppress_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        include_black_keys=True,
        include_white_keys=True,
        markup_direction=Up,
        suppress_markup=False,
        ):
        assert include_black_keys or include_white_keys
        self._include_black_keys = bool(include_black_keys)
        self._include_white_keys = bool(include_white_keys)
        assert markup_direction in (Up, Center, Down)
        self._markup_direction = markup_direction
        self._suppress_markup = bool(suppress_markup)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.grob_overrides.append(
            '\\once \\override Accidental.stencil = ##f\n'
            '\\once \\override AccidentalCautionary.stencil = ##f\n'
            '\\once \\override Arpeggio.X-offset = #-2\n'
            '\\once \\override NoteHead.stencil = #ly:text-interface::print\n'
            '\\once \\override NoteHead.text = \markup {\n'
            "\t\\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25\n"
            '}'
            )
        if not self.suppress_markup:
            if self.include_black_keys and self.include_white_keys:
                string = r'\center-align \concat { \natural \flat }'
            elif self.include_black_keys:
                string = r'\center-align \flat'
            else:
                string = r'\center-align \natural'
            markup = abjad.Markup(
                string,
                direction=self.markup_direction,
                )
            markup_format_pieces = markup._get_format_pieces()
            bundle.right.markup.extend(markup_format_pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def include_black_keys(self):
        r'''Is true if key cluster includes black keys.

        ..  container:: example

            Includes flat markup:

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     include_black_keys=True,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     include_black_keys=False,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

        Set to true or false.
        '''
        return self._include_black_keys

    @property
    def include_white_keys(self):
        r'''Is true if key cluster includes white keys.

        ..  container:: example

            Includes natural markup:

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     include_white_keys=True,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     include_white_keys=False,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

        Set to true or false.
        '''
        return self._include_white_keys

    @property
    def markup_direction(self):
        r'''Gets markup direction.

        ..  container:: example

            Positions markup up:

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     markup_direction=Up,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(
                ...     markup_direction=Down,
                ...     )
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

        Set to up, down or center.
        '''
        return self._markup_direction

    @property
    def suppress_markup(self):
        r'''Is true if key cluster suppresses key markup.

        ..  container:: example

            Does not suppress markup:

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(suppress_markup=False)
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
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

            Does not suppress markup:

            ::

                >>> chord = abjad.Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = abjad.KeyCluster(suppress_markup=True)
                >>> abjad.attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  docs::

                >>> f(chord)
                \once \override Accidental.stencil = ##f
                \once \override AccidentalCautionary.stencil = ##f
                \once \override Arpeggio.X-offset = #-2
                \once \override NoteHead.stencil = #ly:text-interface::print
                \once \override NoteHead.text = \markup {
                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                }
                <c' e' g' b' d'' f''>8

        ..  todo:: Remove?

        Set to true or false.
        '''
        return self._suppress_markup
