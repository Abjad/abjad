from itertools import groupby
from abjad import Chord
from abjad import Container
from abjad import Fraction
from abjad import Rest
from abjad import Tuplet
from abjad.tools.contexttools import TempoMark
from abjad.tools.leaftools import fuse_leaves_big_endian
from abjad.tools.leaftools import fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
from abjad.tools.marktools import Annotation
from abjad.tools.resttools import yield_groups_of_rests_in_sequence
from abjad.tools.quantizationtools.QGrid import QGrid
from abjad.tools.quantizationtools.QGridSearchTree import QGridSearchTree
from abjad.tools.quantizationtools.QGridTempoLookup import QGridTempoLookup
from abjad.tools.quantizationtools._Quantizer import _Quantizer
from abjad.tools.quantizationtools.is_valid_beatspan import is_valid_beatspan
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
    import tempo_scaled_rational_to_milliseconds
from abjad.tools.sequencetools import flatten_sequence
from abjad.tools.sequencetools import iterate_sequence_pairwise_strict
from abjad.tools.sequencetools import yield_outer_product_of_sequences
from abjad.tools.spannertools import MultipartBeamSpanner
from abjad.tools.tietools import TieSpanner
from abjad.tools.tietools import get_tie_chain
from abjad.tools.tietools import get_tie_chains_in_expr
from abjad.tools.tietools import remove_tie_spanners_from_components_in_expr


