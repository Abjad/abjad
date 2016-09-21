# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools.new import new


class MetricModulation(AbjadValueObject):
    r'''A metric modulation.

    ..  container:: example

        **Example 1.** With notes:

        ::

            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note("c'4"),
            ...     right_rhythm=Note("c'4."),
            ...     )

        ::

            >>> show(metric_modulation) # doctest: +SKIP

        ..  doctest::

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

        **Example 2.** With tuplets:

        ::

            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Tuplet((4, 5), "c'4"),
            ...     right_rhythm=Note("c'4"),
            ...     )

        ::

            >>> show(metric_modulation) # doctest: +SKIP

        ..  doctest::

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

        **Example 3.** With tuplets again:

        ::

            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note("c16."),
            ...     right_rhythm=Tuplet((2, 3), "c8"),
            ...     )

        ::

            >>> show(metric_modulation) # doctest: +SKIP

        ..  doctest::

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

        **Example 4.** With ties:

        ::

            >>> notes = scoretools.make_notes([0], [Duration(5, 16)])
            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note("c'4"),
            ...     right_rhythm=notes,
            ...     )

        ::

            >>> show(metric_modulation) # doctest: +SKIP

        ..  doctest::

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

        **Example 5.** With ties and tuplets:

        ::

            >>> notes = scoretools.make_notes([0], [Duration(5, 16)])
            >>> tuplet = Tuplet((2, 3), notes)
            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note("c'4"),
            ...     right_rhythm=tuplet,
            ...     )

        ::

            >>> show(metric_modulation) # doctest: +SKIP

        ..  doctest::

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

        **Example 6.** Attach metric modulations to generate score output:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4 e'4 d'4")
            >>> attach(TimeSignature((3, 4)), staff)
            >>> score = Score([staff])

        ::

            >>> metric_modulation = indicatortools.MetricModulation(
            ...     left_rhythm=Note("c4"),
            ...     right_rhythm=Note("c8."),
            ...     )
            >>> attach(metric_modulation, staff[3])
            >>> override(staff).text_script.staff_padding = 2.5

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
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
        '_default_scope',
        '_left_markup',
        '_left_rhythm',
        '_right_markup',
        '_right_rhythm',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        left_rhythm=None,
        right_rhythm=None,
        left_markup=None,
        right_markup=None,
        ):
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        self._default_scope = None
        left_rhythm = left_rhythm or scoretools.Note('c4')
        right_rhythm = right_rhythm or scoretools.Note('c4')
        left_rhythm = self._initialize_rhythm(left_rhythm)
        self._left_rhythm = left_rhythm
        right_rhythm = self._initialize_rhythm(right_rhythm)
        self._right_rhythm = right_rhythm
        self._right_rhythm = right_rhythm
        if left_markup is not None:
            assert isinstance(left_markup, markuptools.Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, markuptools.Markup)
        self._right_markup = right_markup

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true `expr` is another metric modulation with the same ratio as
        this metric modulation. Otherwise false.

        ..  container:: example

            ::

                >>> metric_modulation_1 = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation_2 = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )
                >>> notes = scoretools.make_notes([0], [Duration(5, 16)])
                >>> metric_modulation_3 = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=notes,
                ...     )

            ::

                >>> metric_modulation_1.ratio
                Ratio((2, 3))
                >>> metric_modulation_2.ratio
                Ratio((2, 3))
                >>> metric_modulation_3.ratio
                Ratio((4, 5))

            ::

                >>> metric_modulation_1 == metric_modulation_1
                True
                >>> metric_modulation_1 == metric_modulation_2
                True
                >>> metric_modulation_1 == metric_modulation_3
                False

            ::

                >>> metric_modulation_2 == metric_modulation_1
                True
                >>> metric_modulation_2 == metric_modulation_2
                True
                >>> metric_modulation_2 == metric_modulation_3
                False

            ::

                >>> metric_modulation_3 == metric_modulation_1
                False
                >>> metric_modulation_3 == metric_modulation_2
                False
                >>> metric_modulation_3 == metric_modulation_3
                True

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            if self.ratio == expr.ratio:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )

            ::

                >>> print(format(metric_modulation))
                indicatortools.MetricModulation(
                    left_rhythm=selectiontools.Selection(
                        [
                            scoretools.Note("c'4"),
                            ]
                        ),
                    right_rhythm=selectiontools.Selection(
                        [
                            scoretools.Note("c'4."),
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

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), "c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> show(metric_modulation) # doctest: +SKIP

            ..  doctest::

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
        from abjad.tools import lilypondfiletools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.header_block.tagline = False
        lilypond_file.items.append(self._get_markup())
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )

            ::

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

    ### PRIVATE METHODS ###

    def _get_left_markup(self):
        if self.left_markup is not None:
            return self.left_markup
        markup = durationtools.Duration._to_score_markup(self.left_rhythm)
        return markup

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self._get_markup()
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    def _get_markup(self, music_scale_pair=(0.75, 0.75)):
        assert isinstance(music_scale_pair, (tuple, type(None)))
        left_markup = self._get_left_markup()
        if music_scale_pair:
            left_markup = left_markup.scale(music_scale_pair)
        equal = markuptools.Markup('=')
        right_space = markuptools.Markup.hspace(-0.5)
        right_markup = self._get_right_markup()
        if music_scale_pair:
            right_markup = right_markup.scale(music_scale_pair)
        markup = left_markup + equal + right_space + right_markup
        return markup

    def _get_right_markup(self):
        if self.right_markup is not None:
            return self.right_markup
        markup = durationtools.Duration._to_score_markup(self.right_rhythm)
        return markup

    def _initialize_rhythm(self, rhythm):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        if isinstance(rhythm, scoretools.Component):
            selection = selectiontools.Selection([rhythm])
        elif isinstance(rhythm, selectiontools.Selection):
            selection = rhythm
        else:
            message = 'rhythm must be duration, component or selection: {!r}.'
            message = message.format(rhythm)
            raise TypeError(message)
        assert isinstance(selection, selectiontools.Selection)
        return selection

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation.default_scope is None
                True

        .. todo:: Metric modulations should be score-scope.

        Returns none (but should return score).
        '''
        return self._default_scope

    @property
    def left_markup(self):
        r'''Gets left markup of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation.left_markup

        Returns markup or none.
        '''
        return self._left_markup

    @property
    def left_rhythm(self):
        r'''Gets left rhythm of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
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

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Tuplet((2, 3), [Note("c'4")]),
                ...     right_rhythm=Note("c'4"),
                ...     )
                >>> metric_modulation.ratio
                Ratio((2, 3))

        Returns ratio.
        '''
        left_duration = self.left_rhythm.get_duration()
        right_duration = self.right_rhythm.get_duration()
        duration = left_duration / right_duration
        ratio = mathtools.Ratio(duration.pair)
        return ratio

    @property
    def right_markup(self):
        r'''Gets right markup of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation.right_markup

        Returns markup or none.
        '''
        return self._right_markup

    @property
    def right_rhythm(self):
        r'''Gets right tempo of metric modulation.

        ..  container:: example

            ::

                >>> metric_modulation = indicatortools.MetricModulation(
                ...     left_rhythm=Note("c'4"),
                ...     right_rhythm=Note("c'4."),
                ...     )
                >>> metric_modulation.right_rhythm
                Selection([Note("c'4.")])

        Returns selection.
        '''
        return self._right_rhythm
