import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MetricModulation(AbjadValueObject):
    r'''Metric modulation.

    ..  container:: example

        With notes:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=abjad.Note("c'4."),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4.
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }

    ..  container:: example

        With tuplets:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Tuplet((4, 5), "c'4"),
        ...     right_rhythm=abjad.Note("c'4"),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    \tweak edge-height #'(0.7 . 0)
                                    \times 4/5 {
                                        c'4
                                    }
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }

    ..  container:: example

        With tuplets again:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c16."),
        ...     right_rhythm=abjad.Tuplet((2, 3), "c8"),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c16.
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    \tweak edge-height #'(0.7 . 0)
                                    \times 2/3 {
                                        c8
                                    }
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }

    ..  container:: example

        With ties:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(5, 16)])
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=notes,
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4 ~
                                    c'16
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }

    ..  container:: example

        With ties and tuplets:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(5, 16)])
        >>> tuplet = abjad.Tuplet((2, 3), notes)
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=tuplet,
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    \tweak edge-height #'(0.7 . 0)
                                    \times 2/3 {
                                        c'4 ~
                                        c'16
                                    }
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }


    ..  container:: example

        Attach metric modulations to generate score output:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 e'4 d'4")
        >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0])
        >>> score = abjad.Score([staff])

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c4"),
        ...     right_rhythm=abjad.Note("c8."),
        ...     )
        >>> abjad.attach(metric_modulation, staff[3])
        >>> abjad.override(staff).text_script.staff_padding = 2.5

        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score <<
                \new Staff \with {
                    \override TextScript.staff-padding = #2.5
                } {
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    f'4
                        ^ \markup {
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c4
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            =
                            \hspace
                                #-0.5
                            \scale
                                #'(0.75 . 0.75)
                                \score
                                    {
                                        \new Score \with {
                                            \override SpacingSpanner.spacing-increment = #0.5
                                            proportionalNotationDuration = ##f
                                        } <<
                                            \new RhythmicStaff \with {
                                                \remove Time_signature_engraver
                                                \remove Staff_symbol_engraver
                                                \override Stem.direction = #up
                                                \override Stem.length = #5
                                                \override TupletBracket.bracket-visibility = ##t
                                                \override TupletBracket.direction = #up
                                                \override TupletBracket.padding = #1.25
                                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                tupletFullLength = ##t
                                            } {
                                                c8.
                                            }
                                        >>
                                        \layout {
                                            indent = #0
                                            ragged-right = ##t
                                        }
                                    }
                            }
                    e'4
                    d'4
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_left_markup',
        '_left_rhythm',
        '_right_markup',
        '_right_rhythm',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        left_rhythm=None,
        right_rhythm=None,
        left_markup=None,
        right_markup=None,
        ):
        import abjad
        self._context = 'Score'
        left_rhythm = left_rhythm or abjad.Note('c4')
        right_rhythm = right_rhythm or abjad.Note('c4')
        left_rhythm = self._initialize_rhythm(left_rhythm)
        self._left_rhythm = left_rhythm
        right_rhythm = self._initialize_rhythm(right_rhythm)
        self._right_rhythm = right_rhythm
        self._right_rhythm = right_rhythm
        if left_markup is not None:
            assert isinstance(left_markup, abjad.Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, abjad.Markup)
        self._right_markup = right_markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is another metric modulation with the same
        ratio as this metric modulation. Otherwise false.

        ..  container:: example

            >>> metric_modulation_1 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation_2 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )
            >>> maker = abjad.NoteMaker()
            >>> notes = maker([0], [(5, 16)])
            >>> metric_modulation_3 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=notes,
            ...     )

            >>> metric_modulation_1.ratio
            Ratio((2, 3))
            >>> metric_modulation_2.ratio
            Ratio((2, 3))
            >>> metric_modulation_3.ratio
            Ratio((4, 5))

            >>> metric_modulation_1 == metric_modulation_1
            True
            >>> metric_modulation_1 == metric_modulation_2
            True
            >>> metric_modulation_1 == metric_modulation_3
            False

            >>> metric_modulation_2 == metric_modulation_1
            True
            >>> metric_modulation_2 == metric_modulation_2
            True
            >>> metric_modulation_2 == metric_modulation_3
            False

            >>> metric_modulation_3 == metric_modulation_1
            False
            >>> metric_modulation_3 == metric_modulation_2
            False
            >>> metric_modulation_3 == metric_modulation_3
            True

        Returns true or false.
        '''
        # custom definition because input rhythms don't compare:
        if isinstance(argument, type(self)):
            if self.ratio == argument.ratio:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )

            >>> abjad.f(metric_modulation)
            abjad.MetricModulation(
                left_rhythm=abjad.Selection(
                    [
                        abjad.Note("c'4"),
                        ]
                    ),
                right_rhythm=abjad.Selection(
                    [
                        abjad.Note("c'4."),
                        ]
                    ),
                )

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        superclass = super(MetricModulation, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes metric modulation.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(MetricModulation, self).__hash__()

    def __illustrate__(self):
        r'''Illustrates metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), "c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> abjad.show(metric_modulation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = metric_modulation.__illustrate__()
                >>> metric_modulation = lilypond_file.items[-1]
                >>> print(format(metric_modulation))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        \tweak edge-height #'(0.7 . 0)
                                        \times 2/3 {
                                            c'4
                                        }
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    =
                    \hspace
                        #-0.5
                    \scale
                        #'(0.75 . 0.75)
                        \score
                            {
                                \new Score \with {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                } <<
                                    \new RhythmicStaff \with {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    } {
                                        c'4.
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                    }

        Returns LilyPond file.
        '''
        import abjad
        lilypond_file = abjad.LilyPondFile.new()
        lilypond_file.header_block.tagline = False
        lilypond_file.items.append(self._get_markup())
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )

            >>> print(str(metric_modulation))
            \markup {
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    \tweak edge-height #'(0.7 . 0)
                                    \times 2/3 {
                                        c'4
                                    }
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                =
                \hspace
                    #-0.5
                \scale
                    #'(0.75 . 0.75)
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                }

        Returns string.
        '''
        return str(self._get_markup())

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_left_markup(self):
        import abjad
        if self.left_markup is not None:
            return self.left_markup
        markup = abjad.Duration._to_score_markup(self.left_rhythm)
        return markup

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        markup = self._get_markup()
        markup = abjad.new(markup, direction=abjad.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    def _get_markup(self, music_scale_pair=(0.75, 0.75)):
        import abjad
        if music_scale_pair is not None:
            assert isinstance(music_scale_pair, collections.Iterable)
            music_scale_pair = tuple(music_scale_pair)
        left_markup = self._get_left_markup()
        if music_scale_pair:
            left_markup = left_markup.scale(music_scale_pair)
        equal = abjad.Markup('=')
        right_space = abjad.Markup.hspace(-0.5)
        right_markup = self._get_right_markup()
        if music_scale_pair:
            right_markup = right_markup.scale(music_scale_pair)
        markup = left_markup + equal + right_space + right_markup
        return markup

    def _get_right_markup(self):
        import abjad
        if self.right_markup is not None:
            return self.right_markup
        markup = abjad.Duration._to_score_markup(self.right_rhythm)
        return markup

    def _initialize_rhythm(self, rhythm):
        import abjad
        if isinstance(rhythm, abjad.Component):
            selection = abjad.select([rhythm])
        elif isinstance(rhythm, abjad.Selection):
            selection = rhythm
        else:
            message = 'rhythm must be duration, component or selection: {!r}.'
            message = message.format(rhythm)
            raise TypeError(message)
        assert isinstance(selection, abjad.Selection)
        return selection

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.context
            'Score'

        Returns context or string.
        '''
        return self._context

    @property
    def left_markup(self):
        r'''Gets left markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.left_markup

        Returns markup or none.
        '''
        return self._left_markup

    @property
    def left_rhythm(self):
        r'''Gets left rhythm of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.left_rhythm
            Selection([Note("c'4")])

        Returns selection.
        '''
        return self._left_rhythm

    @property
    def ratio(self):
        r'''Gets ratio of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )
            >>> metric_modulation.ratio
            Ratio((2, 3))

        Returns ratio.
        '''
        import abjad
        left_duration = abjad.inspect(self.left_rhythm).get_duration()
        right_duration = abjad.inspect(self.right_rhythm).get_duration()
        duration = left_duration / right_duration
        ratio = abjad.Ratio(duration.pair)
        return ratio

    @property
    def right_markup(self):
        r'''Gets right markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.right_markup

        Returns markup or none.
        '''
        return self._right_markup

    @property
    def right_rhythm(self):
        r'''Gets right tempo of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.right_rhythm
            Selection([Note("c'4.")])

        Returns selection.
        '''
        return self._right_rhythm