class QGridQuantizer(_Quantizer):
    '''An Abjad implementation of Paul Nauert's Q-grid quantization algorithm.

    Input is converted into timepoints, which are grouped according to which
    beat - or `beatspan` - they fall in, given a target tempo.  Each beatspan
    is then divided into grids called Q-grids, which are based upon a nesting
    division structure (similar to nested tuplets).  The Q-grids generated for
    each beatspan are then tested against the timepoints falling within that
    beatspan, and the grid with least deviation is chosen to represent the
    rhythmic skeleton for that beat.

    ::

        abjad> from abjad.tools.quantizationtools import QGridQuantizer
        abjad> q = QGridQuantizer()

    `QGridQuantizer` is immutable, but cheap to instantiate.  Various attributes
    can be defined on instantiation.  Please consult the documentation for each
    attribute respectively, for proper usage.

    ::

        abjad> from abjad.tools.quantizationtools import QGridSearchTree
        abjad> target_tempo = contexttools.TempoMark((1, 8), 73)
        abjad> beatspan = Fraction(1, 4)
        abjad> search_tree = QGridSearchTree({2: {2: None, 3: None}, 5: None})
        abjad> threshold = 250
        abjad> q = QGridQuantizer(tempo = target_tempo, beatspan = beatspan, search_tree = search_tree, threshold = threshold)

    `QGridQuantizer` can quantize lists of leaves.  If the source leaves have no effective tempo,
    one must be provided with the `tempo` keyword.

    ::

        abjad> q = QGridQuantizer()
        abjad> source = Staff("c'4 d'4 e'4. r'8 <c' e' g'>2. <d' g' b'>4")
        abjad> source_tempo = contexttools.TempoMark((1, 4), 54)
        abjad> result = q(source[:], tempo = source_tempo)

    ::

        abjad> q = QGridQuantizer()
        abjad> source = Staff("c'4 d'4 e'4. r'8 <c' e' g'>2. <d' g' b'>4")
        abjad> t = contexttools.TempoMark((1, 8), 34, target_context = Staff)(source)
        abjad> t = contexttools.TempoMark((1, 4), 135, target_context = Staff)(source[3])
        abjad> result = q(source[:])

    `QGridQuantizer` can quantize lists of millisecond durations.  Negative values can be used
    to indicate silences.

    ::

        abjad> q = QGridQuantizer()
        abjad> milliseconds = [100, 120, -133, 500, -1003, 125]
        abjad> result = q(milliseconds)

    `QGridQuantizer` can also quantize lists of rationals, if a tempo is provided.  As with
    quantizing millisecond durations, negative values can be used to indicate silences.

    ::

        abjad> q = QGridQuantizer()
        abjad> rationals = [1, Fraction(1, 2), Fraction(-1, 4), 3, Fraction(-1, 3), 2]
        abjad> tempo = contexttools.TempoMark((1, 4), 45)
        abjad> result = q(rationals, tempo = tempo)

    Lastly, `QGridQuantizer` can quantize lists of pairs, where the first value in each pair
    is a millisecond duration, and the second value is an int or float - indicating a single pitch -,
    None - indicating silence, or a list of ints or floats - indicating a chord.  This is
    probably most useful for assisting in the importation of audio analyses from other tools.

    ::

        abjad> q = QGridQuantizer()
        abjad> pairs = [(130, 0), (250, 2), (500, None), (1303, [0, 1, 4])]
        abjad> result = q(pairs)

    .. todo :: Write a documentation chapter on quantization.
    .. todo :: Implement multiprocessing-based QGrid comparison
    '''

    __slots__ = ('_beatspan', '_beatspan_ms', '_search_tree', '_tempo', '_tempo_lookup', '_threshold')

    def __init__(self,
        search_tree = None,
        beatspan = Fraction(1, 4),
        tempo = TempoMark(Fraction(1, 4), 60),
        threshold = None):

        assert isinstance(search_tree, (type(None), QGridSearchTree))
        if search_tree is None:
            search_tree = QGridSearchTree()
        assert is_valid_beatspan(beatspan)
        assert isinstance(tempo, TempoMark)
        if threshold is not None:
            assert 0 < threshold
            search_tree = search_tree.prune(beatspan, tempo, threshold)

        object.__setattr__(self, '_beatspan', beatspan)
        object.__setattr__(self, '_beatspan_ms',
            tempo_scaled_rational_to_milliseconds(beatspan, tempo))
        object.__setattr__(self, '_search_tree', search_tree)
        object.__setattr__(self, '_tempo', tempo)
        object.__setattr__(self, '_tempo_lookup', QGridTempoLookup(search_tree, beatspan, tempo))
        object.__setattr__(self, '_threshold', threshold)

    ### PRIVATE METHODS ###

    def _compare_q_events_to_q_grid(self, offsets, q_events, q_grid, verbose = False):
        indices = []
        error = 0

        for i, offset in enumerate(offsets):
            q = q_grid.offsets[0]
            best_index = 0
            best_error = abs(q - offset)

            for j, q in enumerate(q_grid.offsets[1:], start = 1):
                curr_error = abs(q - offset)
                if curr_error < best_error:
                    best_index = j
                    best_error = curr_error

            best_index_contents = q_grid[best_index]
            if best_index_contents == 0:
                q_grid[best_index] = (q_events[i],)
            elif isinstance(best_index_contents, tuple):
                new_contents = list(best_index_contents)
                new_contents.append(q_events[i])
                q_grid[best_index] = tuple(new_contents)

            error += best_error

        return error

    def _divide_grid(self, grid, offsets, verbose = False):
        def recurse(grid, offsets):
            results = []
            indices = grid.find_divisible_indices(offsets)
            divisors = [self.search_tree.find_subtree_divisibility(
                grid.find_parentage_of_index(index))
                for index in indices]
            filtered = filter(lambda x: x[1], zip(indices, divisors))
            if not filtered:
                return results
            indices = [x[0] for x in filtered]
            combinations = yield_outer_product_of_sequences([x[1] for x in filtered])
            for combination in combinations:
                zipped = zip(indices, combination)
                results.append(grid.subdivide_indices(zipped))
                results.extend(recurse(results[-1], offsets))
            return results
        return recurse(grid, offsets)

    def _find_best_q_grid_foreach_q_event_group(self, q_event_groups, verbose = False):
        best_q_grids = {}

        for beatspan_number, group in q_event_groups.iteritems():

            errors = []
            q_grids = []

            mod_offsets = [Fraction(x.offset % self.beatspan_ms) / self.beatspan_ms for x in group]

            q_grids.append(QGrid([0], 0))
            for divisor in self.search_tree:
                q_grid = QGrid([0] * divisor, 0)
                q_grids.append(q_grid)
                q_grids.extend(self._divide_grid(q_grid, mod_offsets))

            for q_grid in q_grids:
                errors.append(self._compare_q_events_to_q_grid(mod_offsets, group, q_grid))

            pairs = zip(errors, q_grids)
            pairs.sort(key = lambda x: (x[0], len(x[1])))

            best_q_grids[beatspan_number] = pairs[0][1]

        return best_q_grids

    def _format_all_q_grids(self, best_q_grids, verbose = False):
        beatspan_numbers = sorted(best_q_grids.keys())

        # store indices of tie-chain starts
        indices = []
        pitches = []
        carry = 0
        for beatspan_number in beatspan_numbers:
            q_grid = best_q_grids[beatspan_number]
            for i, x in enumerate(q_grid):
                if isinstance(x, tuple):
                    indices.append(i + carry)
                    pcs = filter(lambda z: z is not None, flatten_sequence([y.value for y in x]))
                    if len(pcs) == 0:
                        pcs = [None]
                    pitches.append(pcs)
            carry += len(q_grid) - 1 # account of q_grid.next

        # remove terminating silence if it is the only event in the last grid
        final_grid = best_q_grids[beatspan_numbers[-1]]
        if len(final_grid) == 2:
            if len(final_grid[0]) == 1:
                best_q_grids.pop(beatspan_numbers[-1])
                beatspan_numbers.pop(-1)

        # make bare notation
        container = Container()
        for beatspan_number in beatspan_numbers:
            q_grid = best_q_grids[beatspan_number]
            formatted = q_grid.format_for_beatspan(self.beatspan)
            if 1 < len(formatted):
                MultipartBeamSpanner(formatted)
            if isinstance(formatted, Tuplet): # non-binary
                container.append(formatted)
            else: # binary
                container.extend(formatted)

        # add tie chains
        tie_chains = []
        for i, pair in enumerate(iterate_sequence_pairwise_strict(indices)):
            leaves = container.leaves[pair[0]:pair[1]]
            pitch = pitches[i]
            if 1 < len(leaves) and pitch[0] is not None:
                tie_chains.append(get_tie_chain(TieSpanner(leaves)[0]))
            for leaf in leaves:
                parent = leaf._parentage.parent
                idx = parent.index(leaf)
                if len(pitch) == 1:
                    if pitch[0] is None:
                        parent[idx] = Rest(leaf)
                    else:
                        leaf.written_pitch = pitch[0]
                else:
                    parent[idx] = Chord(leaf)
                    parent[idx].written_pitches = pitch

        # rest any trailing, untied leaves
        trailing = container.leaves[indices[-1]:]
        if 1 < len(trailing):
            last_tie = TieSpanner(container.leaves[indices[-1]:])
            last_tie_chain = get_tie_chain(last_tie[0])
            last_tie_chain = fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(last_tie_chain)
            last_tie.clear() # detach
            for note in flatten_sequence(last_tie_chain):
                parent = note._parentage.parent
                parent[parent.index(note)] = Rest(note.written_duration)
        elif len(trailing) == 1:
            parent = trailing[0]._parentage.parent
            parent[parent.index(trailing[0])] = Rest(trailing[0].written_duration)

        # fuse tie chains
        for tie_chain in get_tie_chains_in_expr(container.leaves):
            if 1 < len(tie_chain):
                fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(tie_chain)

        # fuse rests
        rest_groups = list(yield_groups_of_rests_in_sequence(container.leaves))
        for rest_group in rest_groups:
            g = groupby(rest_group, lambda x: x._parentage.parent)
            for value, group in g:
                fused = fuse_leaves_big_endian(list(group))
                remove_tie_spanners_from_components_in_expr(fused[0])

        return container

    def _group_q_events_by_beatspan(self, q_events, verbose = False):
        g = groupby(q_events, lambda x: x.offset // self.beatspan_ms)
        grouped_q_events = {}
        for value, group in g:
            grouped_q_events[value] = list(group)
        return grouped_q_events

    def _regroup_and_fill_out_best_q_grids(self, best_q_grids, verbose = False):
        '''Shift events which have been quantized to the last offset
        of one `QGrid` to the first offset of the subsequent grid.
        '''

        # events to be carried
        carried = None

        # cache keys, as the dictionary may be modified
        beatspan_numbers = sorted(best_q_grids.keys())
        for beatspan_number in beatspan_numbers:
            q_grid = best_q_grids[beatspan_number]

            # rolling over the carried events
            if carried:
                if not q_grid[0]:
                    q_grid[0] = carried
                else:
                    zero = list(q_grid[0])
                    zero.extend(carried)
                    q_grid[0] = tuple(sorted(zero, key = lambda x: x.offset))
                carried = None

            # testing if events need to be carried
            if q_grid.next:
                # no grid follows, so create one
                if beatspan_number + 1 not in best_q_grids:
                    best_q_grids[beatspan_number + 1] = QGrid([q_grid.next], 0)
                # another grid follows, so cache the carried events
                else:
                    carried = q_grid.next
                q_grid[-1] = 0

        for i in range(sorted(best_q_grids.keys())[-1]):
            if i not in best_q_grids:
                best_q_grids[i] = QGrid([0], 0)

        return best_q_grids

    def _quantize(self, q_events, verbose = False):

        grouped_q_events = self._group_q_events_by_beatspan(q_events, verbose = verbose)
        best_q_grids = self._find_best_q_grid_foreach_q_event_group(grouped_q_events, verbose = verbose)
        best_q_grids = self._regroup_and_fill_out_best_q_grids(best_q_grids, verbose = verbose)
        container = self._format_all_q_grids(best_q_grids, verbose = verbose)

        return container

    ### PUBLIC ATTRIBUTES ###

    @property
    def beatspan(self):
        '''The basic division of the beat for quantization.

        Read-only, defaults to `Duration(1, 4)`.
        '''
        return self._beatspan

    @property
    def beatspan_ms(self):
        '''The duration of `beatspan` in milliseconds, as determined by `tempo`.

        Read-only, defaults to `Duration(1000)`.
        '''
        return self._beatspan_ms

    @property
    def search_tree(self):
        '''Reference to a :py:class:`~abjad.tools.quantizationtools.QGridSearchTree`
        object, which defines the permissible divisions for each
        :py:class:`~abjad.tools.quantizationtools.QGrid` comprising a quantization
        attempt.

        Read-only, defaults to `QGridSearchTree()`.

        Please consult the documentation for
        :py:class:`~abjad.tools.quantizationtools.QGrid` and
        :py:class:`~abjad.tools.quantizationtools.QGridSearchTree` for more
        information.
        '''
        return self._search_tree

    @property
    def tempo(self):
        '''Reference to a :py:class:`~abjad.tools.contexttools.TempoMark`,
        defining the target tempo for all quantization results.

        Read-only, defaults to `TempoMark((1, 4), 60)`.
        '''
        return self._tempo

    @property
    def tempo_lookup(self):
        '''Reference to a :py:class:`~abjad.tools.quantizationtools.QGridTempoLookup`
        object, a utility class for mapping rational divisions of a beat into
        milliseconds.

        Read-only.
        '''
        return self._tempo_lookup

    @property
    def threshold(self):
        '''Millisecond duration, which if specified at instantiation will be used
        to call the quantizer's :py:class:`~abjad.tools.quantizationtools.QGridSearchTree`'s
        :py:meth:`~abjad.tools.quantizationtools.QGridSearchTree.prune`
        method, in order to generate a pruned search tree for the quantizer, instead of either
        the user-provided or default search trees.

        Read-only, defaults to None.  See the documentation for
        :py:class:`~abjad.tools.quantizationtools.QGridSearchTree` for more
        information on pruning.
        '''
        return self._threshold
