# -*- encoding: utf-8 -*-
import abc
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject


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
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beam_cells_together=False,
        beam_each_cell=True,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        ):
        self._beam_each_cell = beam_each_cell
        self._beam_cells_together = beam_cells_together
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically
        self._forbidden_written_duration = forbidden_written_duration
        self._name = None

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, divisions, seeds=None):
        r'''Casts `divisions` into duration pairs.
        Reduces numerator and denominator relative to each other.

        Changes none `seeds` into empty list.

        Returns duration pairs and seed list.
        '''
        duration_pairs = [mathtools.NonreducedFraction(x).pair 
            for x in divisions]
        seeds = self._to_tuple(seeds)
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

    def _to_tuple(self, expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    def _none_to_tuple(self, expr):
        if expr is None:
            expr = ()
        assert isinstance(expr, tuple), expr
        return expr

    def _none_to_trivial_helper(self, expr):
        if expr is None:
            return self._trivial_helper
        return expr

    def _scale_taleas(self, duration_pairs, talea_denominator, taleas):
        dummy_duration_pair = (1, talea_denominator)
        duration_pairs.append(dummy_duration_pair)
        Duration = durationtools.Duration
        duration_pairs = \
            Duration.durations_to_nonreduced_fractions(
            duration_pairs)
        dummy_duration_pair = duration_pairs.pop()
        lcd = dummy_duration_pair.denominator
        multiplier = lcd / talea_denominator
        scaled_taleas = []
        for talea in taleas:
            talea = datastructuretools.CyclicTuple(
                [multiplier * x for x in talea])
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
        result = '[$%s$]' % result
        return result

    def _trivial_helper(self, talea, seeds):
        if isinstance(seeds, int) and len(talea):
            return sequencetools.rotate_sequence(talea, seeds)
        return talea

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

    ### PUBLIC METHODS ###

    def __makenew__(self, *args, **kwargs):
        r'''Makes new rhythm-maker with `kwargs`.

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
        new = type(self)(**arguments)
        return new

    def reverse(self):
        r'''Reverses rhythm-maker.

        Defined equal to exact copy of rhythm-maker.

        This is the fallback for child classes.

        Directed rhythm-maker child classes should override this method.

        Returns newly constructed rhythm-maker.
        '''
        arguments = {
            'beam_cells_together': self.beam_cells_together,
            'beam_each_cell': self.beam_each_cell,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        new = type(self)(**arguments)
        return new
