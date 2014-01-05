# -*- encoding: utf-8 -*-
import os
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.agenttools.InspectionAgent import inspect
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import persist


class EvenRunRhythmMaker(RhythmMaker):
    r'''Even run rhythm-maker.

    ..  container:: example

        **Example 1.** Make even run of notes each equal in duration to ``1/d``
        with ``d`` equal to the denominator of each division on which
        the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker()

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Make even run of notes each equal in duration to
        ``1/(2**d)`` with ``d`` equal to the denominator of each division
        on which the rhythm-maker is called:

        ::

            >>> maker = rhythmmakertools.EvenRunRhythmMaker(1)

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

    Output a list of lists of depth-``2`` note-bearing containers.

    Even-run rhythm-maker doesn't yet work with non-power-of-two divisions.

    Usage follows the two-step instantiate-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = ()

    ### GALLERY INPUT ###

    _gallery_input = (
        ({
            'denominator_multiplier_exponent': 0,
            'beam_each_cell': True,
            'beam_cells_together': False,
            },
            [(4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16)],
            ),

        ({
            'denominator_multiplier_exponent': 1,
            'beam_each_cell': True,
            'beam_cells_together': False,
            },
            [(4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16)],
            ),

        ({
            'denominator_multiplier_exponent': 2,
            'beam_each_cell': True,
            'beam_cells_together': False,
            },
            [(4, 8), (3, 4), (2, 4), (1, 16), (1, 16), (7, 8), (5, 16)],
            ),

        )

    ### INITIALIZER ###

    def __init__(
        self,
        denominator_multiplier_exponent=0,
        beam_each_cell=True,
        beam_cells_together=False,
        ):
        assert mathtools.is_nonnegative_integer(
            denominator_multiplier_exponent)
        RhythmMaker.__init__(
            self,
            beam_each_cell=beam_each_cell,
            beam_cells_together=beam_cells_together
            )
        self._denominator_multiplier_exponent = \
            denominator_multiplier_exponent

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls even-run rhythm-maker on `divisions`.

        Returns list of container lists.
        '''
        result = []
        for division in divisions:
            container = self._make_container(division)
            result.append([container])
        return result

    def __format__(self, format_specification=''):
        r'''Formats even run rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ::

            >>> print format(maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False,
                )

        Returns string.
        '''
        superclass = super(EvenRunRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new even-run rhythm-maker with `kwargs`.

        ::

            >>> new_maker = new(maker, denominator_multiplier_exponent=0)

        ::

            >>> print format(new_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=0,
                beam_each_cell=True,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = new_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Returns new even-run rhythm-maker.
        '''
        return RhythmMaker.__makenew__(self, *args, **kwargs)

    ### PRIVATE METHODS ###

    @staticmethod
    def _gallery_input_block_to_score(gallery_input_block):
        from abjad.tools import sequencetools
        input_dictionary = gallery_input_block[0]
        divisions = gallery_input_block[1]
        maker = EvenRunRhythmMaker(**input_dictionary)
        lists = maker(divisions)
        music = sequencetools.flatten_sequence(lists)
        measures = scoretools.make_spacer_skip_measures(divisions)
        time_signature_context = scoretools.Context(
            measures,
            context_name='TimeSignatureContext',
            name='TimeSignatureContext',
            )
        measures = scoretools.make_spacer_skip_measures(divisions)
        staff = scoretools.RhythmicStaff(measures)
        measures = scoretools.replace_contents_of_measures_in_expr(
            staff, music)
        score = scoretools.Score()
        score.append(time_signature_context)
        score.append(staff)
        return score

    @staticmethod
    def _gallery_input_to_lilypond_file():
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        scores = []
        for gallery_input_block in EvenRunRhythmMaker._gallery_input:
            score = EvenRunRhythmMaker._gallery_input_block_to_score(
                gallery_input_block)
            scores.append(score)
        for score in scores:
            if not inspect(score).is_well_formed():
                message = 'score is not well-formed: {!r}.'
                message = message.format(score)
                message += '\n'
                message += inspect(score).tabulate_well_formedness_violations()
                raise Exception(message)
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.remove(lilypond_file.score_block)
        for i, score in enumerate(scores):
            #title_markup = markuptools.Markup('TITLE MARKUP')
            #lilypond_file.items.append(title_markup)
            score_block = lilypondfiletools.ScoreBlock()
            score_block.items.append(score)
            header_block = lilypondfiletools.HeaderBlock()
            string = r'\italic {{ No. {} }}'.format(i + 1)
            header_block.piece = markuptools.Markup(string)
            score_block.items.append(header_block)
            lilypond_file.items.append(score_block)
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

    @staticmethod
    def _write_gallery_to_disk():
        lilypond_file = EvenRunRhythmMaker._gallery_input_to_lilypond_file()
        file_path = __file__
        directory_path = os.path.dirname(file_path)
        class_name = EvenRunRhythmMaker.__name__
        file_name = '{}.pdf'.format(class_name)
        file_path = os.path.join(directory_path, 'gallery', file_name)
        persist(lilypond_file).as_pdf(file_path, remove_ly=True)

    ### PUBLIC PROPERTIES ###

    @property
    def denominator_multiplier_exponent(self):
        r'''Denominator multiplier exponent provided at initialization.

        ::

            >>> maker.denominator_multiplier_exponent
            1

        Returns nonnegative integer.
        '''
        return self._denominator_multiplier_exponent

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses even-run rhythm-maker:

        ::

            >>> reversed_maker = maker.reverse()

        ::

            >>> print format(reversed_maker)
            rhythmmakertools.EvenRunRhythmMaker(
                denominator_multiplier_exponent=1,
                beam_each_cell=True,
                beam_cells_together=False,
                )

        ::

            >>> divisions = [(4, 8), (3, 4), (2, 4)]
            >>> lists = reversed_maker(divisions)
            >>> music = sequencetools.flatten_sequence(lists)
            >>> measures = \
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions)
            >>> staff = scoretools.RhythmicStaff(measures)
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, music)

        ::

            >>> show(staff) # doctest: +SKIP

        Defined equal to copy of even-run rhythm-maker.

        Returns new even-run rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
