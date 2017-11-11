import inspect
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SustainMask(AbjadValueObject):
    r'''Sustain mask.

    ..  container:: example

        >>> mask = abjad.rhythmmakertools.SustainMask(
        ...     pattern=abjad.index([0, 1, 7], 16),
        ...     )

        >>> abjad.f(mask)
        abjad.SustainMask(
            pattern=abjad.index([0, 1, 7], period=16),
            )

    ..  container:: example

        With composite pattern:

        >>> pattern_1 = abjad.index_all()
        >>> pattern_2 = abjad.index_first(1)
        >>> pattern_3 = abjad.index_last(1)
        >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
        >>> mask = abjad.SustainMask(pattern=pattern)

        >>> abjad.f(mask)
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

        >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
        ...     division_masks=[
        ...         abjad.silence([0], 1),
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

    ..  container:: example

        Works inverted composite pattern:

        >>> pattern_1 = abjad.index_all()
        >>> pattern_2 = abjad.index_first(1)
        >>> pattern_3 = abjad.index_last(1)
        >>> pattern = pattern_1 ^ pattern_2 ^ pattern_3
        >>> pattern = ~pattern
        >>> mask = abjad.SustainMask(pattern=pattern)

        >>> abjad.f(mask)
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

        >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
        ...     division_masks=[
        ...         abjad.silence([0], 1),
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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Masks'

    __slots__ = (
        '_pattern',
        '_template',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        pattern=None,
        template=None,
        ):
        import abjad
        if pattern is None:
            pattern = abjad.index_all()
        assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._template = template

    ### SPECIAL METHODS ###

    def __invert__(self):
        r'''Inverts pattern.

        Returns new sustain mask.
        '''
        import abjad
        pattern = ~self.pattern
        inverted = pattern.inverted or None
        return abjad.sustain(pattern.indices, pattern.period, inverted)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        if self.template is None:
            return super(SustainMask, self)._get_format_specification()
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
                static_class=SustainMask,
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

        Returns template.
        '''
        return self._template

    ### PUBLIC METHODS ###

    @staticmethod
    def sustain(indices, period=None, inverted=None):
        r'''Makes sustain mask that matches `indices`.

        ..  container:: example

            Sustains divisions 1 and 2:

            >>> mask = abjad.sustain([1, 2])

            >>> mask
            abjad.sustain([1, 2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         abjad.silence([0], 1),
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

        ..  container:: example

            Sustains divisions -1 and -2:

            >>> mask = abjad.sustain([-1, -2])

            >>> mask
            abjad.sustain([-1, -2])

            >>> rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            ...     division_masks=[
            ...         abjad.silence([0], 1),
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
                        r4.
                    } % measure
                    { % measure
                        \time 7/16
                        c'4..
                    } % measure
                    { % measure
                        \time 3/8
                        c'4.
                    } % measure
                }


        Returns sustain mask.
        '''
        import abjad
        pattern = abjad.index(indices, period=period, inverted=inverted)
        template = SustainMask._get_template(inspect.currentframe())
        return SustainMask(pattern=pattern, template=template)
