# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class SkipRhythmMaker(RhythmMaker):
    r'''Skip rhythm-maker.

    ..  container:: example

        Makes skips equal to the duration of input divisions.

        ::

            >>> maker = rhythmmakertools.SkipRhythmMaker()

        ::

            >>> divisions = [(1, 4), (3, 16), (5, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 1/4
                    s1 * 1/4
                }
                {
                    \time 3/16
                    s1 * 3/16
                }
                {
                    \time 5/8
                    s1 * 5/8
                }
            }

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'S'

    _human_readable_class_name = 'skip rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        RhythmMaker.__init__(
            self,
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls skip rhythm-maker on `divisions`.

        Returns list of skips.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats skip rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.SkipRhythmMaker()

        Returns string.
        '''
        superclass = super(SkipRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new skip rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker)

            ::

                >>> print format(new_maker)
                rhythmmakertools.SkipRhythmMaker()

            ::

                >>> divisions = [(1, 4), (3, 16), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 1/4
                        s1 * 1/4
                    }
                    {
                        \time 3/16
                        s1 * 3/16
                    }
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                }

        Returns new skip rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        result = []
        for duration_pair in duration_pairs:
            written_duration = durationtools.Duration(1)
            multiplied_duration = duration_pair
            skip = scoretools.make_skips_with_multiplied_durations(
                written_duration, [multiplied_duration])
            result.append(skip)
        return result

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses skip rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.SkipRhythmMaker()

            ::

                >>> divisions = [(1, 4), (3, 16), (5, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 1/4
                        s1 * 1/4
                    }
                    {
                        \time 3/16
                        s1 * 3/16
                    }
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                }

        Defined equal to copy of rhythm-maker.

        Returns new skip rhythm-maker.
        '''
        return type(self)()
