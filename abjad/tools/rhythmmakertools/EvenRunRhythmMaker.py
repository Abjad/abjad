# -*- encoding: utf-8 -*-
import os
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.agenttools.InspectionAgent import inspect
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import persist


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

    _human_readable_class_name = 'even-run rhythm-maker'

    ### GALLERY INPUT ###

    _gallery_input_blocks = (
        systemtools.GalleryInputBlock(
            input_={
                'denominator_multiplier_exponent': 0,
                'beam_each_cell': True,
                'beam_cells_together': False,
                },
            divisions=[
                (4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16),
                ],
            ),
        systemtools.GalleryInputBlock(
            input_={
                'denominator_multiplier_exponent': 1,
                'beam_each_cell': True,
                'beam_cells_together': False,
                },
            divisions=[
                (4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16),
                ],
            ),
        systemtools.GalleryInputBlock(
            input_={
                'denominator_multiplier_exponent': 2,
                'beam_each_cell': True,
                'beam_cells_together': False,
                },
            divisions=[
                (4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16),
                ],
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
        ):
        assert mathtools.is_nonnegative_integer(
            denominator_multiplier_exponent)
        RhythmMaker.__init__(
            self,
            beam_cells_together=beam_cells_together,
            beam_each_cell=beam_each_cell,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
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
                Selection({c'16, c'16, c'16, c'16, c'16, c'16, c'16, c'16},)
                Selection({c'8, c'8, c'8, c'8, c'8, c'8},)
                Selection({c'8, c'8, c'8, c'8},)

        Returns a list of selections. Each selection holds a single container
        filled with notes.
        '''
        duration_pairs, seeds = RhythmMaker.__call__(self, divisions, seeds)
        result = []
        for duration_pair in duration_pairs:
            container = self._make_container(duration_pair)
            selection = selectiontools.Selection(container)
            result.append(selection)
        return result

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
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    def _gallery_input_block_to_score(self, block):
        from abjad.tools import sequencetools
        maker = type(self)(**block.input_)
        lists = maker(block.divisions)
        music = sequencetools.flatten_sequence(lists)
        measures = scoretools.make_spacer_skip_measures(block.divisions)
        time_signature_context = scoretools.Context(
            measures,
            context_name='TimeSignatureContext',
            name='TimeSignatureContext',
            )
        measures = scoretools.make_spacer_skip_measures(block.divisions)
        staff = scoretools.RhythmicStaff(measures)
        measures = mutate(staff).replace_measure_contents(music)
        score = scoretools.Score()
        score.append(time_signature_context)
        score.append(staff)
        return score

    def _make_gallery_title_markup(self):
        string = self._human_readable_class_name 
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        return markup

    def _gallery_input_to_lilypond_file(self):
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.items.remove(lilypond_file.score_block)
        title_markup = self._make_gallery_title_markup()
        lilypond_file.header_block.title = title_markup
        markups = []
        scores = []
        for block in self._gallery_input_blocks:
            score = self._gallery_input_block_to_score(block)
            if not inspect(score).is_well_formed():
                message = 'score is not well-formed: {!r}.'
                message = message.format(score)
                message += '\n'
                message += inspect(score).tabulate_well_formedness_violations()
                raise Exception(message)
            scores.append(score)
            markup = block._to_markup(type(self))
            markups.append(markup)
        for markup, score in zip(markups, scores):
            lilypond_file.items.append(markup)
            lilypond_file.items.append(score)
        lilypond_file.default_paper_size = ('letter', 'portrait')
        lilypond_file.global_staff_size = 10
        lilypond_file.use_relative_includes = True
        stylesheet_path = os.path.join(
            '..', '..', '..', 
            'stylesheets', 
            'gallery-layout.ly',
            )
        lilypond_file.file_initial_user_includes.append(stylesheet_path)
        lilypond_file.paper_block.tagline = markuptools.Markup('')
        return lilypond_file

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

    def _write_gallery_to_disk(self):
        lilypond_file = self._gallery_input_to_lilypond_file()
        file_path = __file__
        directory_path = os.path.dirname(file_path)
        class_name = type(self).__name__
        file_name = '{}.pdf'.format(class_name)
        file_path = os.path.join(directory_path, 'gallery', file_name)
        persist(lilypond_file).as_pdf(file_path, remove_ly=True)

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
        arguments = {
            'denominator_multiplier_exponent': 
                self.denominator_multiplier_exponent,
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'decrease_durations_monotonically': 
                decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        new = type(self)(**arguments)
        return new
