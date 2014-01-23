# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools import systemtools
from abjad.tools.rhythmmakertools.GalleryInputSpecifier \
    import GalleryInputSpecifier
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import new


class EvenRunRhythmMaker(RhythmMaker):
    r'''Even run rhythm-maker.

    ..  container:: example

        Makes even run of notes each equal in duration to ``1/d``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker()

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    ..  container:: example

        Makes even run of notes each equal in duration to
        ``1/(2**d)`` with ``d`` equal to the denominator of each division
        on which the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Even-run rhythm-maker doesn't yet work with non-power-of-two divisions.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_denominator_multiplier_exponent',
        )

    _class_name_abbreviation = 'ER'

    _human_readable_class_name = 'even-run rhythm-maker'

    ### GALLERY INPUT ###

    _gallery_input_blocks = (
        GalleryInputSpecifier(
            input_={
                'denominator_multiplier_exponent': 0,
                'beam_each_cell': True,
                'beam_cells_together': False,
                },
            division_lists=(
                [
                    (4, 8), (3, 4),
                    (2, 4), (1, 16), (1, 16), 
                    (7, 8), (2, 8),
                ],
                [
                    (5, 16), (5, 16), (5, 16), (5, 16),
                    (4, 16), (4, 16), (4, 16), (4, 16),
                ],
                [
                    (2, 8), (3, 8), (2, 16), (1, 4), 
                    (2, 4), (2, 16), (2, 4),
                ],
                [
                    (5, 16), (5, 16), (5, 16), (5, 16),
                    (4, 16), (4, 16), (4, 16), (4, 16),
                ],
                ),
            ),
        GalleryInputSpecifier(
            input_={
                'denominator_multiplier_exponent': 1,
                'beam_each_cell': True,
                'beam_cells_together': False,
                },
            division_lists=(
                [
                    (4, 8), (3, 4),
                    (2, 4), (1, 16), (1, 16), 
                    (7, 8), (2, 8),
                ],
                [
                    (5, 16), (5, 16), (5, 16), (5, 16),
                    (4, 16), (4, 16), (4, 16), (4, 16),
                ],
                [
                    (2, 8), (3, 8), (2, 16), (1, 4), 
                    (2, 4), (2, 16), (2, 4),
                ],
                [
                    (5, 16), (5, 16), (5, 16), (5, 16),
                    (4, 16), (4, 16), (4, 16), (4, 16),
                ],
                ),
            ),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        denominator_multiplier_exponent=0,
        beam_cells_together=False,
        beam_each_cell=True,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_across_divisions=False,
        ):
        assert mathtools.is_nonnegative_integer(
            denominator_multiplier_exponent)
        RhythmMaker.__init__(
            self,
            beam_cells_together=beam_cells_together,
            beam_each_cell=beam_each_cell,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_across_divisions=tie_across_divisions,
            )
        self._denominator_multiplier_exponent = \
            denominator_multiplier_exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls even-run rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
                >>> result = maker(divisions)
                >>> for selection in result:
                ...     selection
                Selection(Container("c'16 c'16 c'16 c'16 c'16 c'16 c'16 c'16"),)
                Selection(Container("c'8 c'8 c'8 c'8 c'8 c'8"),)
                Selection(Container("c'8 c'8 c'8 c'8"),)

        Returns a list of selections. Each selection holds a single container
        filled with notes.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats even run rhythm-maker.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.EvenRunRhythmMaker(
                    denominator_multiplier_exponent=1,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

        Set `format_specification` to `''` or `'storage'`.

        Returns string.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new even-run rhythm-maker with `kwargs`.

        ..  container:: example

            ::

                >>> new_maker = new(maker, denominator_multiplier_exponent=0)

            ::

                >>> print format(new_maker)
                rhythmmakertools.EvenRunRhythmMaker(
                    denominator_multiplier_exponent=0,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=True,
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new even-run rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'denominator_multiplier_exponent':
                self.denominator_multiplier_exponent,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        arguments.update(kwargs)
        new = type(self)(**arguments)
        return new

    ### PRIVATE METHODS ###

    def _make_container(self, division):
        numerator, denominator = division
        # eventually allow for non-power-of-two divisions
        assert mathtools.is_positive_integer_power_of_two(denominator)
        denominator_multiplier = 2 ** self.denominator_multiplier_exponent
        denominator *= denominator_multiplier
        unit_duration = durationtools.Duration(1, denominator)
        numerator *= denominator_multiplier
        notes = scoretools.make_notes(numerator * [0], [unit_duration])
        container = scoretools.Container(notes)
        if self.beam_each_cell:
            beam = spannertools.MultipartBeam()
            attach(beam, container)
        return container

    def _make_music(self, duration_pairs, seeds):
        result = []
        for duration_pair in duration_pairs:
            container = self._make_container(duration_pair)
            selection = selectiontools.Selection(container)
            result.append(selection)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def denominator_multiplier_exponent(self):
        r'''Gets denominator multiplier exponent of even-run rhythm-maker.

        ..  container:: example

            ::

                >>> maker.denominator_multiplier_exponent
                1

        Returns nonnegative integer.
        '''
        return self._denominator_multiplier_exponent

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses even-run rhythm-maker.

        ..  container:: example
        
            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.EvenRunRhythmMaker(
                    denominator_multiplier_exponent=1,
                    beam_cells_together=False,
                    beam_each_cell=True,
                    decrease_durations_monotonically=False,
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(4, 8), (3, 4), (2, 4)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Defined equal to copy of even-run rhythm-maker.

        Returns new even-run rhythm-maker.
        '''
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
#        arguments = {
#            'denominator_multiplier_exponent': 
#                self.denominator_multiplier_exponent,
#            'beam_cells_together': self.beam_cells_together,
#            'beam_each_cell': self.beam_each_cell,
#            'decrease_durations_monotonically': 
#                decrease_durations_monotonically,
#            'forbidden_written_duration': self.forbidden_written_duration,
#            }
#        new = type(self)(**arguments)
#        return new
        maker = new(
            self,
            decrease_durations_monotonically=decrease_durations_monotonically,
            )
        return maker
