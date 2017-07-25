# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SilenceMask(AbjadValueObject):
    r'''Silence mask.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    ..  container:: example

        ::

            >>> pattern = abjad.index_every([0, 1, 7], period=16)
            >>> mask = rhythmmakertools.SilenceMask(pattern)

        ::

            >>> f(mask)
            rhythmmakertools.SilenceMask(
                pattern=abjad.Pattern(
                    indices=[0, 1, 7],
                    period=16,
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        '_use_multimeasure_rests',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        use_multimeasure_rests=None,
        ):
        import abjad
        from abjad.tools import rhythmmakertools
        if pattern is None:
            pattern = abjad.index_all()
        assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        if use_multimeasure_rests is not None:
            assert isinstance(use_multimeasure_rests, type(True))
        self._use_multimeasure_rests = use_multimeasure_rests

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern

    @property
    def use_multimeasure_rests(self):
        r'''Is true when silence mask should use multimeasure rests.

        ..  container:: example

            Without multimeasure rests:

            ::

            
                >>> mask = rhythmmakertools.SilenceMask(
                ...     abjad.index_every([0, 1, 7], period=16),
                ...     use_multimeasure_rests=False,
                ...     )

            ::

                >>> mask.use_multimeasure_rests
                False

        ..  container:: example

            With multimeasure rests:

            ::

                >>> mask = rhythmmakertools.SilenceMask(
                ...     abjad.index_every([0, 1, 7], period=16),
                ...     use_multimeasure_rests=True,
                ...     )

            ::

                >>> mask.use_multimeasure_rests
                True

        Set to true, false or none.
        '''
        return self._use_multimeasure_rests

    ### PUBLIC METHODS ###

    @staticmethod
    def silence(indices=None, inverted=None):
        r'''Makes silence mask that matches `indices`.

        ..  container:: example

            Silences divisions 1 and 2:

            ::

                >>> mask = abjad.silence([1, 2])

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[1, 2],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

            Silences divisions -1 and -2:

            ::

                >>> mask = abjad.silence([-1, -2])

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[-1, -2],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
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
                        c'4.
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

        ..  container:: example

            Works with pattern input:

            ::

                >>> pattern_1 = abjad.index_all()
                >>> pattern_2 = abjad.index_first()
                >>> pattern_3 = abjad.index_last()
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
                >>> mask = abjad.silence(pattern)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        operator='xor',
                        patterns=(
                            abjad.Pattern(
                                indices=[0],
                                period=1,
                                ),
                            abjad.Pattern(
                                indices=[0],
                                ),
                            abjad.Pattern(
                                indices=[-1],
                                ),
                            ),
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
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

        ..  container:: example

            Works with pattern input and inverted flag:

            ::

                >>> pattern_1 = abjad.index_all()
                >>> pattern_2 = abjad.index_first()
                >>> pattern_3 = abjad.index_last()
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
                >>> mask = abjad.silence(pattern, inverted=True)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        inverted=True,
                        operator='xor',
                        patterns=(
                            abjad.Pattern(
                                indices=[0],
                                period=1,
                                ),
                            abjad.Pattern(
                                indices=[0],
                                ),
                            abjad.Pattern(
                                indices=[-1],
                                ),
                            ),
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
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

        Returns silence mask.
        '''
        import abjad
        if isinstance(indices, abjad.Pattern):
            pattern = indices
        else:
            pattern = abjad.Pattern(
                indices=indices,
                inverted=inverted,
                )
        pattern = abjad.new(pattern, inverted=inverted)
        return SilenceMask(pattern=pattern)

    @staticmethod
    def silence_all(inverted=None, use_multimeasure_rests=None):
        r'''Makes silence that matches all indices.

        ..  container:: example

            Silences all divisions:

            ::

                >>> mask = abjad.silence_all()

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[0],
                        period=1,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

        ..  container:: example

            Silences all divisions with multimeasure rests:

            ::

                >>> mask = abjad.silence_all(
                ...     use_multimeasure_rests=True,
                ...     )
                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[mask],
                ...     )

            ::

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
                        R1 * 7/16
                    }
                    {
                        \time 3/8
                        R1 * 3/8
                    }
                    {
                        \time 7/16
                        R1 * 7/16
                    }
                    {
                        \time 3/8
                        R1 * 3/8
                    }
                }

        Returns silence mask.
        '''
        import abjad
        pattern = abjad.Pattern(
            indices=[0],
            inverted=inverted,
            period=1,
            )
        mask = SilenceMask(
            pattern=pattern,
            use_multimeasure_rests=use_multimeasure_rests,
            )
        return mask

    @staticmethod
    def silence_every(
        indices, 
        period=None, 
        inverted=None, 
        use_multimeasure_rests=None,
        ):
        r'''Makes silence mask that matches `indices` at `period`.

        ..  container:: example

            Silences every second division:

            ::

                >>> mask = abjad.silence_every(indices=[1], period=2)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[1],
                        period=2,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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
                        r4.
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

            Silences every second and third division:

            ::

                >>> mask = abjad.silence_every(indices=[1, 2], period=3)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[1, 2],
                        period=3,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

            Silences every division except the last:

            ::

                >>> mask = abjad.silence_every(indices=[-1], inverted=True)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[-1],
                        inverted=True,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

        Returns silence mask.
        '''
        import abjad
        pattern = abjad.Pattern(
            indices=indices,
            inverted=inverted,
            period=period,
            )
        mask = SilenceMask(
            pattern=pattern,
            use_multimeasure_rests=use_multimeasure_rests,
            )
        return mask

    @staticmethod
    def silence_except(indices=None):
        r'''Makes silence mask that matches all indices except `indices`.

        ..  container:: example

            Silences divisions except 1 and 2:

            ::

                >>> mask = abjad.silence_except([1, 2])

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[1, 2],
                        inverted=True,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

                >>> staff = lilypond_file[abjad.Staff]
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

            Silences divisions except -1 and -2:

            ::

                >>> mask = abjad.silence_except([-1, -2])

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[-1, -2],
                        inverted=True,
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
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

        ..  container:: example

            Works with pattern input:

            ::

                >>> pattern_1 = abjad.index_all()
                >>> pattern_2 = abjad.index_first()
                >>> pattern_3 = abjad.index_last()
                >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
                >>> mask = abjad.silence_except(pattern)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        inverted=True,
                        operator='xor',
                        patterns=(
                            abjad.Pattern(
                                indices=[0],
                                period=1,
                                ),
                            abjad.Pattern(
                                indices=[0],
                                ),
                            abjad.Pattern(
                                indices=[-1],
                                ),
                            ),
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
                ...     division_masks=[
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

        Equivalent to ``silence(..., inverted=True)``.

        Returns silence mask.
        '''
        import abjad
        if isinstance(indices, abjad.Pattern):
            pattern = indices
        else:
            pattern = abjad.Pattern(
                indices=indices,
                )
        pattern = abjad.new(pattern, inverted=True)
        return SilenceMask(pattern=pattern)

    @staticmethod
    def silence_first(n=1, inverted=None, use_multimeasure_rests=None):
        r'''Makes silence mask that matches the first `n` indices.

        ..  container:: example

            Silences first division:

            ::

                >>> mask = abjad.silence_first()

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[0],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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
                        c'4.
                    }
                }

        ..  container:: example

            Silences first two divisions:

            ::

                >>> mask = abjad.silence_first(n=2)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[0, 1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

            Silences no first divisions:

            ::

                >>> mask = abjad.silence_first(n=0)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

        Returns silence mask.
        '''
        import abjad
        if 0 < n:
            indices = list(range(n))
        else:
            indices = None
        pattern = abjad.Pattern(
            indices=indices,
            inverted=inverted,
            )
        mask = SilenceMask(
            pattern=pattern,
            use_multimeasure_rests=use_multimeasure_rests,
            )
        return mask

    @staticmethod
    def silence_last(n=1, inverted=None, use_multimeasure_rests=None):
        r'''Makes silence mask that matches the last `n` indices.

        ..  container:: example

            Silences last division:

            ::

                >>> mask = abjad.silence_last()

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[-1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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
                        r4.
                    }
                }

        ..  container:: example

            Silences last two divisions:

            ::

                >>> mask = abjad.silence_last(n=2)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(
                        indices=[-2, -1],
                        ),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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
                        r4..
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        ..  container:: example

            Silences no last divisions:

            ::

                >>> mask = abjad.silence_last(n=0)

            ::

                >>> f(mask)
                rhythmmakertools.SilenceMask(
                    pattern=abjad.Pattern(),
                    )

            ::

                >>> rhythm_maker = rhythmmakertools.NoteRhythmMaker(
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

        Returns silence mask.
        '''
        import abjad
        if 0 < n:
            indices = list(reversed(range(-1, -n-1, -1)))
        else:
            indices = None
        pattern = abjad.Pattern(
            indices=indices,
            inverted=inverted,
            )
        mask = SilenceMask(
            pattern=pattern,
            use_multimeasure_rests=use_multimeasure_rests,
            )
        return mask
