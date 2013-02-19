import abc
import copy
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import sequencetools
from abjad.tools import tuplettools
from abjad.tools.abctools.AbjadObject import AbjadObject


class RhythmMaker(AbjadObject):
    '''.. versionadded:: 2.8

    Rhythm maker abstract base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, beam_each_cell=True, beam_cells_together=False):
        self.beam_each_cell = beam_each_cell
        self.beam_cells_together = beam_cells_together

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        '''Cast `divisions` into duration pairs.
        Reduce numerator and denominator relative to each other.

        Change none `seeds` into empty list.

        Return duration pairs and seed list.
        '''
        duration_pairs = [durationtools.Duration(x).pair for x in divisions]
        seeds = self._none_to_new_list(seeds)
        return duration_pairs, seeds

    def __eq__(self, expr):
        '''True when `expr` is same type
        with the equal public nonhelper properties.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self._positional_argument_values == expr._positional_argument_values:
                nonhelper_keyword_argument_names = [
                    x for x in self._keyword_argument_names if 'helper' not in x]
                for nonhelper_keyword_argument_name in nonhelper_keyword_argument_names:
                    if not getattr(self, nonhelper_keyword_argument_name) == \
                        getattr(expr, nonhelper_keyword_argument_name):
                        return False
                return True
        return False

    def __repr__(self):
        '''Rhythm-maker interpreter representation.

        Return string.
        '''
        if getattr(self, 'name', None) is not None:
            return '{}({!r})'.format(self._class_name, self.name)
        return AbjadObject.__repr__(self)

    ### PRIVATE METHODS ###

    def _all_are_tuplets_or_all_are_leaf_lists(self, expr):
        if tuplettools.all_are_tuplets(expr):
            return True
        elif all([leaftools.all_are_leaves(x) for x in expr]):
            return True
        else:
            return False

    def _make_secondary_duration_pairs(self, duration_pairs, secondary_divisions):
        if not secondary_divisions:
            return duration_pairs[:]
        numerators = [duration_pair.numerator for duration_pair in duration_pairs]
        secondary_numerators = sequencetools.split_sequence_by_weights(
            numerators, secondary_divisions, cyclic=True, overhang=True)
        secondary_numerators = sequencetools.flatten_sequence(secondary_numerators)
        denominator = duration_pairs[0].denominator
        secondary_duration_pairs = [(n, denominator) for n in secondary_numerators]
        return secondary_duration_pairs

    def _make_tuplets(self, duration_pairs, leaf_lists):
        assert len(duration_pairs) == len(leaf_lists)
        tuplets = []
        for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
            tuplet = tuplettools.FixedDurationTuplet(duration_pair, leaf_list)
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
        duration_pairs = durationtools.durations_to_nonreduced_fractions_with_common_denominator(
            duration_pairs)
        dummy_duration_pair = duration_pairs.pop()
        lcd = dummy_duration_pair.denominator
        multiplier = lcd / talea_denominator
        scaled_talee = []
        for talea in talee:
            talea = sequencetools.CyclicTuple([multiplier * x for x in talea])
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
        return talea

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        r'''Create new rhythm-maker with `kwargs`:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 16), (3, 8)]
            >>> leaf_lists = maker.new(decrease_durations_monotonically=False)(divisions)
            >>> leaves = sequencetools.flatten_sequence(leaf_lists)

        ::

            >>> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(divisions))
            >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, leaves)

        ::

            >>> f(staff)
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

        Return new rhythm-maker.
        '''
        new = copy.deepcopy(self)
        for key, value in kwargs.iteritems():
            setattr(new, key, value)
        return new
 
    def reverse(self):
        '''Reverse rhythm-maker.

        .. note:: method is provisional.

        Defined equal to exact copy of rhythm-maker.

        This is the fallback for child classes.

        Directed rhythm-maker child classes should override this method.

        Return newly constructed rhythm-maker.
        '''
        new = copy.deepcopy(self)
        return new
