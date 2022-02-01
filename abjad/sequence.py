import collections.abc
import copy
import itertools
import math
import sys
import typing

import quicktions

from . import cyclictuple as _cyclictuple
from . import enums as _enums
from . import format as _format
from . import math as _math
from . import ratio as _ratio


class Sequence(collections.abc.Sequence):
    """
    Sequence.

    ..  container:: example

        Initializes sequence:

        ..  container:: example

            >>> abjad.Sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes and reverses sequence:

        ..  container:: example

            >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.reverse()
            Sequence([6, 5, 4, 3, 2, 1])

    ..  container:: example

        Initializes, reverses and flattens sequence:

        ..  container:: example

            >>> sequence = abjad.Sequence([1, 2, 3, [4, 5, [6]]])
            >>> sequence = sequence.reverse()
            >>> sequence = sequence.flatten(depth=-1)
            >>> sequence
            Sequence([4, 5, 6, 3, 2, 1])

    ..  container:: example

        REGRESSION:

        >>> abjad.Sequence(0)
        Sequence([0])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    ### INITIALIZER ###

    def __init__(self, items=None):
        if items is None:
            items = ()
        if not isinstance(items, collections.abc.Iterable):
            items = [items]
        self._items = tuple(items)

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> "Sequence":
        r"""
        Adds ``argument`` to sequence.

        ..  container:: example

            Adds tuple to sequence:

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]) + (4, 5, 6)
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds list to sequence:

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]) + [4, 5, 6]
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> sequence_1 = abjad.Sequence([1, 2, 3])
                >>> sequence_2 = abjad.Sequence([4, 5, 6])
                >>> sequence_1 + sequence_2
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Reverses result:

            ..  container:: example

                >>> sequence_1 = abjad.Sequence([1, 2, 3])
                >>> sequence_2 = abjad.Sequence([4, 5, 6])
                >>> sequence = sequence_1 + sequence_2
                >>> sequence.reverse()
                Sequence([6, 5, 4, 3, 2, 1])

        """
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items)

    def __eq__(self, argument) -> bool:
        """
        Compares ``items``.

        ..  container:: example

            Is true when ``argument`` is a sequence with items equal to those
            of this sequence:

            >>> abjad.Sequence([1, 2, 3, 4, 5, 6]) == abjad.Sequence([1, 2, 3, 4, 5, 6])
            True

        ..  container:: example

            Is false when ``argument`` is not a sequence with items equal to
            those of this sequence:

            >>> abjad.Sequence([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6])
            False

        """
        if isinstance(argument, type(self)):
            return self.items == argument.items
        return False

    def __getitem__(self, argument) -> typing.Any:
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets first item in sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[0]
                1

        ..  container:: example

            Gets last item in sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[-1]
                6

        ..  container:: example

            Gets slice from sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = sequence[:3]

                >>> sequence
                Sequence([1, 2, 3])

        ..  container:: example

            Gets item in sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = abjad.Sequence(sequence[0])

                >>> sequence
                Sequence([1])

        ..  container:: example

            Gets slice from sequence and flattens slice:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, [3, [4]], 5])
                >>> sequence = sequence[:-1]
                >>> sequence = sequence.flatten(depth=-1)

                >>> sequence
                Sequence([1, 2, 3, 4])

        Returns item or new sequence.
        """
        result = self._items.__getitem__(argument)
        if isinstance(argument, slice):
            return type(self)(result)
        return result

    def __hash__(self) -> int:
        """
        Hashes sequence.
        """
        return hash(self.__class__.__name__ + str(self))

    def __len__(self) -> int:
        """
        Gets length of sequence.

        ..  container:: example

            Gets length of sequence:

            >>> len(abjad.Sequence([1, 2, 3, 4, 5, 6]))
            6

        ..  container:: example

            Gets length of sequence:

            >>> len(abjad.Sequence('text'))
            4

        """
        return len(self._items)

    def __radd__(self, argument) -> "Sequence":
        r"""
        Adds sequence to ``argument``.

        ..  container:: example

            Adds sequence to tuple:

            ..  container:: example

                >>> (1, 2, 3) + abjad.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to list:

            ..  container:: example

                >>> [1, 2, 3] + abjad.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]) + abjad.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        """
        argument = type(self)(items=argument)
        items = argument.items + self.items
        return type(self)(items)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of sequence.

        ..  container:: example

            Gets interpreter representation:

            >>> abjad.Sequence([99])
            Sequence([99])

        ..  container:: example

            Gets interpreter representation:

            >>> abjad.Sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

        """
        items = ", ".join([repr(_) for _ in self.items])
        string = f"{type(self).__name__}([{items}])"
        return string

    ### PRIVATE METHODS ###

    # creates an iterator that can generate a flattened list,
    # descending down into child elements to a depth given in the arguments.
    # note that depth < 0 is effectively equivalent to infinity.
    @staticmethod
    def _flatten_helper(sequence, classes, depth):
        if not isinstance(sequence, classes):
            yield sequence
        elif depth == 0:
            for item in sequence:
                yield item
        else:
            for item in sequence:
                # flatten an iterable by one level
                depth_ = depth - 1
                for item_ in Sequence._flatten_helper(item, classes, depth_):
                    yield item_

    def _get_format_specification(self):
        return _format.FormatSpecification()

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_least(
        class_, sequence, weights, overhang=False
    ):
        l_copy = list(sequence)
        result = []
        current_part = []
        target_weight_index = 0
        len_weights = len(weights)
        while l_copy:
            target_weight = weights[target_weight_index % len_weights]
            item = l_copy.pop(0)
            current_part.append(item)
            if target_weight <= _math.weight(current_part):
                result.append(current_part)
                current_part = []
                target_weight_index += 1
        assert not l_copy
        if current_part:
            if overhang:
                result.append(current_part)
        # return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_most(
        class_, sequence, weights, overhang=False
    ):
        result = []
        current_part = []
        current_target_weight_index = 0
        current_target_weight = weights[current_target_weight_index]
        l_copy = list(sequence)
        while l_copy:
            current_target_weight = weights[current_target_weight_index % len(weights)]
            item = l_copy.pop(0)
            current_part_weight = _math.weight(current_part)
            candidate_part_weight = current_part_weight + _math.weight([item])
            if candidate_part_weight < current_target_weight:
                current_part.append(item)
            elif candidate_part_weight == current_target_weight:
                current_part.append(item)
                result.append(current_part)
                current_part = []
                current_target_weight_index += 1
            elif current_target_weight < candidate_part_weight:
                if current_part:
                    l_copy.insert(0, item)
                    result.append(current_part)
                    current_part = []
                    current_target_weight_index += 1
                else:
                    raise Exception("elements in sequence too big.")
            else:
                raise ValueError("candidate and target rates must compare.")
        if current_part:
            if overhang:
                result.append(current_part)
        # return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_least(
        class_, sequence, weights, overhang=False
    ):
        result = []
        current_part = []
        l_copy = list(sequence)
        for num_weight, target_weight in enumerate(weights):
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    if num_weight + 1 == len(weights):
                        if current_part:
                            result.append(current_part)
                            break
                    raise Exception("too few elements in sequence.")
                current_part.append(item)
                if target_weight <= _math.weight(current_part):
                    result.append(current_part)
                    current_part = []
                    break
        if l_copy:
            if overhang:
                result.append(l_copy)
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_most(
        class_, sequence, weights, overhang=False
    ):
        l_copy = list(sequence)
        result = []
        current_part = []
        for target_weight in weights:
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    raise Exception("too few elements in sequence.")
                current_weight = _math.weight(current_part)
                candidate_weight = current_weight + _math.weight([item])
                if candidate_weight < target_weight:
                    current_part.append(item)
                elif candidate_weight == target_weight:
                    current_part.append(item)
                    result.append(current_part)
                    current_part = []
                    break
                elif target_weight < candidate_weight:
                    if current_part:
                        result.append(current_part)
                        current_part = []
                        l_copy.insert(0, item)
                        break
                    else:
                        raise Exception("elements in sequence too big.")
                else:
                    raise ValueError("candidate and target weights must compare.")
        if overhang:
            left_over = current_part + l_copy
            if left_over:
                result.append(left_over)
        result = [class_(_) for _ in result]
        return class_(items=result)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple[typing.Any, ...]:
        """
        Gets sequence items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> abjad.Sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                >>> abjad.Sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

        """
        return self._items

    ### PUBLIC METHODS ###

    def filter(self, predicate=None) -> "Sequence":
        """
        Filters sequence by ``predicate``.

        ..  container:: example

            By length:

            ..  container:: example

                With lambda:

                >>> items = [[1], [2, 3, [4]], [5], [6, 7, [8]]]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.filter(lambda _: len(_) == 1)
                Sequence([[1], [5]])

            ..  container:: example

                With inequality:

                >>> items = [[1], [2, 3, [4]], [5], [6, 7, [8]]]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.filter(abjad.LengthInequality('==', 1))
                Sequence([[1], [5]])

        ..  container:: example

            By duration:

            ..  container:: example

                With inequality:

                >>> staff = abjad.Staff("c'4. d'8 e'4. f'8 g'2")
                >>> sequence = abjad.Sequence(staff)

                >>> sequence.filter(abjad.DurationInequality('==', (1, 8)))
                Sequence([Note("d'8"), Note("f'8")])

        """
        if predicate is None:
            return self[:]
        items = []
        for item in self:
            if predicate(item):
                items.append(item)
        return type(self)(items)

    def flatten(self, classes=None, depth=1) -> "Sequence":
        r"""
        Flattens sequence.

        ..  container:: example

            Flattens sequence:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.flatten()
                Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

        ..  container:: example

            Flattens sequence to depth 2:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.flatten(depth=2)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        ..  container:: example

            Flattens sequence to depth -1:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.flatten(depth=-1)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        ..  container:: example

            Flattens tuples in sequence only:

            ..  container:: example

                >>> items = ['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')]
                >>> sequence = abjad.Sequence(items)

                >>> sequence.flatten(classes=(tuple,))
                Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

        """
        if classes is None:
            classes = (collections.abc.Sequence,)
        if Sequence not in classes:
            classes = tuple(list(classes) + [Sequence])
        items = self._flatten_helper(self, classes, depth)
        return type(self)(items)

    def group_by(self, predicate=None) -> "Sequence":
        """
        Groups sequence items by value of items.

        ..  container:: example

            >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]
            >>> sequence = abjad.Sequence(items)
            >>> for item in sequence.group_by():
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1, 1])
            Sequence([5])
            Sequence([-5])

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' d' e' e' e'")
            >>> predicate = lambda x: abjad.PitchSet.from_selection(abjad.select(x))
            >>> for item in abjad.Sequence(staff).group_by(predicate):
            ...     item
            ...
            Sequence([Note("c'8")])
            Sequence([Note("d'8"), Note("d'8")])
            Sequence([Note("e'8"), Note("e'8"), Note("e'8")])

        Returns nested sequence.
        """
        items = []
        if predicate is None:
            pairs = itertools.groupby(self, lambda _: _)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        else:
            pairs = itertools.groupby(self, predicate)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        return type(self)(items)

    def is_decreasing(self, strict=True) -> bool:
        """
        Is true when sequence decreases.

        ..  container:: example

            Is true when sequence is strictly decreasing:

            >>> abjad.Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=True)
            True

            >>> abjad.Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=True)
            False

            >>> abjad.Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=True)
            False

            >>> abjad.Sequence().is_decreasing(strict=True)
            True

        ..  container:: example

            Is true when sequence decreases monotonically:

            >>> abjad.Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> abjad.Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> abjad.Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=False)
            True

            >>> abjad.Sequence().is_decreasing(strict=False)
            True

        """
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

    def is_increasing(self, strict=True) -> bool:
        """
        Is true when sequence increases.

        ..  container:: example

            Is true when sequence is strictly increasing:

            >>> abjad.Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=True)
            True

            >>> abjad.Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> abjad.Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> abjad.Sequence().is_increasing(strict=True)
            True

        ..  container:: example

            Is true when sequence increases monotonically:

            >>> abjad.Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=False)
            True

            >>> abjad.Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> abjad.Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> abjad.Sequence().is_increasing(strict=False)
            True

        """
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

    def is_permutation(self, length=None) -> bool:
        """
        Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            >>> abjad.Sequence([4, 5, 0, 3, 2, 1]).is_permutation()
            True

        ..  container:: example

            Is false when sequence is not a permutation:

            >>> abjad.Sequence([1, 1, 5, 3, 2, 1]).is_permutation()
            False

        """
        return tuple(sorted(self)) == tuple(range(len(self)))

    def is_repetition_free(self) -> bool:
        """
        Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence is repetition-free:

            >>> abjad.Sequence([0, 1, 2, 6, 7, 8]).is_repetition_free()
            True

        ..  container:: example

            Is true when sequence is empty:

            >>> abjad.Sequence().is_repetition_free()
            True

        ..  container:: example

            Is false when sequence contains repetitions:

            >>> abjad.Sequence([0, 1, 2, 2, 7, 8]).is_repetition_free()
            False

        """
        try:
            for left, right in self.nwise():
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def join(self) -> "Sequence":
        r"""
        Join subsequences in ``sequence``.

        ..  container:: example

            >>> items = [(1, 2, 3), (), (4, 5), (), (6,)]
            >>> sequence = abjad.Sequence(items)
            >>> sequence
            Sequence([(1, 2, 3), (), (4, 5), (), (6,)])

            >>> sequence.join()
            Sequence([(1, 2, 3, 4, 5, 6)])

        """
        if not self:
            return type(self)()
        item = self[0]
        for item_ in self[1:]:
            item += item_
        return type(self)([item])

    def map(self, operand=None) -> "Sequence":
        r"""
        Maps ``operand`` to sequence items.

        ..  container:: example

            Partitions sequence and sums parts:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(1, 10+1))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     )
                >>> sequence = sequence.map(sum)

                >>> sequence
                Sequence([6, 15, 24])

        ..  container:: example

            Maps identity:

            >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.map()
            Sequence([1, 2, 3, 4, 5, 6])

        """
        if operand is not None:
            items = []
            for i, item_ in enumerate(self):
                item_ = operand(item_)
                items.append(item_)
        else:
            items = list(self.items[:])
        return type(self)(items)

    def nwise(self, n=2, cyclic=False, wrapped=False) -> typing.Generator:
        """
        Iterates sequence ``n`` at a time.

        ..  container:: example

            Iterates iterable by pairs:

            >>> sequence = abjad.Sequence(range(10))
            >>> for item in sequence.nwise():
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])

        ..  container:: example

            Iterates iterable by triples:

            >>> sequence = abjad.Sequence(range(10))
            >>> for item in sequence.nwise(n=3):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])

        ..  container:: example

            Iterates iterable by pairs. Wraps around at end:

            >>> sequence = abjad.Sequence(range(10))
            >>> for item in sequence.nwise(n=2, wrapped=True):
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])

        ..  container:: example

            Iterates iterable by triples. Wraps around at end:

            >>> sequence = abjad.Sequence(range(10))
            >>> for item in sequence.nwise(n=3, wrapped=True):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])

        ..  container:: example

            Iterates iterable by pairs. Cycles indefinitely:

            >>> sequence = abjad.Sequence(range(10))
            >>> pairs = sequence.nwise(n=2, cyclic=True)
            >>> for _ in range(15):
            ...     next(pairs)
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])

            Returns infinite generator.

        ..  container:: example

            Iterates iterable by triples. Cycles indefinitely:

            >>> sequence = abjad.Sequence(range(10))
            >>> triples = sequence.nwise(n=3, cyclic=True)
            >>> for _ in range(15):
            ...     next(triples)
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])

            Returns infinite generator.

        ..  container:: example

            Iterates items one at a time:

            >>> sequence = abjad.Sequence(range(10))
            >>> for item in sequence.nwise(n=1):
            ...     item
            ...
            Sequence([0])
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5])
            Sequence([6])
            Sequence([7])
            Sequence([8])
            Sequence([9])

        Ignores ``wrapped`` when ``cyclic`` is true.
        """
        if cyclic:
            item_buffer = []
            long_enough = False
            for item in self:
                item_buffer.append(item)
                if not long_enough:
                    if n <= len(item_buffer):
                        long_enough = True
                if long_enough:
                    yield type(self)(item_buffer[-n:])
            len_sequence = len(item_buffer)
            current = len_sequence - n + 1
            while True:
                output = []
                for local_offset in range(n):
                    index = (current + local_offset) % len_sequence
                    output.append(item_buffer[index])
                yield type(self)(output)
                current += 1
                current %= len_sequence
        elif wrapped:
            first_n_minus_1: typing.List[typing.Any] = []
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)
                if len(first_n_minus_1) < n - 1:
                    first_n_minus_1.append(item)
            item_buffer = item_buffer + first_n_minus_1
            if item_buffer:
                for x in range(n - 1):
                    stop = x + n
                    yield type(self)(item_buffer[x:stop])
        else:
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        enchain=False,
        overhang=False,
        reversed_=False,
    ) -> "Sequence":
        r"""
        Partitions sequence by ``counts``.

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> sequence
                Sequence([Sequence([0, 1, 2])])

                >>> for part in sequence:
                ...     part
                Sequence([0, 1, 2])

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])
                Sequence([14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0])
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Partitions sequence once by counts and asserts that sequence
            partitions exactly (with no overhang):

            ..  container:: example

                >>> sequence = abjad.Sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 3, 5],
                ...     cyclic=False,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8, 9])

        ..  container:: example

            Partitions sequence cyclically by counts and asserts that sequence
            partitions exactly Exact partitioning means partitioning with no
            overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2],
                ...     cyclic=True,
                ...     overhang=abjad.Exact,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])
                Sequence([8, 9])

        ..  container:: example

            Partitions string:

            ..  container:: example

                >>> sequence = abjad.Sequence('some text')
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence(['s', 'o', 'm'])
                Sequence(['e', ' ', 't', 'e', 'x', 't'])

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            truncates overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            returns overhang at end:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])
                Sequence([13, 14, 15])

        ..  container:: example

            REGRESSION: partitions sequence cyclically into enchained parts by
            counts; does not return false 1-element part at end:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [5],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4])
                Sequence([4, 5, 6, 7, 8])
                Sequence([8, 9, 10, 11, 12])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Edge case: empty counts nests sequence and ignores keywords:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(16))
                >>> parts = sequence.partition_by_counts([])

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        Returns nested sequence.
        """
        if not all(isinstance(_, int) and 0 <= _ for _ in counts):
            raise Exception(f"must be nonnegative integers: {counts!r}.")
        sequence = self
        if reversed_:
            sequence = type(self)(reversed(sequence))
        if counts:
            counts = _cyclictuple.CyclicTuple(counts)
        else:
            return type(self)([sequence])
        result = []
        i, start = 0, 0
        while True:
            count = counts[i]
            stop = start + count
            part = sequence[start:stop]
            if len(sequence) < stop:
                if enchain and len(part) == 1:
                    part = None
                break
            result.append(part)
            start = stop
            i += 1
            if not cyclic and len(counts) <= i:
                part = sequence[start:]
                break
            if enchain:
                start -= 1
        if part:
            if overhang is True:
                result.append(part)
            elif overhang is _enums.Exact and len(part) == count:
                result.append(part)
            elif overhang is _enums.Exact and len(part) != count:
                raise Exception("sequence does not partition exactly.")
        if reversed_:
            result_ = []
            for part in reversed(result):
                part_type = type(part)
                part = reversed(part)
                part = part_type(part)
                result_.append(part)
            result = result_
        return type(self)(result)

    def partition_by_ratio_of_lengths(self, ratio) -> "Sequence":
        r"""
        Partitions sequence by ``ratio`` of lengths.

        ..  container:: example

            Partitions sequence by ``1:1:1`` ratio:

            ..  container:: example

                >>> numbers = abjad.Sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 1))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7, 8, 9])

        ..  container:: example

            Partitions sequence by ``1:1:2`` ratio:

            ..  container:: example

                >>> numbers = abjad.Sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 2))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4])
                Sequence([5, 6, 7, 8, 9])

        Returns nested sequence.
        """
        ratio = _ratio.Ratio(ratio)
        length = len(self)
        counts = ratio.partition_integer(length)
        parts = self.partition_by_counts(counts, cyclic=False, overhang=_enums.Exact)
        return type(self)(parts)

    def partition_by_ratio_of_weights(self, weights) -> "Sequence":
        """
        Partitions sequence by ratio of ``weights``.

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = abjad.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = abjad.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = abjad.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = abjad.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = abjad.Sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1, 2, 2])
            Sequence([2, 2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = abjad.Sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1])
            Sequence([2, 2, 2])
            Sequence([2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = abjad.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = abjad.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = abjad.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = abjad.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        Rounded weight-proportions of sequences returned equal to rounded
        ``weights``.

        Returns nested sequence.
        """
        list_weight = _math.weight(self)
        weights_parts = _ratio.Ratio(weights).partition_integer(list_weight)
        cumulative_weights = _math.cumulative_sums(weights_parts, start=None)
        items = []
        sublist: typing.List[typing.Any] = []
        items.append(sublist)
        current_cumulative_weight = cumulative_weights.pop(0)
        for item in self:
            if not isinstance(item, (int, float, quicktions.Fraction)):
                raise TypeError(f"must be number: {item!r}.")
            sublist.append(item)
            while current_cumulative_weight <= _math.weight(
                type(self)(items).flatten(depth=-1)
            ):
                try:
                    current_cumulative_weight = cumulative_weights.pop(0)
                    sublist = []
                    items.append(sublist)
                except IndexError:
                    break
        items_ = [type(self)(_) for _ in items]
        return type(self)(items_)

    def partition_by_weights(
        self,
        weights,
        # TODO: make keyword-only:
        cyclic=False,
        overhang=False,
        allow_part_weights=_enums.Exact,
    ) -> "Sequence":
        r"""
        Partitions sequence by ``weights`` exactly.

        >>> sequence = abjad.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence once by weights with overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])

        ..  container:: example

            Partitions sequence once by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])
            Sequence([4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence cyclically by weights:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])
            Sequence([4, 5])

        >>> sequence = abjad.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.Less,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        >>> sequence = abjad.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allow part weights to be just
            more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.More,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])
            Sequence([5])

        Returns nested sequence.
        """
        if allow_part_weights is _enums.Exact:
            candidate = type(self)(self)
            candidate = candidate.split(weights, cyclic=cyclic, overhang=overhang)
            flattened_candidate = candidate.flatten(depth=-1)
            if flattened_candidate == self[: len(flattened_candidate)]:
                return candidate
            else:
                raise Exception("can not partition exactly.")
        elif allow_part_weights is _enums.More:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_least(
                    self, weights, overhang=overhang
                )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_least(
                    self, weights, overhang=overhang
                )
        elif allow_part_weights is _enums.Less:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_most(
                    self, weights, overhang=overhang
                )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_most(
                    self, weights, overhang=overhang
                )
        else:
            message = "allow_part_weights must be ordinal constant: {!r}."
            message = message.format(allow_part_weights)
            raise ValueError(message)

    def permute(self, permutation) -> "Sequence":
        r"""
        Permutes sequence by ``permutation``.

        ..  container:: example

            >>> sequence = abjad.Sequence([10, 11, 12, 13, 14, 15])
            >>> sequence.permute([5, 4, 0, 1, 2, 3])
            Sequence([15, 14, 10, 11, 12, 13])

        ..  container:: example

            >>> sequence = abjad.Sequence([11, 12, 13, 14])
            >>> sequence.permute([1, 0, 3, 2])
            Sequence([12, 11, 14, 13])

        ..  container:: example

            Raises exception when lengths do not match:

            >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.permute([3, 0, 1, 2])
            Traceback (most recent call last):
                ...
            ValueError: permutation Sequence([3, 0, 1, 2]) must match length of Sequence([1, 2, 3, 4, 5, 6]).

        """
        permutation = type(self)(permutation)
        if not permutation.is_permutation():
            raise ValueError(f"must be permutation: {permutation!r}.")
        if len(permutation) != len(self):
            message = f"permutation {permutation!r} must match length of {self !r}."
            raise ValueError(message)
        result = []
        for i, item in enumerate(self):
            j = permutation[i]
            item_ = self[j]
            result.append(item_)
        return type(self)(result)

    # TODO: change input to pattern
    def remove(self, indices=None, period=None) -> "Sequence":
        """
        Removes items at ``indices``.

        ..  container:: example

            >>> sequence = abjad.Sequence(range(15))

        ..  container:: example

            >>> sequence.remove()
            Sequence([])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3])
            Sequence([0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes elements and indices -2 and -3:

            >>> sequence.remove(indices=[-2, -3])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3], period=4)
            Sequence([0, 1, 4, 5, 8, 9, 12, 13])

        ..  container:: example

            >>> sequence.remove(indices=[-2, -3], period=4)
            Sequence([2, 3, 6, 7, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            >>> sequence.remove(indices=[97, 98, 99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes no elements:

            >>> sequence.remove(indices=[-97, -98, -99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        """
        items = []
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        for i, item in enumerate(self):
            if i % period not in indices:
                items.append(item)
        return type(self)(items)

    def remove_repeats(self) -> "Sequence":
        """
        Removes repeats from ``sequence``.

        ..  container:: example

            >>> items = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequence = abjad.Sequence(items)
            >>> sequence.remove_repeats()
            Sequence([31, 35, 31, 35])

        """
        items = [self[0]]
        for item in self[1:]:
            if item != items[-1]:
                items.append(item)
        return type(self)(items)

    def repeat(self, n=1) -> "Sequence":
        r"""
        Repeats sequence.

        ..  container:: example

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]).repeat(n=0)
                Sequence([])

        ..  container:: example

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]).repeat(n=1)
                Sequence([Sequence([1, 2, 3])])

        ..  container:: example

            ..  container:: example

                >>> abjad.Sequence([1, 2, 3]).repeat(n=2)
                Sequence([Sequence([1, 2, 3]), Sequence([1, 2, 3])])

        Returns nested sequence.
        """
        items = []
        for i in range(n):
            items.append(self[:])
        return type(self)(items)

    def repeat_to_length(self, length=None, start=0) -> "Sequence":
        """
        Repeats sequence to ``length``.

        ..  container:: example

            Repeats list to length 11:

            >>> abjad.Sequence(range(5)).repeat_to_length(11)
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0])

        ..  container:: example

            >>> abjad.Sequence(range(5)).repeat_to_length(11, start=2)
            Sequence([2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2])

        ..  container:: example

            >>> sequence = abjad.Sequence([0, -1, -2, -3, -4])
            >>> sequence.repeat_to_length(11)
            Sequence([0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0])

        ..  container:: example

            >>> sequence.repeat_to_length(0)
            Sequence([])

        ..  container:: example

            >>> abjad.Sequence([1, 2, 3]).repeat_to_length(10, start=100)
            Sequence([2, 3, 1, 2, 3, 1, 2, 3, 1, 2])

        """
        assert _math.is_nonnegative_integer(length), repr(length)
        assert len(self), repr(self)
        items = []
        start %= len(self)
        stop_index = start + length
        repetitions = int(math.ceil(float(stop_index) / len(self)))
        for i in range(repetitions):
            for item in self:
                items.append(item)
        return type(self)(items[start:stop_index])

    def repeat_to_weight(self, weight, allow_total=_enums.Exact) -> "Sequence":
        """
        Repeats sequence to ``weight``.

        ..  container:: example

            Repeats sequence to weight of 23 exactly:

            >>> abjad.Sequence([5, -5, -5]).repeat_to_weight(23)
            Sequence([5, -5, -5, 5, -3])

        ..  container:: example

            Repeats sequence to weight of 23 more:

            >>> sequence = abjad.Sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.More)
            Sequence([5, -5, -5, 5, -5])

        ..  container:: example

            Repeats sequence to weight of 23 or less:

            >>> sequence = abjad.Sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.Less)
            Sequence([5, -5, -5, 5])

        ..  container:: example

            >>> items = [abjad.NonreducedFraction(3, 16)]
            >>> sequence = abjad.Sequence(items)
            >>> weight = abjad.NonreducedFraction(5, 4)
            >>> sequence = sequence.repeat_to_weight(weight)
            >>> sum(sequence)
            NonreducedFraction(20, 16)

            >>> [_.pair for _ in sequence]
            [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]

        """
        assert 0 <= weight
        if allow_total is _enums.Exact:
            sequence_weight = _math.weight(self)
            complete_repetitions = int(
                math.ceil(float(weight) / float(sequence_weight))
            )
            items = list(self)
            items = complete_repetitions * items
            overage = complete_repetitions * sequence_weight - weight
            for item in reversed(items):
                if 0 < overage:
                    element_weight = abs(item)
                    candidate_overage = overage - element_weight
                    if 0 <= candidate_overage:
                        overage = candidate_overage
                        items.pop()
                    else:
                        absolute_amount_to_keep = element_weight - overage
                        assert 0 < absolute_amount_to_keep
                        signed_amount_to_keep = absolute_amount_to_keep
                        signed_amount_to_keep *= _math.sign(item)
                        items.pop()
                        items.append(signed_amount_to_keep)
                        break
                else:
                    break
        elif allow_total is _enums.Less:
            items = [self[0]]
            i = 1
            while _math.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            if weight < _math.weight(items):
                items = items[:-1]
            return type(self)(items)
        elif allow_total is _enums.More:
            items = [self[0]]
            i = 1
            while _math.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            return type(self)(items)
        else:
            raise ValueError(f"is not an ordinal value constant: {allow_total!r}.")
        return type(self)(items=items)

    def replace(self, old, new) -> "Sequence":
        """
        Replaces ``old`` with ``new``.

        ..  container:: example

            >>> sequence = abjad.Sequence([0, 2, 3, 0, 2, 3, 0, 2, 3])
            >>> sequence.replace(0, 1)
            Sequence([1, 2, 3, 1, 2, 3, 1, 2, 3])

        """
        items = []
        for item in self:
            if item == old:
                new_copy = copy.copy(new)
                items.append(new_copy)
            else:
                items.append(item)
        return type(self)(items=items)

    def replace_at(self, indices, new_material) -> "Sequence":
        """
        Replaces items at ``indices`` with ``new_material``.

        ..  container:: example

            Replaces items at indices 0, 2, 4, 6:

            >>> sequence = abjad.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Replaces elements at indices 0, 1, 8, 13:

            >>> sequence = abjad.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0, 1, 8, 13], None),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15])

        ..  container:: example

            Replaces every item at even index:

            >>> sequence = abjad.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['*'], 1),
            ...     )
            Sequence(['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15])

        ..  container:: example

            Replaces every element at an index congruent to 0 (mod 6) with
            ``'A'``; replaces every element at an index congruent to 2 (mod 6)
            with ``'B'``:

            >>> sequence = abjad.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['A', 'B'], 3),
            ...     )
            Sequence(['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15])

        """
        assert isinstance(indices, collections.abc.Sequence)
        assert len(indices) == 2
        index_values, index_period = indices
        assert isinstance(index_values, collections.abc.Sequence)
        index_values = list(index_values)
        assert isinstance(index_period, (int, type(None)))
        assert isinstance(new_material, collections.abc.Sequence)
        assert len(new_material) == 2
        material_values, material_period = new_material
        assert isinstance(material_values, collections.abc.Sequence)
        material_values = list(material_values)
        assert isinstance(material_period, (int, type(None)))
        maxsize = sys.maxsize
        if index_period is None:
            index_period = maxsize
        if material_period is None:
            material_period = maxsize
        items = []
        material_index = 0
        for index, item in enumerate(self):
            if index % index_period in index_values:
                try:
                    cyclic_material_index = material_index % material_period
                    material_value = material_values[cyclic_material_index]
                    items.append(material_value)
                except IndexError:
                    items.append(item)
                material_index += 1
            else:
                items.append(item)
        return type(self)(items=items)

    # TODO: remove in favor of self.retain_pattern()
    def retain(self, indices=None, period=None) -> "Sequence":
        """
        Retains items at ``indices``.

        ..  container:: example

            >>> sequence = abjad.Sequence(range(10))
            >>> sequence.retain()
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3])
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3])
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3], period=4)
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3], period=4)
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[97, 98, 99])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[-97, -98, -99])
            Sequence([])

        """
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        items = []
        for i, item in enumerate(self):
            if i % period in indices:
                items.append(item)
        return type(self)(items=items)

    def retain_pattern(self, pattern) -> "Sequence":
        """
        Retains items at indices matching ``pattern``.

        ..  container:: example

            >>> sequence = abjad.Sequence(range(10))
            >>> sequence.retain_pattern(abjad.index_all())
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3]))
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3]))
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3], 4))
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3], 4))
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([97, 98, 99]))
            Sequence([])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-97, -98, -99]))
            Sequence([])

        """
        length = len(self)
        items = []
        for i, item in enumerate(self):
            if pattern.matches_index(i, length):
                items.append(item)
        return type(self)(items=items)

    def reverse(self, recurse=False) -> "Sequence":
        r"""
        Reverses sequence.

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence([[1, 2], 3, [4, 5]])

                >>> sequence.reverse()
                Sequence([[4, 5], 3, [1, 2]])

        ..  container:: example

            Reverses recursively:

            ..  container:: example

                >>> segment_1 = abjad.PitchClassSegment([1, 2])
                >>> pitch = abjad.NumberedPitch(3)
                >>> segment_2 = abjad.PitchClassSegment([4, 5])
                >>> sequence = abjad.Sequence([segment_1, pitch, segment_2])

                >>> for item in sequence.reverse(recurse=True):
                ...     item
                ...
                PitchClassSegment([5, 4])
                NumberedPitch(3)
                PitchClassSegment([2, 1])

        """
        if not recurse:
            return type(self)(items=reversed(self))

        def _reverse_helper(item):
            if isinstance(item, collections.abc.Iterable):
                subitems_ = [_reverse_helper(_) for _ in reversed(item)]
                return type(item)(subitems_)
            else:
                return item

        items = _reverse_helper(self.items)
        return type(self)(items=items)

    def rotate(self, n=0) -> "Sequence":
        r"""
        Rotates sequence by index ``n``.

        ..  container:: example

            Rotates sequence to the right:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(10))

                >>> sequence.rotate(n=4)
                Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

        ..  container:: example

            Rotates sequence to the left:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(10))

                >>> sequence.rotate(n=-3)
                Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

        ..  container:: example

            Rotates sequence neither to the right nor the left:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(10))

                >>> sequence.rotate(n=0)
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        """
        n = n or 0
        items = []
        if len(self):
            n = n % len(self)
            for item in self[-n : len(self)] + self[:-n]:
                items.append(item)
        return type(self)(items=items)

    def sort(self, key=None, reverse=False) -> "Sequence":
        """
        Sorts sequence.

        ..  container:: example

            >>> sequence = abjad.Sequence([3, 2, 5, 4, 1, 6])
            >>> sequence.sort()
            Sequence([1, 2, 3, 4, 5, 6])

            >>> sequence
            Sequence([3, 2, 5, 4, 1, 6])

        """
        items = list(self)
        items.sort(key=key, reverse=reverse)
        return type(self)(items=items)

    def split(self, weights, cyclic=False, overhang=False) -> "Sequence":
        r"""
        Splits sequence by ``weights``.

        ..  container:: example

            Splits sequence cyclically by weights with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence([10, -10, 10, -10])

                >>> for part in sequence.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     ):
                ...     part
                ...
                Sequence([3])
                Sequence([7, -8])
                Sequence([-2, 1])
                Sequence([3])
                Sequence([6, -9])
                Sequence([-1])

        ..  container:: example

            Splits sequence once by weights with overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])
            Sequence([9, -10])

        ..  container:: example

            Splits sequence once by weights without overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])

        ..  container:: example

            REGRESSION. Splits sequence of nonreduced fractions cyclically by
            weights with overhang:

            ..  container:: example

                >>> sequence = abjad.Sequence([
                ...     abjad.NonreducedFraction(20, 2),
                ...     abjad.NonreducedFraction(-20, 2),
                ...     abjad.NonreducedFraction(20, 2),
                ...     abjad.NonreducedFraction(-20, 2),
                ... ])

                >>> for part in sequence.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     ):
                ...     part
                ...
                Sequence([NonreducedFraction(6, 2)])
                Sequence([NonreducedFraction(14, 2), NonreducedFraction(-16, 2)])
                Sequence([NonreducedFraction(-4, 2), NonreducedFraction(2, 2)])
                Sequence([NonreducedFraction(6, 2)])
                Sequence([NonreducedFraction(12, 2), NonreducedFraction(-18, 2)])
                Sequence([NonreducedFraction(-2, 2)])

        """
        result = []
        current_index = 0
        current_piece: typing.List[typing.Any] = []
        if cyclic:
            weights = Sequence(weights).repeat_to_weight(
                _math.weight(self), allow_total=_enums.Less
            )
        for weight in weights:
            current_piece_weight = _math.weight(current_piece)
            while current_piece_weight < weight:
                current_piece.append(self[current_index])
                current_index += 1
                current_piece_weight = _math.weight(current_piece)
            if current_piece_weight == weight:
                current_piece_ = type(self)(current_piece)
                result.append(current_piece_)
                current_piece = []
            elif weight < current_piece_weight:
                overage = current_piece_weight - weight
                current_last_element = current_piece.pop(-1)
                needed = abs(current_last_element) - overage
                needed *= _math.sign(current_last_element)
                current_piece.append(needed)
                current_piece_ = type(self)(current_piece)
                result.append(current_piece_)
                overage *= _math.sign(current_last_element)
                current_piece = [overage]
        if overhang:
            last_piece = current_piece
            last_piece.extend(self[current_index:])
            if last_piece:
                last_piece_ = type(self)(last_piece)
                result.append(last_piece_)
        return type(self)(items=result)

    def sum(self) -> typing.Any:
        r"""
        Sums sequence.

        ..  container:: example

            Sums sequence of positive numbers:

            ..  container:: example

                >>> sequence = abjad.Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

                >>> sequence.sum()
                55

        ..  container:: example

            Sum sequence of numbers with mixed signs:

            ..  container:: example

                >>> sequence = abjad.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

                >>> sequence.sum()
                5

        ..  container:: example

            Sums sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = abjad.Sequence(range(1, 10+1))
                >>> result = sequence.sum()
                >>> sequence = abjad.Sequence(result)

                >>> sequence
                Sequence([55])

        """
        if len(self) == 0:
            return 0
        result = self[0]
        for item in self[1:]:
            result += item
        return result

    def sum_by_sign(self, sign=(-1, 0, 1)) -> "Sequence":
        """
        Sums consecutive sequence items by ``sign``.

        >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]
        >>> sequence = abjad.Sequence(items)

        ..  container:: example

            >>> sequence.sum_by_sign()
            Sequence([0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1])
            Sequence([0, 0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0])
            Sequence([0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[1])
            Sequence([0, 0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0])
            Sequence([0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 1])
            Sequence([0, 0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0, 1])
            Sequence([0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0, 1])
            Sequence([0, -2, 5, -5, 8, -11])

        Sumsn consecutive negative elements when ``-1`` in ``sign``.

        Sums consecutive zero-valued elements when ``0`` in ``sign``.

        Sums consecutive positive elements when ``1`` in ``sign``.
        """
        items = []
        generator = itertools.groupby(self, _math.sign)
        for current_sign, group in generator:
            if current_sign in sign:
                items.append(sum(group))
            else:
                for item in group:
                    items.append(item)
        return type(self)(items=items)

    def truncate(self, sum_=None, weight=None) -> "Sequence":
        """
        Truncates sequence.

        >>> sequence = abjad.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to weights ranging from 1 to 10:

            >>> for weight in range(1, 11):
            ...     result = sequence.truncate(weight=weight)
            ...     print(weight, result)
            ...
            1 Sequence([-1])
            2 Sequence([-1, 1])
            3 Sequence([-1, 2])
            4 Sequence([-1, 2, -1])
            5 Sequence([-1, 2, -2])
            6 Sequence([-1, 2, -3])
            7 Sequence([-1, 2, -3, 1])
            8 Sequence([-1, 2, -3, 2])
            9 Sequence([-1, 2, -3, 3])
            10 Sequence([-1, 2, -3, 4])

        ..  container:: example

            Truncates sequence to sums ranging from 1 to 10:

            >>> for sum_ in range(1, 11):
            ...     result = sequence.truncate(sum_=sum_)
            ...     print(sum_, result)
            ...
            1 Sequence([-1, 2])
            2 Sequence([-1, 2, -3, 4])
            3 Sequence([-1, 2, -3, 4, -5, 6])
            4 Sequence([-1, 2, -3, 4, -5, 6, -7, 8])
            5 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            6 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            7 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            8 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            9 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            10 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to zero weight:

            >>> sequence.truncate(weight=0)
            Sequence([])

        ..  container:: example

            Truncates sequence to zero sum:

            >>> sequence.truncate(sum_=0)
            Sequence([])

        Ignores ``sum`` when ``weight`` and ``sum`` are both set.

        Raises value error on negative ``sum``.
        """
        if weight is not None:
            assert 0 <= weight, repr(weight)
            items = []
            if 0 < weight:
                total = 0
                for item in self:
                    total += abs(item)
                    if total < weight:
                        items.append(item)
                    else:
                        sign = _math.sign(item)
                        trimmed_part = weight - _math.weight(items)
                        trimmed_part *= sign
                        items.append(trimmed_part)
                        break
        elif sum_ is not None:
            assert 0 <= sum_, repr(sum_)
            items = []
            if 0 < sum_:
                total = 0
                for item in self:
                    total += item
                    if total < sum_:
                        items.append(item)
                    else:
                        items.append(sum_ - sum(items))
                        break
        return type(self)(items=items)

    def weight(self) -> typing.Any:
        """
        Gets weight.

        ..  container:: example

            >>> abjad.Sequence([]).weight()
            0

            >>> abjad.Sequence([1]).weight()
            1

            >>> abjad.Sequence([1, 2, 3]).weight()
            6

            >>> abjad.Sequence([1, 2, -3]).weight()
            6

            >>> abjad.Sequence([-1, -2, -3]).weight()
            6

            >>> sequence = abjad.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            >>> sequence.weight()
            55

        ..  container:: example

            >>> abjad.Sequence([[1, -7, -7], [1, -8 -8]]).weight()
            32

        """
        weights = []
        for item in self:
            if hasattr(item, "weight"):
                weights.append(item.weight())
            elif isinstance(item, collections.abc.Iterable):
                item = Sequence(item)
                weights.append(item.weight())
            else:
                weights.append(abs(item))
        return sum(weights)

    def zip(self, cyclic=False, truncate=True) -> "Sequence":
        """
        Zips sequences in sequence.

        ..  container:: example

            Zips cyclically:

            >>> sequence = abjad.Sequence([[1, 2, 3], ['a', 'b']])
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([1, 'a'])
            Sequence([2, 'b'])
            Sequence([3, 'a'])

            >>> items = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
            >>> sequence = abjad.Sequence(items)
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([10, 20, 30])
            Sequence([11, 21, 31])
            Sequence([12, 20, 32])
            Sequence([10, 21, 33])

        ..  container:: example

            Zips without truncation:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> sequence = abjad.Sequence(items)
            >>> for item in sequence.zip(truncate=False):
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])
            Sequence([4])

        ..  container:: example

            Zips strictly:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> for item in abjad.Sequence(items).zip():
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])

        Returns nested sequence.
        """
        for item in self:
            if not isinstance(item, collections.abc.Iterable):
                raise Exception(f"must by iterable: {item!r}.")
        items: typing.List[typing.Any] = []
        if cyclic:
            if not min(len(_) for _ in self):
                return type(self)(items=items)
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    index = i % len(item)
                    element = item[index]
                    part.append(element)
                part_ = type(self)(items=part)
                items.append(part_)
        elif not truncate:
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    try:
                        part.append(item[i])
                    except IndexError:
                        pass
                part_ = type(self)(items=part)
                items.append(part_)
        elif truncate:
            for item in zip(*self):
                item = type(self)(items=item)
                items.append(item)
        return type(self)(items=items)
