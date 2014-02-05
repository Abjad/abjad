# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import new


class RestRhythmMaker(RhythmMaker):
    r'''Rest rhythm-maker.

    ..  container:: example

        Makes rests equal to the duration of input divisions.

        ::

            >>> maker = rhythmmakertools.RestRhythmMaker()

        ::

            >>> divisions = [(5, 16), (3, 8)]
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
                    \time 5/16
                    r4
                    r16
                }
                {
                    \time 3/8
                    r4.
                }
            }


    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'R'

    _human_readable_class_name = 'rest rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        duration_spelling_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            duration_spelling_specifier=duration_spelling_specifier,
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls rest rhythm-maker on `divisions`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats rest rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.RestRhythmMaker()

        Returns string.
        '''
        superclass = super(RestRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        result = []
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        for duration_pair in duration_pairs:
            rests = scoretools.make_leaves(
                pitches=None,
                durations=[duration_pair],
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                )
            result.append(rests)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of rest rhythm-maker.

            ..  container:: example

                Forbids rests with written duration greater than or equal to
                ``1/4`` of a whole note:

                ::

                    >>> duration_spelling_specifier = \
                    ...     rhythmmakertools.DurationSpellingSpecifier(
                    ...     forbidden_written_duration=Duration(1, 4),
                    ...     )
                    >>> maker = rhythmmakertools.RestRhythmMaker(
                    ...     duration_spelling_specifier=duration_spelling_specifier,
                    ...     )

                ::

                    >>> divisions = [(5, 16), (3, 8)]
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
                            \time 5/16
                            r8
                            r8
                            r16
                        }
                        {
                            \time 3/8
                            r8
                            r8
                            r8
                        }
                    }

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rest rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.RestRhythmMaker()
                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.RestRhythmMaker(
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(5, 16), (3, 8)]
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
                        \time 5/16
                        r4
                        r16
                    }
                    {
                        \time 3/8
                        r4.
                    }
                }

        Returns new rest rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self.duration_spelling_specifier
        if duration_spelling_specifier is None:
            default = rhythmmakertools.DurationSpellingSpecifier()
            duration_spelling_specifier = default
        duration_spelling_specifier = duration_spelling_specifier.reverse()
        arguments = {
            'duration_spelling_specifier': duration_spelling_specifier,
            }
        result = new(self, **arguments)
        return result
