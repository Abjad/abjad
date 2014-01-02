# -*- encoding: utf-8 -*-
import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class RhythmMaker(AbjadObject):
    '''Rhythm maker abstract base class.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        forbidden_written_duration=None,
        beam_each_cell=True,
        beam_cells_together=False,
        ):
        self.forbidden_written_duration = forbidden_written_duration
        self.beam_each_cell = beam_each_cell
        self.beam_cells_together = beam_cells_together

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Casts `divisions` into duration pairs.
        Reduces numerator and denominator relative to each other.

        Changes none `seeds` into empty list.

        Returns duration pairs and seed list.
        '''
        duration_pairs = [durationtools.Duration(x).pair for x in divisions]
        seeds = self._none_to_new_list(seeds)
        return duration_pairs, seeds

    def __eq__(self, expr):
        r'''Is true when `expr` is same type
        with the equal public nonhelper properties.
        Otherwise false.

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
        r'''Gets object state.
        '''
        return vars(self)

    ### PRIVATE METHODS ###

    # TODO: make static
    def _all_are_tuplets_or_all_are_leaf_lists(self, expr):
        if all(isinstance(x, scoretools.Tuplet) for x in expr):
            return True
        elif all(self._is_leaf_list(x) for x in expr):
            return True
        else:
            return False

    @staticmethod
    def _is_leaf_list(expr):
        return all(isinstance(x, scoretools.Leaf) for x in expr)

    def _make_secondary_duration_pairs(
        self, duration_pairs, secondary_divisions):
        if not secondary_divisions:
            return duration_pairs[:]
        numerators = [duration_pair.numerator
            for duration_pair in duration_pairs]
        secondary_numerators = sequencetools.split_sequence_by_weights(
            numerators, secondary_divisions, cyclic=True, overhang=True)
        secondary_numerators = \
            sequencetools.flatten_sequence(secondary_numerators)
        denominator = duration_pairs[0].denominator
        secondary_duration_pairs = \
            [(n, denominator) for n in secondary_numerators]
        return secondary_duration_pairs

    def _make_tuplets(self, duration_pairs, leaf_lists):
        assert len(duration_pairs) == len(leaf_lists)
        tuplets = []
        for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
            tuplet = scoretools.FixedDurationTuplet(duration_pair, leaf_list)
            tuplets.append(tuplet)
        return tuplets

    def _none_to_new_list(self, expr):
        if expr is None:
            return []
        return expr

    def _none_to_trivial_helper(self, expr):
        if expr is None:
            return self._trivial_helper
        return expr

    def _scale_talee(self, duration_pairs, talea_denominator, talee):
        dummy_duration_pair = (1, talea_denominator)
        duration_pairs.append(dummy_duration_pair)
        Duration = durationtools.Duration
        duration_pairs = \
            Duration.durations_to_nonreduced_fractions(
            duration_pairs)
        dummy_duration_pair = duration_pairs.pop()
        lcd = dummy_duration_pair.denominator
        multiplier = lcd / talea_denominator
        scaled_talee = []
        for talea in talee:
            talea = datastructuretools.CyclicTuple([multiplier * x for x in talea])
            scaled_talee.append(talea)
        result = [duration_pairs, lcd]
        result.extend(scaled_talee)
        return tuple(result)

    def _sequence_to_ellipsized_string(self, sequence):
        if not sequence:
            return '[]'
        if len(sequence) <= 4:
            result = ', '.join([str(x) for x in sequence])
        else:
            result = ', '.join([str(x) for x in sequence[:4]])
            result += ', ...'
        result = '[$%s$]' % result
        return result

    def _trivial_helper(self, talea, seeds):
        if isinstance(seeds, int) and len(talea):
            return sequencetools.rotate_sequence(talea, seeds)
        return talea

    ### PUBLIC METHODS ###

    def __makenew__(self, *args, **kwargs):
        r'''Creates new rhythm-maker with `kwargs`.

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> new_maker = new(maker, decrease_durations_monotonically=False)
            >>> leaf_lists = new_maker(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)

        ::

            >>> staff = Staff(
            ...     scoretools.make_spacer_skip_measures(
            ...     divisions))
            >>> measures = scoretools.replace_contents_of_measures_in_expr(
            ...     staff, leaves)

        ..  doctest::

            >>> print format(staff)
            \new Staff {
                {
                    \time 5/16
                    c'16 ~
                    c'4
                }
                {
                    \time 3/8
                    c'4.
                }
            }

        Returns new rhythm-maker.
        '''
        new_maker = copy.deepcopy(self)
        for key, value in kwargs.iteritems():
            try:
                setattr(new_maker, key, value)
            except AttributeError:
                setattr(new_maker, '_' + key, value)
        return new_maker

    def reverse(self):
        r'''Reverses rhythm-maker.

        .. note:: method is provisional.

        Defined equal to exact copy of rhythm-maker.

        This is the fallback for child classes.

        Directed rhythm-maker child classes should override this method.

        Returns newly constructed rhythm-maker.
        '''
        new = copy.deepcopy(self)
        return new
