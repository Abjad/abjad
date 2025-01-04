import collections
import dataclasses
import typing


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class CyclicTuple:
    """
    Cyclic tuple.

    ..  container:: example

        Initializes from string:

        >>> tuple_ = abjad.CyclicTuple('abcd')

        >>> tuple_
        CyclicTuple(items=('a', 'b', 'c', 'd'))

        >>> for x in range(8):
        ...     print(x, tuple_[x])
        ...
        0 a
        1 b
        2 c
        3 d
        4 a
        5 b
        6 c
        7 d

    Cyclic tuples overload the item-getting method of built-in tuples.

    Cyclic tuples return a value for any integer index.

    Cyclic tuples otherwise behave exactly like built-in tuples.
    """

    items: typing.Sequence = ()

    def __post_init__(self):
        self.items = tuple(self.items)

    def __contains__(self, item) -> bool:
        """
        Is true when cyclic tuple contains ``item``.

        ..  container:: example

            >>> tuple_ = abjad.CyclicTuple('abcd')
            >>> 'a' in tuple_
            True

        """
        return self.items.__contains__(item)

    def __eq__(self, argument) -> bool:
        """
        Compares ``items``.
        """
        if isinstance(argument, tuple):
            return self.items == argument
        elif isinstance(argument, type(self)):
            return self.items == argument.items
        return False

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets slice open at right:

            >>> items = [0, 1, 2, 3, 4, 5]
            >>> tuple_ = abjad.CyclicTuple(items=items)
            >>> tuple_[2:]
            (2, 3, 4, 5)

        ..  container:: example

            Gets slice closed at right:

            >>> items = [0, 1, 2, 3, 4, 5]
            >>> tuple_ = abjad.CyclicTuple(items=items)
            >>> tuple_[:15]
            (0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2)

        Raises index error when ``argument`` can not be found in cyclic tuple.
        """
        if isinstance(argument, slice):
            if (argument.stop is not None and argument.stop < 0) or (
                argument.start is not None and argument.start < 0
            ):
                return self.items.__getitem__(argument)
            else:
                return self._get_slice(argument.start, argument.stop)
        if not self:
            raise IndexError(f"cyclic tuple is empty: {self!r}.")
        argument = argument % len(self)
        return self.items.__getitem__(argument)

    def __iter__(self) -> typing.Iterator:
        """
        Iterates cyclic tuple.

        Iterates items only once.

        Does not iterate infinitely.
        """
        return self.items.__iter__()

    def __len__(self) -> int:
        """
        Gets length of cyclic tuple.
        """
        assert isinstance(self.items, tuple | CyclicTuple), repr(self.items)
        return self.items.__len__()

    def _get_slice(self, start_index, stop_index):
        if stop_index is not None and 1000000 < stop_index:
            stop_index = len(self)
        result = []
        if start_index is None:
            start_index = 0
        if stop_index is None:
            indices = range(start_index, len(self))
        else:
            indices = range(start_index, stop_index)
        result = [self[n] for n in indices]
        return tuple(result)


collections.abc.Sequence.register(CyclicTuple)
