# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class KeyCluster(AbjadValueObject):
    r'''A key cluster indicator.

    ..  container:: example

        
        **Example 1.** Default values:

        ::

            >>> chord = Chord("<c' e' g' b' d'' f''>8")
            >>> key_cluster = indicatortools.KeyCluster()
            >>> attach(key_cluster, chord)
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
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
        '_default_scope',
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
        self._default_scope = None
        assert include_black_keys or include_white_keys
        self._include_black_keys = bool(include_black_keys)
        self._include_white_keys = bool(include_white_keys)
        assert markup_direction in (Up, Center, Down)
        self._markup_direction = markup_direction
        self._suppress_markup = bool(suppress_markup)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import markuptools
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.grob_overrides.append(
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
            markup = markuptools.Markup(
                string,
                direction=self.markup_direction,
                )
            markup_format_pieces = markup._get_format_pieces()
            lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gest default scope of key cluster indicator.

        ..  container:: example

            ::

                >>> key_cluster = indicatortools.KeyCluster()
                >>> key_cluster.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def include_black_keys(self):
        r'''Is true if key cluster includes black keys.

        ..  container:: example

            **Example 1.** Includes flat markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     include_black_keys=True,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 2.** Does not include flat markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     include_black_keys=False,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 1.** Includes natural markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     include_white_keys=True,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 2.** Does not include natural markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     include_white_keys=False,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 1.** Positions markup up:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     markup_direction=Up,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 2.** Positions markup down:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     markup_direction=Down,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 1.** Does not suppress markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     suppress_markup=False,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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

            **Example 2.** Does not suppress markup:

            ::

                >>> chord = Chord("<c' e' g' b' d'' f''>8")
                >>> key_cluster = indicatortools.KeyCluster(
                ...     suppress_markup=True,
                ...     )
                >>> attach(key_cluster, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
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
