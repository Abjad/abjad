import abc
import copy
from abjad.tools import beamtools
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
import types


class BurnishedRhythmMaker(RhythmMaker):
    '''.. versionadded:: 2.8

    Abstract base class for time token makers that burnish some or
    all of the time tokens they produce.

    'Burnishing' means to forcibly cast the first or last 
    (or both first and last) elements of a time token to be 
    either a note or rest.

    'Token-burnishing' time token makers burnish every time token they produce.

    'Output-burnishing' time token makers burnish only the first and last 
    time tokens they produce and leave interior time tokens unchanged.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    _default_mandatory_input_arguments = ([-1, 4, -2, 3], 16, )

    ### INITIALIZER ###

    def __init__(self, talea, denominator, prolation_addenda=None,
        lefts=None, middles=None, rights=None, left_lengths=None, right_lengths=None,
        secondary_divisions=None,
        talea_helper=None, prolation_addenda_helper=None,
        lefts_helper=None, middles_helper=None, rights_helper=None,
        left_lengths_helper=None, right_lengths_helper=None, secondary_divisions_helper=None,
        beam_each_cell=False,
        big_endian=True, tie_rests=False
        ):
        RhythmMaker.__init__(self)
        prolation_addenda = self._none_to_new_list(prolation_addenda)
        lefts = self._none_to_new_list(lefts)
        middles = self._none_to_new_list(middles)
        rights = self._none_to_new_list(rights)
        left_lengths = self._none_to_new_list(left_lengths)
        right_lengths = self._none_to_new_list(right_lengths)
        secondary_divisions = self._none_to_new_list(secondary_divisions)
        talea_helper = self._none_to_trivial_helper(talea_helper)
        prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
        lefts_helper = self._none_to_trivial_helper(lefts_helper)
        middles_helper = self._none_to_trivial_helper(middles_helper)
        rights_helper = self._none_to_trivial_helper(rights_helper)
        left_lengths_helper = self._none_to_trivial_helper(left_lengths_helper)
        right_lengths_helper = self._none_to_trivial_helper(right_lengths_helper)
        secondary_divisions_helper = self._none_to_trivial_helper(secondary_divisions_helper)
        assert sequencetools.all_are_integer_equivalent_numbers(talea)
        assert mathtools.is_positive_integer_equivalent_number(denominator)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
        assert all([x in (-1, 0, 1) for x in lefts])
        assert all([x in (-1, 0, 1) for x in middles])
        assert all([x in (-1, 0, 1) for x in rights])
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(left_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(right_lengths)
        assert sequencetools.all_are_nonnegative_integer_equivalent_numbers(secondary_divisions)
        assert isinstance(talea_helper, (types.FunctionType, types.MethodType))
        assert isinstance(prolation_addenda_helper, (types.FunctionType, types.MethodType))
        assert isinstance(lefts_helper, (types.FunctionType, types.MethodType))
        assert isinstance(middles_helper, (types.FunctionType, types.MethodType))
        assert isinstance(rights_helper, (types.FunctionType, types.MethodType))
        assert isinstance(left_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(right_lengths_helper, (types.FunctionType, types.MethodType))
        assert isinstance(big_endian, bool)
        assert isinstance(tie_rests, bool)
        self.talea = talea
        self.denominator = denominator
        self.prolation_addenda = prolation_addenda
        self.lefts = lefts
        self.middles = middles
        self.rights = rights
        self.left_lengths = left_lengths
        self.right_lengths = right_lengths
        self.secondary_divisions = secondary_divisions
        self.talea_helper = talea_helper
        self.prolation_addenda_helper = prolation_addenda_helper
        self.lefts_helper = lefts_helper
        self.middles_helper = middles_helper
        self.rights_helper = rights_helper
        self.left_lengths_helper = left_lengths_helper
        self.right_lengths_helper = right_lengths_helper
        self.secondary_divisions_helper = secondary_divisions_helper
        self.beam_each_cell = beam_each_cell
        self.big_endian = big_endian
        self.tie_rests = tie_rests

    ### SPECIAL METHODS ###

    def __call__(self, duration_tokens, seeds=None):
        duration_pairs, seeds = RhythmMaker.__call__(self, duration_tokens, seeds)
        octuplet = self._prepare_input(seeds)
        talea, prolation_addenda = octuplet[:2]
        secondary_divisions = octuplet[-1]
        signals = (talea, prolation_addenda, secondary_divisions)
        result = self._scale_signals(duration_pairs, self.denominator, signals)
        duration_pairs, lcd, talea, prolation_addenda, secondary_divisions = result
        secondary_duration_pairs = self._make_secondary_duration_pairs(
            duration_pairs, secondary_divisions)
        septuplet = (talea, prolation_addenda) + octuplet[2:-1]
        numeric_map = self._make_numeric_map(secondary_duration_pairs, septuplet)
        leaf_lists = self._make_leaf_lists(numeric_map, lcd)
        if not prolation_addenda:
            result = leaf_lists
        else:
            tuplets = self._make_tuplets(secondary_duration_pairs, leaf_lists)
            result = tuplets
        if self.beam_each_cell:
            for cell in result:
                beamtools.MultipartBeamSpanner(cell)
        return result

    def __eq__(self, other):
        return isinstance(other, type(self)) and all([
            self.talea == other.talea,
            self.denominator == other.denominator,
            self.prolation_addenda == other.prolation_addenda,
            self.lefts == other.lefts,
            self.middles == other.middles,
            self.rights == other.rights,
            self.left_lengths == other.left_lengths,
            self.right_lengths == other.right_lengths,
            self.secondary_divisions == other.secondary_divisions,
            #self.talea_helper == other.talea_helper,
            #self.prolation_addenda_helper == other.prolation_addenda_helper,
            #self.lefts_helper == other.lefts_helper,
            #self.middles_helper == other.middles_helper,
            #self.rights_helper == other.rights_helper,
            #self.left_lengths_helper == other.left_lengths_helper,
            #self.right_lengths_helper == other.right_lengths_helper,
            #self.secondary_divisons_helper == other.secondary_divisions_helper,
            ])    

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _force_token_parts(self, tokens, quintuplet):
        pass

    def _force_token_part(self, token_part, indicator):
        assert len(token_part) == len(indicator)
        new_token_part = []
        for number, i in zip(token_part, indicator):
            if i == -1:
                new_token_part.append(-abs(number))
            elif i == 0:
                new_token_part.append(number)
            elif i == 1:
                new_token_part.append(abs(number))
            else:
                raise ValueError
        new_token_part = type(token_part)(new_token_part)
        return new_token_part

    def _make_leaf_lists(self, numeric_map, denominator):
        leaf_lists = []
        for map_token in numeric_map:
            leaf_list = leaftools.make_leaves_from_talea(
                map_token, denominator, big_endian=self.big_endian, tie_rests=self.tie_rests)
            leaf_lists.append(leaf_list)
        return leaf_lists

    def _make_numeric_map(self, duration_pairs, septuplet):
        talea, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
        prolated_duration_pairs = self._make_prolated_duration_pairs(
            duration_pairs, prolation_addenda)
        if isinstance(prolated_duration_pairs[0], tuple):
            prolated_numerators = [pair[0] for pair in prolated_duration_pairs]
        else:
            prolated_numerators = [pair.numerator for pair in prolated_duration_pairs]
        map_tokens = sequencetools.split_sequence_extended_to_weights(
            talea, prolated_numerators, overhang=False)
        quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
        forced_map_tokens = self._force_token_parts(map_tokens, quintuplet)
        numeric_map = forced_map_tokens
        return numeric_map

    def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
        prolated_duration_pairs = []
        for i, duration_pair in enumerate(duration_pairs):
            if not prolation_addenda:
                prolated_duration_pairs.append(duration_pair)
            else:
                prolation_addendum = prolation_addenda[i]
                if hasattr(duration_pair, 'numerator'):
                    prolation_addendum %= duration_pair.numerator
                else:
                    prolation_addendum %= duration_pair[0]
                if isinstance(duration_pair, tuple):
                    numerator, denominator = duration_pair
                else:
                    numerator, denominator = duration_pair.pair
                prolated_duration_pair = (numerator + prolation_addendum, denominator)
                prolated_duration_pairs.append(prolated_duration_pair)
        return prolated_duration_pairs

    def _prepare_input(self, seeds):
        talea = sequencetools.CyclicTuple(self.talea_helper(self.talea, seeds))
        prolation_addenda = self.prolation_addenda_helper(self.prolation_addenda, seeds)
        prolation_addenda = sequencetools.CyclicTuple(prolation_addenda)
        lefts = sequencetools.CyclicTuple(self.lefts_helper(self.lefts, seeds))
        middles = sequencetools.CyclicTuple(self.middles_helper(self.middles, seeds))
        rights = sequencetools.CyclicTuple(self.rights_helper(self.rights, seeds))
        left_lengths = sequencetools.CyclicTuple(self.left_lengths_helper(self.left_lengths, seeds))
        right_lengths = sequencetools.CyclicTuple(self.right_lengths_helper(self.right_lengths, seeds))
        secondary_divisions = self.secondary_divisions_helper(self.secondary_divisions, seeds)
        secondary_divisions = sequencetools.CyclicTuple(secondary_divisions)
        return talea, prolation_addenda, \
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions

    ### PUBLIC METHODS ###

    
    def reverse(self):
        '''.. versionadded:: 2.10

        Reverse burnished rhythm maker.

        .. note:: method is provisional.

        Defined equal to reversal of the following on a copy of rhythm maker::

            new.talea
            new.prolation_addenda
            new.lefts
            new.middles
            new.rights
            new.left_lengths
            new.right_lengths
            new.secondary_divisions

        Return newly constructed rhythm maker.
        '''
        new = copy.deepcopy(self)
        new.talea.reverse()
        new.prolation_addenda.reverse()
        new.lefts.reverse()
        new.middles.reverse()
        new.rights.reverse()
        new.left_lengths.reverse()
        new.right_lengths.reverse()
        new.secondary_divisions.reverse()
        if new.big_endian:
            new.big_endian = False
        return new
