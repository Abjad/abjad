# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadObject


class Sequence(AbjadObject):
    r'''A sequence.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        items = items or ()
        if isinstance(items, collections.Iterable):
            items = tuple(items)
        else:
            items = (items,)
        self._items = items

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds `expr` to sequence.

        ..  container:: example

            Adds sequence to sequence:

            ::

                >>> Sequence((1, 2, 3)) + Sequence((4, 5, 6))
                Sequence((1, 2, 3, 4, 5, 6))

            Adds tuple to sequence:

            ::

                >>> Sequence((1, 2, 3)) + (4, 5, 6)
                Sequence((1, 2, 3, 4, 5, 6))

            Adds list to sequence:

            ::

                >>> Sequence((1, 2, 3)) + [4, 5, 6]
                Sequence((1, 2, 3, 4, 5, 6))

        Returns new sequence.
        '''
        expr = type(self)(expr)
        items = self._items + expr._items
        return type(self)(items)

    def __eq__(self, expr):
        r'''Is true when `expr` is a sequence with items equal to those of
        this sequence. Otherwise false.

        ..  container:: example

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)) == Sequence((1, 2, 3, 4, 5, 6))
                True

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)) == ((1, 2, 3, 4, 5, 6))
                False

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self._items == expr._items
        return False

    def __format__(self, format_specification=''):
        r'''Formats sequence.

        ..  container:: example

            **Example.** Prints format:

            ::

                >>> print(format(Sequence((1, 2, 3, 4, 5, 6))))
                sequencetools.Sequence(
                    items=(1, 2, 3, 4, 5, 6),
                    )

        Returns string.
        '''
        return AbjadObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __getitem__(self, i):
        r'''Gets item `i` from sequence.

        ..  container:: example

            **Example.** Gets last item in sequence:

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6))[-1]
                6

        Returns item.
        '''
        result = self._items.__getitem__(i)
        if isinstance(i, slice):
            return type(self)(result)
        return result

    def __hash__(self):
        r'''Hashes sequence.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Sequence, self).__hash__()

    def __len__(self):
        r'''Gets length of sequence.

        ..  container:: example

            Gets length of six-item sequence:

            ::

                >>> len(Sequence((1, 2, 3, 4, 5, 6)))
                6

        Returns nonnegative integer.
        '''
        return len(self._items)

    def __ne__(self, expr):
        r'''Is true when sequence is not equal to `expr`. Otherwise false.

        ..  container:: example

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)) != (1, 2, 3, 4, 5, 6)
                True

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)) != Sequence((1, 2, 3, 4, 5, 6))
                False

        '''
        return not self == expr

    def __radd__(self, expr):
        r'''Adds sequence to `expr`.

        ..  container:: example

            **Example 1.** Adds sequence to sequence:

            ::

                >>> Sequence((1, 2, 3)) + Sequence((4, 5, 6))
                Sequence((1, 2, 3, 4, 5, 6))

        ..  container:: example

            **Example 2.** Adds sequence to tuple:

            ::

                >>> (1, 2, 3) + Sequence((4, 5, 6))
                Sequence((1, 2, 3, 4, 5, 6))

        ..  container:: example

            **Example 3.** Adds sequence to list:

            ::

                >>> [1, 2, 3] + Sequence((4, 5, 6))
                Sequence((1, 2, 3, 4, 5, 6))

        Returns new sequence.
        '''
        expr = type(self)(expr)
        items = expr._items + self._items
        return type(self)(items)

    def __repr__(self):
        r'''Gets interpreter representation of sequence.

        ..  container:: example

            **Example 1.** Gets interpreter representation of sequence with
            length equal to one:

            ::

                >>> Sequence((99,))
                Sequence((99,))

        ..  container:: example

            **Example 2.** Gets interpreter representation of sequence with
            length greater than one:

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6))
                Sequence((1, 2, 3, 4, 5, 6))

        Returns string.
        '''
        items = ', '.join([repr(_) for _ in self.items])
        if len(self.items) == 1:
            items = items + ','
        string = '{}(({}))'
        string = string.format(type(self).__name__, items)
        return string

    ### PUBLIC METHODS ###

    def flatten(self, classes=None, depth=-1, indices=None):
        r'''Flattens sequence.

        ..  container:: example

            **Example 1.** Flattens sequence completely:

            ::

                >>> sequence = Sequence((1, [2, 3, [4]], 5, [6, 7, [8]]))
                >>> sequence.flatten()
                Sequence((1, 2, 3, 4, 5, 6, 7, 8))

        ..  container:: example

            **Example 2.** Flattens `sequence` to depth ``1``:

            ::

                >>> sequence = Sequence((1, [2, 3, [4]], 5, [6, 7, [8]]))
                >>> sequence.flatten(depth=1)
                Sequence((1, 2, 3, [4], 5, 6, 7, [8]))

        ..  container:: example

            **Example 3.** Flattens `sequence` to depth ``2``:

            ::

                >>> sequence = Sequence((1, [2, 3, [4]], 5, [6, 7, [8]]))
                >>> sequence.flatten(depth=2)
                Sequence((1, 2, 3, 4, 5, 6, 7, 8))

        ..  container:: example

            **Example 4.** Flattens `sequence` at `indices`:

            ::

                >>> sequence = Sequence((1, [2, 3, [4]], 5, [6, 7, [8]]))
                >>> sequence.flatten(indices=[3])
                Sequence((1, [2, 3, [4]], 5, 6, 7, 8))

        ..  container:: example

            **Example 5.** Flattens `sequence` at negative `indices`:

            ::

                >>> sequence = Sequence((1, [2, 3, [4]], 5, [6, 7, [8]]))
                >>> sequence.flatten(indices=[-1])
                Sequence((1, [2, 3, [4]], 5, 6, 7, 8))

        ..  container:: example

            **Example 6.** Flattens only tuples in `sequence`:

            ::

                >>> sequence = Sequence(('ab', 'cd', ('ef', 'gh'), ('ij', 'kl')))
                >>> sequence.flatten(classes=(tuple,))
                Sequence(('ab', 'cd', 'ef', 'gh', 'ij', 'kl'))

        Returns new sequence.
        '''
        from abjad.tools import sequencetools
        items = sequencetools.flatten_sequence(
            self._items[:],
            classes=classes,
            depth=depth,
            indices=indices,
            )
        result = type(self)(items)
        return result

    def is_decreasing(self, strict=True):
        r'''Is true when sequence decreases.

        ..  container:: example

            With ``strict=True``:

            ::

                >>> Sequence((5, 4, 3, 2, 1, 0)).is_decreasing(strict=True)
                True

            ::

                >>> Sequence((3, 3, 3, 2, 1, 0)).is_decreasing(strict=True)
                False

            ::

                >>> Sequence((3, 3, 3, 3, 3, 3)).is_decreasing(strict=True)
                False

            ::

                >>> Sequence().is_decreasing(strict=True)
                True

        ..  container:: example

            With ``strict=False``:

            ::

                >>> Sequence((5, 4, 3, 2, 1, 0)).is_decreasing(strict=False)
                True

            ::

                >>> Sequence((3, 3, 3, 2, 1, 0)).is_decreasing(strict=False)
                True

            ::

                >>> Sequence((3, 3, 3, 3, 3, 3)).is_decreasing(strict=False)
                True

            ::

                >>> Sequence().is_decreasing(strict=False)
                True

        Returns true or false.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current < previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current <= previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_increasing(self, strict=True):
        r'''Is true when sequence increases.

        ..  container:: example

            With ``strict=True``:

            ::

                >>> Sequence((0, 1, 2, 3, 4, 5)).is_increasing(strict=True)
                True

            ::

                >>> Sequence((0, 1, 2, 3, 3, 3)).is_increasing(strict=True)
                False

            ::

                >>> Sequence((3, 3, 3, 3, 3, 3)).is_increasing(strict=True)
                False

            ::

                >>> Sequence().is_increasing(strict=True)
                True

        ..  container:: example

            With ``strict=False``:

            ::

                >>> Sequence((0, 1, 2, 3, 4, 5)).is_increasing(strict=False)
                True

            ::

                >>> Sequence((0, 1, 2, 3, 3, 3)).is_increasing(strict=False)
                True

            ::

                >>> Sequence((3, 3, 3, 3, 3, 3)).is_increasing(strict=False)
                True

            ::

                >>> Sequence().is_increasing(strict=False)
                True

        Returns true or false.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous < current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous <= current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_permutation(self, length=None):
        '''Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            ::

                >>> Sequence((4, 5, 0, 3, 2, 1)).is_permutation()
                True

        ..  container:: example

            Is false when sequence is not a permutation:

            ::

                >>> Sequence((1, 1, 5, 3, 2, 1)).is_permutation()
                False

        Returns true or false.
        '''
        return tuple(sorted(self)) == tuple(range(len(self)))

    def is_repetition_free(self):
        '''Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence contains no repetitions:

            ::

                >>> Sequence((0, 1, 2, 6, 7, 8)).is_repetition_free()
                True

            Is true when sequence is empty:

            ::

                >>> Sequence().is_repetition_free()
                True

        ..  container:: example

            Is false when sequence contains repetitions:

            ::

                >>> Sequence((0, 1, 2, 2, 7, 8)).is_repetition_free()
                False

        Returns true or false.
        '''
        from abjad.tools import sequencetools
        try:
            pairs = sequencetools.iterate_sequence_nwise(self)
            for left, right in pairs:
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def is_restricted_growth_function(self):
        '''Is true when sequence is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            ::

                >>> Sequence((1, 1, 1, 1)).is_restricted_growth_function()
                True

            ::


                >>> Sequence((1, 1, 1, 2)).is_restricted_growth_function()
                True

            ::

                >>> Sequence((1, 1, 2, 1)).is_restricted_growth_function()
                True

            ::

                >>> Sequence((1, 1, 2, 2)).is_restricted_growth_function()
                True

        ..  container:: example

            Is false when sequence is not a restricted growth function:

            ::

                >>> Sequence((1, 1, 1, 3)).is_restricted_growth_function()
                False

            ::

                >>> Sequence((17,)).is_restricted_growth_function()
                False

        A restricted growth function is a sequence ``l`` such that
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for
        ``1 <= i <= len(l)``.

        Returns true or false.
        '''
        try:
            for i, n in enumerate(self):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(self[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        overhang=False,
        reversed_=False,
        ):
        r'''Partitions sequence by `counts`.

        ..  container:: example

            **Example 1.** Partitions sequence once by counts without overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2))

        ..  container:: example

            **Example 2.** Partitions sequence once by counts without overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3))
                Sequence((4, 5, 6))

        ..  container:: example

            **Example 3.** Partitions sequence cyclically by counts without
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2))
                Sequence((3, 4, 5))
                Sequence((6, 7, 8))
                Sequence((9, 10, 11))
                Sequence((12, 13, 14))

        ..  container:: example

            **Example 4.** Partitions sequence cyclically by counts without
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3))
                Sequence((4, 5, 6))
                Sequence((7, 8, 9, 10))
                Sequence((11, 12, 13))

        ..  container:: example

            **Example 5.** Partitions sequence once by counts with overhang:

            ::


                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2))
                Sequence((3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))

        ..  container:: example

            **Example 6.** Partitions sequence once by counts with overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3))
                Sequence((4, 5, 6))
                Sequence((7, 8, 9, 10, 11, 12, 13, 14, 15))

        ..  container:: example

            **Example 7.** Partitions sequence cyclically by counts with
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2))
                Sequence((3, 4, 5))
                Sequence((6, 7, 8))
                Sequence((9, 10, 11))
                Sequence((12, 13, 14))
                Sequence((15,))

        ..  container:: example

            **Example 8.** Partitions sequence cyclically by counts with
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3))
                Sequence((4, 5, 6))
                Sequence((7, 8, 9, 10))
                Sequence((11, 12, 13))
                Sequence((14, 15))






        ..  container:: example

            **Example 9.** Reversed-partitions sequence once by counts without
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((13, 14, 15))

        ..  container:: example

            **Example 10.** Reverse-partitions sequence once by counts without
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((9, 10, 11))
                Sequence((12, 13, 14, 15))

        ..  container:: example

            **Example 11.** Reverse-partitions sequence cyclically by counts
            without overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((1, 2, 3))
                Sequence((4, 5, 6))
                Sequence((7, 8, 9))
                Sequence((10, 11, 12))
                Sequence((13, 14, 15))

        ..  container:: example

            **Example 12.** Reverse-partitions sequence cyclically by counts
            without overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((2, 3, 4))
                Sequence((5, 6, 7, 8))
                Sequence((9, 10, 11))
                Sequence((12, 13, 14, 15))

        ..  container:: example

            **Example 13.** Reverse-partitions sequence once by counts with
            overhang:

            ::


                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
                Sequence((13, 14, 15))

        ..  container:: example

            **Example 14.** Reverse-partitions sequence once by counts with
            overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1, 2, 3, 4, 5, 6, 7, 8))
                Sequence((9, 10, 11))
                Sequence((12, 13, 14, 15))

        ..  container:: example

            **Example 15.** Reverse-partitions sequence cyclically by counts
            with overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0,))
                Sequence((1, 2, 3))
                Sequence((4, 5, 6))
                Sequence((7, 8, 9))
                Sequence((10, 11, 12))
                Sequence((13, 14, 15))

        ..  container:: example

            **Example 16.** Reverse-partitions sequence cyclically by counts
            with overhang:

            ::

                >>> sequence_ = Sequence(range(16))
                >>> parts = sequence_.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1))
                Sequence((2, 3, 4))
                Sequence((5, 6, 7, 8))
                Sequence((9, 10, 11))
                Sequence((12, 13, 14, 15))

        ..  container:: example

            **Example 17.** Partitions sequence once by counts and asserts that
            sequence partitions exactly (with no overhang):

            ::

                >>> sequence_ = Sequence(range(10))
                >>> parts = sequence_.partition_by_counts(
                ...     [2, 3, 5],
                ...     cyclic=False,
                ...     overhang=Exact,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1))
                Sequence((2, 3, 4))
                Sequence((5, 6, 7, 8, 9))

        ..  container:: example

            **Example 18.** Partitions sequence cyclically by counts and
            asserts that sequence partitions exactly:

            ::

                >>> sequence_ = Sequence(range(10))
                >>> parts = sequence_.partition_by_counts(
                ...     [2],
                ...     cyclic=True,
                ...     overhang=Exact,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence((0, 1))
                Sequence((2, 3))
                Sequence((4, 5))
                Sequence((6, 7))
                Sequence((8, 9))

            Exact partitioning means partitioning with no overhang.

        ..  container:: example

            **Example 19.** Partitions string:

            ::

                >>> sequence_ = Sequence('some text')
                >>> parts = sequence_.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )
                >>> for part in parts:
                ...     part
                Sequence(('s', 'o', 'm'))
                Sequence(('e', ' ', 't', 'e', 'x', 't'))

        Returns nested sequence.
        '''
        from abjad.tools import sequencetools
        items = self._items[:]
        subsequences = []
        parts = sequencetools.partition_sequence_by_counts(
            items,
            counts,
            cyclic=cyclic,
            overhang=overhang,
            reversed_=reversed_,
            )
        parts = [type(self)(_) for _ in parts]
        sequence = type(self)(parts)
        return sequence

    def partition_by_ratio_of_lengths(self, ratio):
        r'''Partitions sequence by `ratio` of lengths.

        ..  container:: example

            **Example 1.** Partitions sequence by ``1:1:1`` ratio:

            ::

                >>> numbers = Sequence(range(10))
                >>> ratio = mathtools.Ratio((1, 1, 1))
                >>> numbers.partition_by_ratio_of_lengths(ratio)
                Sequence((Sequence((0, 1, 2)), Sequence((3, 4, 5, 6)), Sequence((7, 8, 9))))

        ..  container:: example

            **Example 2.** Partitions sequence by ``1:1:2`` ratio:

            ::

                >>> numbers = Sequence(range(10))
                >>> ratio = mathtools.Ratio((1, 1, 2))
                >>> numbers.partition_by_ratio_of_lengths(ratio)
                Sequence((Sequence((0, 1, 2)), Sequence((3, 4)), Sequence((5, 6, 7, 8, 9))))

        Returns a sequence of sequences.
        '''
        from abjad.tools import sequencetools
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            self.items,
            ratio=ratio,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(parts)

    def reverse(self):
        '''Reverses sequence.

        ..  container:: example

            **Example.**

            ::

                >>> Sequence((1, 2, 3, 4, 5)).reverse()
                Sequence((5, 4, 3, 2, 1))

        Returns new sequence.
        '''
        return type(self)(reversed(self))

    def rotate(self, index=None):
        '''Rotates sequence by `index`.

        ..  container:: example

            **Example 1.** Rotates `sequence` to the right:

            ::

                >>> Sequence(tuple(range(10))).rotate(4)
                Sequence((6, 7, 8, 9, 0, 1, 2, 3, 4, 5))

        ..  container:: example

            **Example 2.** Rotates `sequence` to the left:

            ::

                >>> Sequence(tuple(range(10))).rotate(-3)
                Sequence((3, 4, 5, 6, 7, 8, 9, 0, 1, 2))

        ..  container:: example

            **Example 3.** Rotates `sequence` neither to the right nor the
            left:

            ::

                >>> Sequence(tuple(range(10))).rotate(0)
                Sequence((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

        Returns new sequence.
        '''
        index = index or 0
        result = []
        if len(self):
            index = index % len(self)
            for item in self[-index:len(self)] + self[:-index]:
                result.append(item)
        return type(self)(result)

    def split(self, weights, cyclic=False, overhang=False):
        r'''Splits sequence by `weights`.

        ..  todo:: Port remaining examples from
            ``sequencetools.split_sequence()``.

        ..  container:: example

            **Example 1.** Splits sequence cyclically by weights with overhang:

            ::

                >>> sequence_ = Sequence((10, -10, 10, -10))
                >>> sequence_.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     )
                Sequence((Sequence((3,)), Sequence((7, -8)), Sequence((-2, 1)), Sequence((3,)), Sequence((6, -9)), Sequence((-1,))))

        Returns new sequence.
        '''
        from abjad.tools import sequencetools
        parts = sequencetools.split_sequence(
            self.items,
            weights,
            cyclic=cyclic,
            overhang=overhang,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(parts)

    def sum(self):
        '''Sums sequence.

        ..  container:: example

            **Example 1.** Sums sequence of positive numbers:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).sum()
                55

        ..  container:: example

            **Example 2.** Sum sequence of numbers with mixed signs:

            ::

                >>> Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]).sum()
                5

        Returns new sequence.
        '''
        return sum(self)

    ### PUBLIC PROPERTIES ###

    @property
    def degree_of_rotational_symmetry(self):
        '''Gets degree of rotational symmetry.

        ..  container:: example

            ::

                >>> Sequence((1, 1, 1, 1, 1, 1)).degree_of_rotational_symmetry
                6

            ::

                >>> Sequence((1, 2, 1, 2, 1, 2)).degree_of_rotational_symmetry
                3

            ::

                >>> Sequence((1, 2, 3, 1, 2, 3)).degree_of_rotational_symmetry
                2

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)).degree_of_rotational_symmetry
                1

            ::

                >>> Sequence().degree_of_rotational_symmetry
                1

        Returns positive integer.
        '''
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
        return degree_of_rotational_symmetry

    @property
    def items(self):
        r'''Gets sequence items.

        Returns tuple.
        '''
        return self._items

    @property
    def period_of_rotation(self):
        '''Gets period of rotation.

        ..  container:: example

            ::

                >>> Sequence((1, 2, 3, 4, 5, 6)).period_of_rotation
                6

            ::

                >>> Sequence((1, 2, 3, 1, 2, 3)).period_of_rotation
                3

            ::

                >>> Sequence((1, 2, 1, 2, 1, 2)).period_of_rotation
                2

            ::

                >>> Sequence((1, 1, 1, 1, 1, 1)).period_of_rotation
                1

            ::

                >>> Sequence().period_of_rotation
                0

        Defined equal to length of sequence divided by degree of rotational
        symmetry of sequence.

        Returns positive integer.
        '''
        return len(self) // self.degree_of_rotational_symmetry

collections.Sequence.register(Sequence)
