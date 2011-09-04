import copy
from collections import Iterable
from numbers import Number
from abjad import Container
from abjad import Fraction
from abjad import Note
from abjad import Tuplet
from abjad.core import _Immutable
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import divisors
from abjad.tools.mathtools import greatest_power_of_two_less_equal
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.quantizationtools.is_valid_beatspan import is_valid_beatspan
from abjad.tools.sequencetools import all_are_numbers
from abjad.tools.sequencetools import flatten_sequence


class QGrid(_Immutable):
    '''Abjad model of a QGrid, a nesting division structure which
    assists certain quantization algorithms.

    `QGrids` are defined by a list, which must be prime in length,
    whose members are either Numbers or tuples of Numbers (useful for
    representing timepoint or pitch information), a
    :py:class:`~abjad.tools.quantizationtools.QEvent` or tuple of
    :py:class:`~abjad.tools.quantizationtools.QEvent` objects, or None
    (representing silence), or other lists which must recursively
    obey the same rules.

    `QGrids` also have a `next` attribute, representing the downbeat of
    not "this" `QGrid`, but the next `QGrid` in a list of grids.  This is
    useful as timepoints must often be quantized not to any internal
    division of a the "current" beat, but to the next beat.

    ::

        abjad> from abjad.tools.quantizationtools import QGrid
        abjad> q = QGrid([0, 0, [0, 0]], 0)

    The values in the grid can be access via subscript, as though
    the grid were a flat list.

    ::

        abjad> q[0] = 1
        abjad> q[2] = 3
        abjad> q[4] = 5
        abjad> q
        QGrid([1, 0, [3, 0]], 5)

    `QGrids` are quasi-immutable.
    '''

    __slots__ = ('_definition', '_next', '_offsets')

    def __new__(klass, definition, next):
        self = object.__new__(klass)
        assert self._is_valid_grid_definition(definition)
        assert self._is_valid_grid_value(next)
        object.__setattr__(self, '_definition', definition)
        object.__setattr__(self, '_next', next)
        object.__setattr__(self, '_offsets', self._expand_offsets())
        return self

    def __getnewargs__(self):
        return self._definition, self._next

    # OVERRIDES #

    def __eq__(self, other):
        if type(self) == type(other) and \
            self._definition == other._definition and \
            self._next == other._next:
            return True
        return False

    def __getitem__(self, item):
        if not isinstance(item, int):
            return None
        if item < 0:
            item = len(self) + item
        if item < 0 or len(self) <= item:
            return None

        for i, x in enumerate(self):
            if i == item:
                return x

    def __iter__(self):
        seq = flatten_sequence(self._definition, klasses=list)
        seq.append(self._next)
        for x in seq:
            yield x

    def __len__(self):
        return len(self.offsets)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __setitem__(self, item, value):
        def recurse(n, item, value, prev_count):
            count = prev_count
            for i, x in enumerate(n):
                if isinstance(x, list):
                    count = recurse(x, item, value, count)
                else:
                    if count == item:
                        n[i] = value
                    count += 1
            return count

        if not isinstance(item, int):
            raise ValueError('Index must be an int.')
        if item < 0:
            item = len(self) + item
        if item < 0 or len(self) <= item:
            raise Exception('Index out of bounds.')

        if not self._is_valid_grid_value(value):
            raise ValueError

        if item == len(self) - 1:
            object.__setattr__(self, '_next', value)
        else:
            recurse(self._definition, item, value, 0)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%s, %s' % (self._definition, self._next)

    ### PRIVATE METHODS ###

    def _expand_offsets(self):
        def recurse(n, prev_div, prev_offset):
            results = []
            this_div = Fraction(1, len(n)) * prev_div
            for i, x in enumerate(n):
                this_offset = Offset(i * this_div) + prev_offset
                if isinstance(x, list):
                    results.extend(recurse(x, this_div, this_offset))
                else:
                    results.append(this_offset)
            return results
        expanded = list(recurse(self._definition, 1, 0))
        expanded.append(Offset(1))
        return tuple(expanded)

    def _is_valid_grid_definition(self, definition):
        def recurse(n):
            if not isinstance(n, list) or \
                not all([isinstance(x, list) or \
                    self._is_valid_grid_value(x) for x in n]) or \
                not set(divisors(len(n))) == set([1, len(n)]):
                return [False]
            results = []
            for x in n:
                if isinstance(x, list):
                    results.extend(recurse(x))
                else:
                    results.append(self._is_valid_grid_value(x))
            return results
        return all(recurse(definition))

    def _is_valid_grid_value(self, value):
        if isinstance(value, (Number, type(None), QEvent)):
            return True
        elif isinstance(value, tuple):
            if 0 < len(value):
                if all([isinstance(x, Number) for x in value]) or \
                    all([isinstance(x, QEvent) for x in value]):
                    return True
            else:
                return True
        return False

    ### PUBLIC ATTRIBUTES ###

    @property
    def definition(self):
        '''The nested list which defines the `QGrid's` structure.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, 0, [0, 0]], 0)
            abjad> q.definition
            [0, 0, [0, 0]]

        Read-only.
        '''

        return copy.deepcopy(self._definition)

    @property
    def next(self):
        '''The contents of the final offset in the `QGrid.`

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, 0, [0, 0]], 0)
            abjad> q[-1] = 9
            abjad> q
            QGrid([0, 0, [0, 0]], 9)
            abjad> q.next
            9

        Read-only.
        '''

        return self._next

    @property
    def offsets(self):
        '''An ordered tuple of those :py:class:`~abjad.tools.durationtools.Offset`
        objects generated by the division structure of a `QGrid`.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, [0, 0], 0], 0)
            abjad> q.offsets
            (Offset(0, 1), Offset(1, 3), Offset(1, 2), Offset(2, 3), Offset(1, 1))

        Read-only.
        '''

        return self._offsets

    ### PUBLIC METHODS ###

    def find_parentage_of_index(self, index):
        '''Return a tuple of the lengths of each container containing `index`,
        from the topmost to the bottommost.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, [0, [0, 0], 0], 0, 0, 0], 0)
            abjad> q.find_parentage_of_index(0)
            (5,)
            abjad> q.find_parentage_of_index(1)
            (5, 3)
            abjad> q.find_parentage_of_index(2)
            (5, 3, 2)
            abjad> q.find_parentage_of_index(7)
            (5,)

        Returns a tuple.
        '''

        if index < 0:
            index = len(self) + index
        if index < 0 or len(self) <= index:
            return None
        if index == len(self) - 1:
            return None
        def recurse(n, index, prev_count):
            results = []
            count = prev_count
            for i, x in enumerate(n):
                if isinstance(x, list):
                    subcount, subresults = recurse(x, index, count)
                    count = subcount
                    if subresults:
                        results = [len(n)]
                        results.extend(subresults)
                        return count, results
                else:
                    if index == count:
                        return count, [len(n)]
                    count += 1
            return count, results
        return tuple(recurse(self.definition, index, 0)[1])

    def find_divisible_indices(self, points):
        '''Given a list of numbers 0 <= n <= 1, return a list of indices in self
        which countain those points, as though they were segments.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, [0, 0]], 0)
            abjad> q.offsets
            (Offset(0, 1), Offset(1, 2), Offset(3, 4), Offset(1, 1))
            abjad> points = [0.1, 0.9]
            abjad> q.find_divisible_indices(points)
            [0, 2]

        Returns a list.
        '''

        assert all_are_numbers(points)
        points = filter(lambda x: 0 <= x <= 1, points)
        offsets = self.offsets
        indices = []
        for i in range(len(offsets) - 1):
            filtered = filter(lambda x: offsets[i] < x < offsets[i + 1], points)
            if filtered:
                indices.append(i)
        return indices

    def format_for_beatspan(self, beatspan = Fraction(1, 4)):
        '''Return an Abjad container, whose structure mirrors the
        division structure of the `QGrid`.  The values of the items in
        the `QGrid` have no effect on the output.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, [0, 0], 0], 0)
            abjad> q.format_for_beatspan()
            Tuplet(2/3, [c'8, c'16, c'16, c'8])

        Returns a :py:class:`~abjad.tools.tuplettools.Tuplet` or
        :py:class:`~abjad.tools.containertools.Container`, depending on
        structure.
        '''

        assert is_valid_beatspan(beatspan)

        def recurse(n, division):
            pow = greatest_power_of_two_less_equal(len(n))
            val = Fraction(1, pow) * division
            if divisors(len(n)) in [[1], [1, 2]]:
                c = Container([])
            else: # we are in a non-2 prime container, hence tuplet
                c = Tuplet(Fraction(pow, len(n)), [])
            for x in n:
                if isinstance(x, list):
                    if len(x) in [1, 2]:
                        c.extend(recurse(x, val))
                    else:
                        c.append(recurse(x, val))
                else:
                    c.append(Note(0, val))
            return c
        return recurse(self.definition, beatspan)

    def subdivide_indices(self, pairs):
        '''Given a list of 2-tuples, where for each tuple t,
        t[0] is a valid index into self, and t[1] is a prime integer
        greater than 1, return a new `QGrid` with those indices subdivided.

        ::

            abjad> from abjad.tools.quantizationtools import QGrid
            abjad> q = QGrid([0, 0], 0)
            abjad> q.subdivide_indices([(0, 2), (1, 3)])
            QGrid([[0, 0], [0, 0, 0]], 0)

        Returns a new `QGrid`.
        '''

        # add some validation here
        assert isinstance(pairs, Iterable) and \
            all([isinstance(x, Iterable) and len(x) == 2 for x in pairs]) and \
            all([0 <= x[0] < len(self) - 1 for x in pairs]) and \
            all([set(divisors(x[1])) == set([1, x[1]]) for x in pairs])
        pairs = sorted(pairs, key = lambda x: x[0])
        def recurse(n, prev_count):
            count = prev_count
            for i, x in enumerate(n):
                if isinstance(x, list):
                    count = recurse(x, count)
                else:
                    for pair in filter(lambda x: x[0] == count, pairs):
                        n[i] = [0] * pair[1]
                        pairs.pop(pairs.index(pair))
                    count += 1
            return count
        definition = copy.deepcopy(self.definition)
        recurse(definition, 0)
        return QGrid(definition, self.next)
