import inspect
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SilenceMask(AbjadValueObject):
    r'''Silence mask.

    ..  container:: example

        >>> pattern = abjad.index_every([0, 1, 7], period=16)
        >>> mask = abjad.rhythmmakertools.SilenceMask(pattern)

        >>> abjad.f(mask)
        abjad.SilenceMask(
            pattern=abjad.index_every([0, 1, 7], 16),
            )

    ..  container:: example

        With composite pattern:

        >>> pattern_1 = abjad.index_all()
        >>> pattern_2 = abjad.index_first(1)
        >>> pattern_3 = abjad.index_last(1)
        >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
        >>> mask = abjad.SilenceMask(pattern)

        >>> abjad.f(mask)
        abjad.SilenceMask(
            pattern=abjad.Pattern(
                operator='xor',
                patterns=(
                    abjad.index_all(),
                    abjad.index_first(1),
                    abjad.index_last(1),
                    ),
                ),
            )

        >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
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

        With inverted composite pattern:

        >>> pattern_1 = abjad.index_all()
        >>> pattern_2 = abjad.index_first(1)
        >>> pattern_3 = abjad.index_last(1)
        >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
        >>> pattern = ~pattern
        >>> mask = abjad.SilenceMask(pattern)

        >>> abjad.f(mask)
        abjad.SilenceMask(
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

        >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        '_template',
        '_use_multimeasure_rests',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        template=None,
        use_multimeasure_rests=None,
        ):
        import abjad
        if pattern is None:
            pattern = abjad.index_all()
        assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._template = template
        if use_multimeasure_rests is not None:
            assert isinstance(use_multimeasure_rests, type(True))
        self._use_multimeasure_rests = use_multimeasure_rests

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        if self.template is None:
            return super(SilenceMask, self)._get_format_specification()
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.template],
            storage_format_forced_override=self.template,
            storage_format_kwargs_names=(),
            )

    @staticmethod
    def _get_template(frame):
        import abjad
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            arguments = abjad.Expression._wrap_arguments(
                frame,
                static_class=SilenceMask,
                )
            template = 'abjad.{}({})'.format(function_name, arguments)
        finally:
            del frame
        return template

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        Returns pattern.
        '''
        return self._pattern

    @property
    def template(self):
        r'''Gets template.

        Returns string or none.
        '''
        return self._template

    @property
    def use_multimeasure_rests(self):
        r'''Is true when silence mask should use multimeasure rests.

        ..  container:: example

            Without multimeasure rests:

            >>> mask = abjad.rhythmmakertools.SilenceMask(
            ...     abjad.index_every([0, 1, 7], period=16),
            ...     use_multimeasure_rests=False,
            ...     )

            >>> mask.use_multimeasure_rests
            False

        ..  container:: example

            With multimeasure rests:

            >>> mask = abjad.rhythmmakertools.SilenceMask(
            ...     abjad.index_every([0, 1, 7], period=16),
            ...     use_multimeasure_rests=True,
            ...     )

            >>> mask.use_multimeasure_rests
            True

        Set to true, false or none.
        '''
        return self._use_multimeasure_rests

    ### PUBLIC METHODS ###

    @staticmethod
    def silence(indices, inverted=None):
        r'''Makes silence mask that matches `indices`.

        ..  container:: example

            Silences divisions 1 and 2:

            >>> mask = abjad.silence([1, 2])

            >>> mask
            abjad.silence([1, 2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence([-1, -2])

            >>> mask
            abjad.silence([-1, -2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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


        Returns silence mask.
        '''
        import abjad
        pattern = abjad.index(indices, inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(pattern=pattern, template=template)

    @staticmethod
    def silence_all(inverted=None, use_multimeasure_rests=None):
        r'''Makes silence that matches all indices.

        ..  container:: example

            Silences all divisions:

            >>> mask = abjad.silence_all()

            >>> mask
            abjad.silence_all()

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_all(use_multimeasure_rests=True)
            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )

            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        pattern = abjad.index_all(inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(
            pattern=pattern,
            template=template,
            use_multimeasure_rests=use_multimeasure_rests,
            )

    @staticmethod
    def silence_every(
        indices,
        period,
        inverted=None,
        use_multimeasure_rests=None,
        ):
        r'''Makes silence mask that matches `indices` at `period`.

        ..  container:: example

            Silences every second division:

            >>> mask = abjad.silence_every([1], 2)

            >>> mask
            abjad.silence_every([1], 2)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_every([1, 2], 3)

            >>> mask
            abjad.silence_every([1, 2], 3)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_except([-1])

            >>> mask
            abjad.silence_except([-1])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        pattern = abjad.index_every(indices, period, inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(
            pattern=pattern,
            template=template,
            use_multimeasure_rests=use_multimeasure_rests,
            )

    @staticmethod
    def silence_except(indices):
        r'''Makes silence mask that matches all indices except `indices`.

        ..  container:: example

            Silences divisions except 1 and 2:

            >>> mask = abjad.silence_except([1, 2])

            >>> mask
            abjad.silence_except([1, 2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_except([-1, -2])

            >>> mask
            abjad.silence_except([-1, -2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

        Equivalent to ``silence(..., inverted=True)``.

        Returns silence mask.
        '''
        import abjad
        pattern = abjad.index(indices, inverted=True)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(pattern=pattern, template=template)

    @staticmethod
    def silence_first(n, inverted=None, use_multimeasure_rests=None):
        r'''Makes silence mask that matches the first `n` indices.

        ..  container:: example

            Silences first division:

            >>> mask = abjad.silence_first(1)

            >>> mask
            abjad.silence_first(1)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_first(2)

            >>> mask
            abjad.silence_first(2)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_first(0)

            >>> mask
            abjad.silence_first(0)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        pattern = abjad.index_first(n, inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(
            pattern=pattern,
            template=template,
            use_multimeasure_rests=use_multimeasure_rests,
            )

    @staticmethod
    def silence_last(n, inverted=None, use_multimeasure_rests=None):
        r'''Makes silence mask that matches the last `n` indices.

        ..  container:: example

            Silences last division:

            >>> mask = abjad.silence_last(1)

            >>> mask
            abjad.silence_last(1)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_last(2)

            >>> mask
            abjad.silence_last(2)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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

            >>> mask = abjad.silence_last(0)

            >>> mask
            abjad.silence_last(0)

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[mask],
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> selections = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     selections,
            ...     divisions,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
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
        pattern = abjad.index_last(n, inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(
            pattern=pattern,
            template=template,
            use_multimeasure_rests=use_multimeasure_rests,
            )
