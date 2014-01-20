# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import persist


class RhythmMaker(AbjadObject):
    '''Rhythm-maker abstract base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_cells_together',
        '_beam_each_cell',
        '_decrease_durations_monotonically',
        '_forbidden_written_duration',
        '_name',
        '_tie_across_divisions',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_cells_together=False,
        beam_each_cell=True,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_across_divisions=False,
        ):
        self._beam_each_cell = beam_each_cell
        self._beam_cells_together = beam_cells_together
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically
        self._forbidden_written_duration = forbidden_written_duration
        self._name = None
        self._tie_across_divisions = bool(tie_across_divisions)

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls rhythm-maker.

        Casts `divisions` into duration pairs.

        Reduces numerator and denominator relative to each other.

        Coerces none `seeds` into empty list.

        Returns duration pairs and seed list.
        '''
        duration_pairs = [
            mathtools.NonreducedFraction(x).pair
            for x in divisions
            ]
        seeds = self._to_tuple(seeds)
        music = self._make_music(duration_pairs, seeds)
        if self.tie_across_divisions:
            self._make_ties_across_divisions(music)
        assert isinstance(music, list), repr(music)
        assert len(music), repr(music)
        prototype = (
            scoretools.Tuplet,
            selectiontools.Selection,
            )
        assert all(isinstance(x, prototype) for x in music), repr(music)
        return music

    def __eq__(self, expr):
        r'''Is true when `expr` is a rhythm-maker with type and public
        properties equal to those of this rhythm-maker. Otherwise false.

        Returns boolean.
        '''
        from abjad.tools import systemtools
        if isinstance(expr, type(self)):
            manager = systemtools.StorageFormatManager
            if manager.get_positional_argument_values(self) == \
                manager.get_positional_argument_values(expr):
                nonhelper_keyword_argument_names = [
                    x for x in manager.get_keyword_argument_names(self)
                    if 'helper' not in x]
                for nonhelper_keyword_argument_name in \
                    nonhelper_keyword_argument_names:
                    if not getattr(self, nonhelper_keyword_argument_name) == \
                        getattr(expr, nonhelper_keyword_argument_name):
                        return False
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        Defaults `format_specification=None` to
        `format_specification='storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getstate__(self):
        r'''Gets state of rhythm-maker.

        Returns dictionary.
        '''
        if hasattr(self, '__dict__'):
            return vars(self)
        state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, '__slots__', ()):
                state[slot] = getattr(self, slot, None)
        return state

    def __makenew__(self, *args, **kwargs):
        r'''Makes new rhythm-maker with optional `kwargs`.

        Returns new rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        arguments.update(kwargs)
        maker = type(self)(**arguments)
        return maker

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_tuplets_or_all_are_leaf_lists(expr):
        if all(isinstance(x, scoretools.Tuplet) for x in expr):
            return True
        elif all(RhythmMaker._is_leaf_list(x) for x in expr):
            return True
        else:
            return False

    def _gallery_input_block_to_scores(self, block):
        maker = type(self)(**block.input_)
        scores = []
        for division_list in block.division_lists:
            lists = maker(division_list)
            music = sequencetools.flatten_sequence(lists)
            measures = scoretools.make_spacer_skip_measures(division_list)
            time_signature_context = scoretools.Context(
                measures,
                context_name='TimeSignatureContext',
                name='TimeSignatureContext',
                )
            measures = scoretools.make_spacer_skip_measures(division_list)
            staff = scoretools.Staff(measures)
            staff.context_name = 'RhythmicStaff'
            measures = mutate(staff).replace_measure_contents(music)
            score = scoretools.Score()
            score.append(time_signature_context)
            score.append(staff)
            scores.append(score)
        return scores

    @staticmethod
    def _is_leaf_list(expr):
        return all(isinstance(x, scoretools.Leaf) for x in expr)

    def _gallery_input_to_lilypond_file(self):
        from abjad.tools import lilypondfiletools
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.items.remove(lilypond_file.score_block)
        title_markup = self._make_gallery_title_markup()
        lilypond_file.header_block.title = title_markup
        markups = []
        for block in self._gallery_input_blocks:
            markup = block._to_markup(type(self))
            lilypond_file.items.append(markup)
            scores = self._gallery_input_block_to_scores(block)
            for score in scores:
                score.add_final_bar_line()
                selection = score.select_leaves(start=-1)
                last_leaf = selection[0]
                string = "override Staff.BarLine #'extra-offset = #'(1.6 . 0)"
                command = indicatortools.LilyPondCommand(
                    string,
                    'after',
                    )
                attach(command, last_leaf)
                if not inspect_(score).is_well_formed():
                    message = 'score is not well-formed: {!r}.'
                    message = message.format(score)
                    message += '\n'
                    message += inspect_(score).tabulate_well_formedness_violations()
                    raise Exception(message)
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

    def _make_gallery_title_markup(self):
        string = self._human_readable_class_name
        string = stringtools.capitalize_string_start(string)
        markup = markuptools.Markup(string)
        return markup

    @abc.abstractmethod
    def _make_music(self, duration_pairs, seeds):
        raise NotImplementedError

    def _make_secondary_duration_pairs(
        self,
        duration_pairs,
        secondary_divisions,
        ):
        if not secondary_divisions:
            return duration_pairs[:]
        numerators = [
            duration_pair.numerator
            for duration_pair in duration_pairs
            ]
        secondary_numerators = sequencetools.split_sequence_by_weights(
            numerators,
            secondary_divisions,
            cyclic=True,
            overhang=True,
            )
        secondary_numerators = \
            sequencetools.flatten_sequence(secondary_numerators)
        denominator = duration_pairs[0].denominator
        secondary_duration_pairs = [
            (n, denominator)
            for n in secondary_numerators
            ]
        return secondary_duration_pairs

    def _make_ties_across_divisions(self, music):
        for division_one, division_two in \
            sequencetools.iterate_sequence_pairwise_strict(music):
            leaf_one = iterate(division_one).by_class(
                prototype=scoretools.Leaf,
                reverse=True,
                ).next()
            leaf_two = iterate(division_two).by_class(
                prototype=scoretools.Leaf,
                ).next()
            if not isinstance(leaf_one, scoretools.Note) or \
                not isinstance(leaf_two, scoretools.Note):
                continue
            logical_tie_one = inspect_(leaf_one).get_logical_tie()
            logical_tie_two = inspect_(leaf_two).get_logical_tie()
            for tie in inspect_(leaf_one).get_spanners(spannertools.Tie):
                detach(tie, leaf_one)
            for tie in inspect_(leaf_two).get_spanners(spannertools.Tie):
                detach(tie, leaf_two)
            combined_logical_tie = logical_tie_one + logical_tie_two
            attach(spannertools.Tie(), combined_logical_tie)

    def _make_tuplets(self, duration_pairs, leaf_lists):
        assert len(duration_pairs) == len(leaf_lists)
        tuplets = []
        for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
            tuplet = scoretools.FixedDurationTuplet(duration_pair, leaf_list)
            tuplets.append(tuplet)
        return tuplets

    def _none_to_tuple(self, expr):
        if expr is None:
            expr = ()
        assert isinstance(expr, tuple), expr
        return expr

    def _none_to_trivial_helper(self, expr):
        if expr is None:
            expr = self._trivial_helper
        assert callable(expr)
        return expr

    def _scale_taleas(self, duration_pairs, talea_denominator, taleas):
        dummy_duration_pair = (1, talea_denominator)
        duration_pairs.append(dummy_duration_pair)
        Duration = durationtools.Duration
        duration_pairs = Duration.durations_to_nonreduced_fractions(
            duration_pairs)
        dummy_duration_pair = duration_pairs.pop()
        lcd = dummy_duration_pair.denominator
        multiplier = lcd / talea_denominator
        scaled_taleas = []
        for talea in taleas:
            talea = datastructuretools.CyclicTuple(
                [multiplier * x for x in talea],
                )
            scaled_taleas.append(talea)
        result = [duration_pairs, lcd]
        result.extend(scaled_taleas)
        return tuple(result)

    def _sequence_to_ellipsized_string(self, sequence):
        if not sequence:
            return '[]'
        if len(sequence) <= 4:
            result = ', '.join([str(x) for x in sequence])
        else:
            result = ', '.join([str(x) for x in sequence[:4]])
            result += ', ...'
        result = '[${}$]'.format(result)
        return result

    def _to_tuple(self, expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    def _trivial_helper(self, talea, seeds):
        if isinstance(seeds, int) and len(talea):
            return sequencetools.rotate_sequence(talea, seeds)
        return talea

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
    def beam_cells_together(self):
        r'''Is true when rhythm-maker should beam cells together. Otherwise
        false.

        Returns boolean.
        '''
        return self._beam_cells_together

    @property
    def beam_each_cell(self):
        r'''Is true when rhythm-maker should beam each cell. Otherwise false.

        Returns boolean.
        '''
        return self._beam_each_cell

    @property
    def decrease_durations_monotonically(self):
        r'''Is true when rhythm-maker should decrease durations monotonically.
        Otherwise false.

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def forbidden_written_duration(self):
        r'''Gets forbidden written duration of rhythm-maker.

        Returns duration or none.
        '''
        return self._forbidden_written_duration

    @property
    def name(self):
        r'''Gets name of rhythm-maker.

        Returns string or none.
        '''
        return self._name

    @name.setter
    def name(self, arg):
        assert isinstance(arg, (str, type(None)))
        self._name = arg

    @property
    def tie_across_divisions(self):
        r'''Is true when the last and first leaves of adjacent output tuplets
        should be tied together. Otherwise false.

        Returns boolean.
        '''
        return self._tie_across_divisions

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses rhythm-maker.

        Concrete rhythm-makers should override this method.

        Returns new rhythm-maker.
        '''
        decrease_durations_monotonically = \
            not self.decrease_durations_monotonically
        maker = new(
            self,
            decrease_durations_monotonically=decrease_durations_monotonically,
            )
        return maker
