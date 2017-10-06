from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SustainMask(AbjadValueObject):
    r'''Sustain mask.

    ..  container:: example

        ::

            >>> mask = abjad.rhythmmakertools.SustainMask(
            ...     pattern=abjad.index_every([0, 1, 7], period=16),
            ...     )

        ::

            >>> f(mask)
            abjad.SustainMask(
                pattern=abjad.index_every([0, 1, 7], 16),
                )

    ..  container:: example

        With composite pattern:

        ::

            >>> pattern_1 = abjad.index_all()
            >>> pattern_2 = abjad.index_first(1)
            >>> pattern_3 = abjad.index_last(1)
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> mask = abjad.SustainMask(pattern=pattern)

        ::

            >>> f(mask)
            abjad.SustainMask(
                pattern=abjad.Pattern(
                    operator='xor',
                    patterns=(
                        abjad.index_all(),
                        abjad.index_first(1),
                        abjad.index_last(1),
                        ),
                    ),
                )

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         abjad.silence_all(),
            ...         mask,
            ...         ],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                {
                    \time 7/16
                    r4..
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    r4.
                }
            }

    ..  container:: example

        Works inverted composite pattern:

        ::

            >>> pattern_1 = abjad.index_all()
            >>> pattern_2 = abjad.index_first(1)
            >>> pattern_3 = abjad.index_last(1)
            >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
            >>> pattern = ~pattern
            >>> mask = abjad.SustainMask(pattern=pattern)

        ::

            >>> f(mask)
            abjad.SustainMask(
                pattern=abjad.Pattern(
                    inverted=True,
                    operator='xor',
                    patterns=(
                        abjad.index_all(),
                        abjad.index_first(1),
                        abjad.index_last(1),
                        ),
                    ),
                )

        ::

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         abjad.silence_all(),
            ...         mask,
            ...         ],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    r4.
                }
                {
                    \time 7/16
                    r4..
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        ):
        import abjad
        if pattern is None:
            pattern = abjad.index_all()
        assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern

    ### PUBLIC METHODS ###

    @staticmethod
    def sustain(indices=None, inverted=None):
        r'''Makes sustain mask that matches `indices`.

        ..  container:: example

            Sustains divisions 1 and 2:

            ::

                >>> mask = abjad.sustain([1, 2])

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index([1, 2]),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            Sustains divisions -1 and -2:

            ::

                >>> mask = abjad.sustain([-1, -2])

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index([-1, -2]),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }


        Returns sustain mask.
        '''
        import abjad
#        if isinstance(indices, abjad.Pattern):
#            pattern = indices
#        else:
#            indices = indices or []
#            pattern = abjad.Pattern(
#                indices=indices,
#                inverted=inverted,
#                )
#        pattern = abjad.new(pattern, inverted=inverted)
        pattern = abjad.index(indices, inverted=inverted)
        return SustainMask(pattern=pattern)

    @staticmethod
    def sustain_all(inverted=None):
        r'''Makes sustain mask that matches all indices.

        ..  container:: example

            Without mask:

                >>> rhythm_maker = abjad.rhythmmakertools.TupletRhythmMaker(
                ...     tuplet_ratios=[(3, 1)],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

            ::

                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 7/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'4.
                            c'8
                        }
                    }
                    {
                        \time 3/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'4.
                            c'8
                        }
                    }
                }

        ..  container:: example

            With mask:

            ::

                >>> mask = abjad.sustain_all()

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_all(),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.TupletRhythmMaker(
                ...     division_masks=[mask],
                ...     tuplet_ratios=[(3, 1)],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]

            ::

                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns sustain mask.
        '''
        import abjad
#        pattern = abjad.Pattern(
#            indices=[0],
#            inverted=inverted,
#            period=1,
#            )
        pattern = abjad.index_all(inverted=inverted) 
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_every(indices, period, inverted=None):
        r'''Makes sustain mask that matches `indices` at `period`.

        ..  container:: example

            Sustains every second division:

            ::

                >>> mask = abjad.sustain_every([1], 2)

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_every([1], 2),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains every second and third division:

            ::

                >>> mask = abjad.sustain_every([1, 2], 3)

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_every([1, 2], 3),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns sustain mask.
        '''
        import abjad
#        indices = list(indices)
#        pattern = abjad.Pattern(
#            indices=indices,
#            inverted=inverted,
#            period=period,
#            )
        pattern = abjad.index_every(indices, period, inverted=inverted)
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_first(n=1, inverted=None):
        r'''Makes sustain mask that matches the first `n` indices.

        ..  container:: example

            Sustains first division:

            ::

                >>> mask = abjad.sustain_first()

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_first(1),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16],
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 7/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        ..  container:: example

            Sustains first two divisions:

            ::

                >>> mask = abjad.sustain_first(n=2)

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_first(2),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.EvenDivisionRhythmMaker(
                ...     denominators=[16],
                ...     division_masks=[mask],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                    {
                        \time 7/16
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                    {
                        \time 3/8
                        {
                            c'16 [
                            c'16
                            c'16
                            c'16
                            c'16
                            c'16 ]
                        }
                    }
                }

        Returns sustain mask.
        '''
        import abjad
#        indices = list(range(n))
#        pattern = abjad.Pattern(
#            indices=indices,
#            inverted=inverted,
#            )
        pattern = abjad.index_first(n, inverted=inverted)
        mask = SustainMask(pattern=pattern)
        return mask

    @staticmethod
    def sustain_last(n=1, inverted=None):
        r'''Makes sustain mask that matches the last `n` indices.

        ..  container:: example

            Sustains last division:

            ::

                >>> mask = abjad.sustain_last()

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_last(1),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains last two divisions:

            ::

                >>> mask = abjad.sustain_last(2)

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_last(2),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        c'4..
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            Sustains no last divisions:

            ::

                >>> mask = abjad.sustain_last(0)

            ::

                >>> f(mask)
                abjad.SustainMask(
                    pattern=abjad.index_last(0),
                    )

            ::

                >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
                ...         abjad.silence_all(),
                ...         mask,
                ...         ],
                ...     )
                >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
                >>> selections = rhythm_maker(divisions)
                >>> lilypond_file = abjad.LilyPondFile.rhythm(
                ...     selections,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new RhythmicStaff {
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                    {
                        \time 7/16
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        Returns sustain mask.
        '''
        import abjad
#        if 0 < n:
#            start = -1
#            stop = -n - 1
#            stride = -1
#            indices = list(reversed(range(start, stop, stride)))
#        else:
#            indices = None
#        pattern = abjad.Pattern(
#            indices=indices,
#            inverted=inverted,
#            )
        pattern = abjad.index_last(n, inverted=inverted)
        mask = SustainMask(pattern=pattern)
        return mask
