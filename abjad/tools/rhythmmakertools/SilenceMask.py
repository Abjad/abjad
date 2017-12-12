import inspect
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SilenceMask(AbjadValueObject):
    r'''Silence mask.

    ..  container:: example

        >>> pattern = abjad.index([0, 1, 7], 16)
        >>> mask = abjad.rhythmmakertools.SilenceMask(pattern)

        >>> abjad.f(mask)
        abjad.SilenceMask(
            pattern=abjad.index([0, 1, 7], period=16),
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
                { % measure
                    \time 7/16
                    c'4..
                } % measure
                { % measure
                    \time 3/8
                    r4.
                } % measure
                { % measure
                    \time 7/16
                    r4..
                } % measure
                { % measure
                    \time 3/8
                    c'4.
                } % measure
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
                { % measure
                    \time 7/16
                    r4..
                } % measure
                { % measure
                    \time 3/8
                    c'4.
                } % measure
                { % measure
                    \time 7/16
                    c'4..
                } % measure
                { % measure
                    \time 3/8
                    r4.
                } % measure
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

    ### SPECIAL METHODS ###

    def __invert__(self):
        r'''Inverts pattern.

        Returns new silence mask.
        '''
        import abjad
        pattern = ~self.pattern
        inverted = pattern.inverted or None
        return abjad.silence(pattern.indices, pattern.period, inverted)

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
            ...     abjad.index([0, 1, 7], 16),
            ...     use_multimeasure_rests=False,
            ...     )

            >>> mask.use_multimeasure_rests
            False

        ..  container:: example

            With multimeasure rests:

            >>> mask = abjad.rhythmmakertools.SilenceMask(
            ...     abjad.index([0, 1, 7], 16),
            ...     use_multimeasure_rests=True,
            ...     )

            >>> mask.use_multimeasure_rests
            True

        Set to true, false or none.
        '''
        return self._use_multimeasure_rests

    ### PUBLIC METHODS ###

    @staticmethod
    def silence(
        indices,
        period=None,
        inverted=None,
        use_multimeasure_rests=None,
        ):
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
                    { % measure
                        \time 7/16
                        c'4..
                    } % measure
                    { % measure
                        \time 3/8
                        r4.
                    } % measure
                    { % measure
                        \time 7/16
                        r4..
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
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
                    { % measure
                        \time 7/16
                        c'4..
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                    { % measure
                        \time 7/16
                        r4..
                    } % measure
                    { % measure
                        \time 3/8
                        r4.
                    } % measure
                }


        Returns silence mask.
        '''
        import abjad
        pattern = abjad.index(indices, period=period, inverted=inverted)
        template = SilenceMask._get_template(inspect.currentframe())
        return SilenceMask(
            pattern=pattern,
            template=template,
            use_multimeasure_rests=use_multimeasure_rests,
            )
