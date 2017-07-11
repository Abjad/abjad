# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TimeSignatureList(TypedList):
    r'''Time signature list.

    ::

        >>> import abjad

    ..  container:: example

        Two time signatures:

        ::

            >>> time_signatures = abjad.TimeSignatureList(
            ...     [(5, 8), (4, 4)],
            ...     )

        ::

            >>> f(time_signatures)
            abjad.TimeSignatureList(
                [
                    abjad.TimeSignature((5, 8)),
                    abjad.TimeSignature((4, 4)),
                    ]
                )

        ::

            >>> (5, 8) in time_signatures
            True

        ::

            >>> abjad.TimeSignature((4, 4)) in time_signatures
            True

        ::

            >>> (3, 4) in time_signatures
            False

        ::

            >>> show(time_signatures) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = time_signatures.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score <<
                \new RhythmicStaff {
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    {
                        \time 4/4
                        s1 * 1
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collections'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self, format_specification=''):
        r'''Formats time signature list.

        ..  container:: example

            ::

                >>> time_signatures = abjad.TimeSignatureList(
                ...     [(5, 8), (4, 4)],
                ...     )

            ::

                >>> show(time_signatures) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = time_signatures.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score <<
                    \new RhythmicStaff {
                        {
                            \time 5/8
                            s1 * 5/8
                        }
                        {
                            \time 4/4
                            s1 * 1
                        }
                    }
                >>

        Returns LilyPond file.
        '''
        import abjad
        maker = abjad.MeasureMaker()
        measures = maker(self)
        staff = abjad.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        def coerce(argument):
            if isinstance(argument, tuple):
                return indicatortools.TimeSignature(argument)
            elif isinstance(argument, indicatortools.TimeSignature):
                return copy.copy(argument)
            else:
                message = 'must be pair or time signature: {!r}.'
                message = message.format(argument)
                raise Exception(message)
        return coerce
