import abjad


class FerneyhoughDemo(object):
    r'''Ferneyhough demo.

    ..  container:: example

        Initializes Ferneyhough demo:

        >>> demo = abjad.demos.ferneyhough.FerneyhoughDemo()

        Calls Ferneyhough demo:

        >>> lilypond_file = demo(
        ...     tuplet_duration=abjad.Duration(1, 4),
        ...     row_count=11,
        ...     column_count=6,
        ...     )

        Shows LilyPond file:

        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.stencil = ##f
                \override BarNumber.transparent = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override TimeSignature.stencil = ##f
                \override TupletBracket.padding = #2
                \override TupletBracket.staff-padding = #4
                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                proportionalNotationDuration = #(ly:make-moment 1 56)
                tupletFullLength = ##t
            } <<
                \new RhythmicStaff {
                    {
                        \time 1/4
                        c'8
                        {
                            c'8
                        }
                    }
                    {
                        c'8
                        {
                            c'16
                            c'16
                        }
                    }
                    {
                        c'8
                        \times 2/3 {
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'8
                        {
                            c'32
                            c'32
                            c'32
                            c'32
                        }
                    }
                    {
                        c'8
                        \times 4/5 {
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                        }
                    }
                    {
                        c'8
                        \times 2/3 {
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 2/3 {
                        \time 1/4
                        c'8
                        {
                            c'4
                        }
                    }
                    \times 2/3 {
                        c'8
                        {
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'8
                        \times 2/3 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'8
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 2/3 {
                        c'8
                        \times 4/5 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 2/3 {
                        c'8
                        \times 2/3 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    {
                        \time 1/4
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4
                        }
                    }
                    {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'8
                            c'8
                        }
                    }
                    {
                        c'16
                        {
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'16
                        {
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                            c'32
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 4/5 {
                        \time 1/4
                        c'16
                        {
                            c'4
                        }
                    }
                    \times 4/5 {
                        c'16
                        {
                            c'8
                            c'8
                        }
                    }
                    \times 4/5 {
                        c'16
                        \times 2/3 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/5 {
                        c'16
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 4/5 {
                        c'16
                        \times 4/5 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 4/5 {
                        c'16
                        \times 2/3 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 2/3 {
                        \time 1/4
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'2
                        }
                    }
                    \times 2/3 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'4
                            c'4
                        }
                    }
                    \times 2/3 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'16
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 2/3 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 4/7 {
                        \time 1/4
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'2
                        }
                    }
                    \times 4/7 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4
                            c'4
                        }
                    }
                    \times 4/7 {
                        c'16
                        {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/7 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/7 {
                        c'16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/5 {
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/7 {
                        c'16
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    {
                        \time 1/4
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4
                        }
                    }
                    {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'8
                            c'8
                        }
                    }
                    {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/12 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/10 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/12 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 8/9 {
                        \time 1/4
                        c'32
                        {
                            c'4
                        }
                    }
                    \times 8/9 {
                        c'32
                        {
                            c'8
                            c'8
                        }
                    }
                    \times 8/9 {
                        c'32
                        \times 2/3 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 8/9 {
                        c'32
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 8/9 {
                        c'32
                        \times 4/5 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 8/9 {
                        c'32
                        \times 2/3 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 4/5 {
                        \time 1/4
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/16 {
                            c'2
                        }
                    }
                    \times 4/5 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/16 {
                            c'4
                            c'4
                        }
                    }
                    \times 4/5 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/5 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/16 {
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 4/5 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 4/5 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 8/11 {
                        \time 1/4
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'2
                        }
                    }
                    \times 8/11 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'4
                            c'4
                        }
                    }
                    \times 8/11 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 8/11 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/8 {
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 8/11 {
                        c'32
                        {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                    \times 8/11 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
                \new RhythmicStaff {
                    \times 2/3 {
                        \time 1/4
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/16 {
                            c'2
                        }
                    }
                    \times 2/3 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/16 {
                            c'4
                            c'4
                        }
                    }
                    \times 2/3 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/12 {
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/16 {
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/20 {
                            c'8
                            c'8
                            c'8
                            c'8
                            c'8
                        }
                    }
                    \times 2/3 {
                        c'32
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/12 {
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                        }
                    }
                }
            >>

    '''

    ### SPECIAL METHODS ###

    def __call__(self, tuplet_duration=(1, 4), row_count=11, column_count=6):
        r'''Calls Ferneyhough demo.

        Returns LilyPond file.
        '''
        lilypond_file = self.make_lilypond_file(
            tuplet_duration,
            row_count,
            column_count,
            )
        return lilypond_file

    ### PUBLIC METHODS ###

    def configure_lilypond_file(self, lilypond_file):
        r'''Configures LilyPond file.
        '''
        lilypond_file._default_paper_size = '11x17', 'portrait'
        lilypond_file._global_staff_size = 12
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.paper_block.ragged_bottom = True
        spacing_vector = abjad.SpacingVector(0, 0, 8, 0)
        lilypond_file.paper_block.system_system_spacing = spacing_vector

    def configure_score(self, score):
        r'''Configures `score`.
        '''
        moment = abjad.SchemeMoment((1, 56))
        abjad.setting(score).proportional_notation_duration = moment
        abjad.setting(score).tuplet_full_length = True
        abjad.override(score).bar_line.stencil = False
        abjad.override(score).bar_number.transparent = True
        abjad.override(score).spacing_spanner.uniform_stretching = True
        abjad.override(score).spacing_spanner.strict_note_spacing = True
        abjad.override(score).time_signature.stencil = False
        abjad.override(score).tuplet_bracket.padding = 2
        abjad.override(score).tuplet_bracket.staff_padding = 4
        scheme = abjad.Scheme('tuplet-number::calc-fraction-text')
        abjad.override(score).tuplet_number.text = scheme

    def make_lilypond_file(self, tuplet_duration, row_count, column_count):
        r'''Makes LilyPond file.
        '''
        score = self.make_score(
            tuplet_duration,
            row_count,
            column_count,
            )
        self.configure_score(score)
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(score)
        self.configure_lilypond_file(lilypond_file)
        return lilypond_file

    def make_nested_tuplet(
        self,
        tuplet_duration,
        outer_tuplet_proportions,
        inner_tuplet_subdivision_count,
        ):
        r'''Makes nested tuplet.
        '''
        outer_tuplet = abjad.Tuplet.from_duration_and_ratio(
            tuplet_duration,
            outer_tuplet_proportions,
            )
        inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
        selector = abjad.select().leaves()
        last_leaf = selector(outer_tuplet)[-1]
        right_logical_tie = abjad.inspect(last_leaf).get_logical_tie()
        right_logical_tie.to_tuplet(inner_tuplet_proportions)
        return outer_tuplet

    def make_row_of_nested_tuplets(
        self,
        tuplet_duration,
        outer_tuplet_proportions,
        column_count,
        ):
        r'''Makes row of nested tuplets.
        '''
        assert 0 < column_count
        row_of_nested_tuplets = []
        for n in range(column_count):
            inner_tuplet_subdivision_count = n + 1
            nested_tuplet = self.make_nested_tuplet(
                tuplet_duration,
                outer_tuplet_proportions,
                inner_tuplet_subdivision_count,
                )
            row_of_nested_tuplets.append(nested_tuplet)
        return row_of_nested_tuplets

    def make_rows_of_nested_tuplets(
        self,
        tuplet_duration,
        row_count,
        column_count,
        ):
        r'''Makes rows of nested tuplets.
        '''
        assert 0 < row_count
        rows_of_nested_tuplets = []
        for n in range(row_count):
            outer_tuplet_proportions = (1, n + 1)
            row_of_nested_tuplets = self.make_row_of_nested_tuplets(
                tuplet_duration,
                outer_tuplet_proportions,
                column_count,
                )
            rows_of_nested_tuplets.append(row_of_nested_tuplets)
        return rows_of_nested_tuplets

    def make_score(self, tuplet_duration, row_count, column_count):
        r'''Makes score.
        '''
        score = abjad.Score()
        rows_of_nested_tuplets = self.make_rows_of_nested_tuplets(
            tuplet_duration,
            row_count,
            column_count,
            )
        for row_of_nested_tuplets in rows_of_nested_tuplets:
            staff = abjad.Staff(row_of_nested_tuplets)
            staff.context_name = 'RhythmicStaff'
            time_signature = abjad.TimeSignature((1, 4))
            leaf = abjad.inspect(staff).get_leaf(0)
            abjad.attach(time_signature, leaf)
            score.append(staff)
        return score
