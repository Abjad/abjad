# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
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

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Rhythm-makers'

    __slots__ = ()

    _class_name_abbreviation = 'S'

    _human_readable_class_name = 'skip rhythm-maker'

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        r'''Calls skip rhythm-maker on `divisions`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            rotation=rotation,
            )

    def __format__(self, format_specification=''):
        r'''Formats skip rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print(format(maker))
                rhythmmakertools.SkipRhythmMaker()

        Returns string.
        '''
        superclass = super(SkipRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _make_music(self, divisions, rotation):
        result = []
        for division in divisions:
            prototype = mathtools.NonreducedFraction
            assert isinstance(division, prototype), repr(division)
            written_duration = durationtools.Duration(1)
            multiplied_duration = division
            skip = scoretools.make_skips(
                written_duration, [multiplied_duration])
            result.append(skip)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of skip rhythm-maker.

        ..  note:: not yet implemented.

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(SkipRhythmMaker, self)
        return superclass.tuplet_spelling_specifier