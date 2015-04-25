# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: remove multiple inheritance; hold a private _tuple instead
class CyclicTuple(AbjadObject, tuple):
    '''A cylic tuple.

    ..  container:: example

        **Example 1.** Initializes from string:

        ::

            >>> cyclic_tuple = datastructuretools.CyclicTuple('abcd')

        ::

            >>> cyclic_tuple
            CyclicTuple(['a', 'b', 'c', 'd'])

        ::

            >>> for x in range(8):
            ...     print(x, cyclic_tuple[x])
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
    '''

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a tuple with items equal to those of this
        cyclic tuple. Otherwise false.

        Returns boolean.
        '''
        return tuple.__eq__(self, expr)

    def __getitem__(self, i):
        r'''Gets `i` from cyclic tuple.

        Raises index error when `i` can not be found in cyclic tuple.

        Returns item.
        '''
        if isinstance(i, slice):
            return self.__getslice__(i.start, i.stop)
        if not self:
            raise IndexError
        i = i % len(self)
        return tuple.__getitem__(self, i)

    def __getslice__(self, start_index, stop_index):
        r'''Gets slice of items from `start_index` to `stop_index` in cyclic
        tuple.

        ..  container:: example

            Gets slice open at right:

            ::

                >>> sequence = [0, 1, 2, 3, 4, 5]
                >>> sequence = datastructuretools.CyclicTuple(sequence)
                >>> sequence[2:]
                (2, 3, 4, 5)

        ..  container:: example

            Gets slice closed at right:

            ::

                >>> sequence = [0, 1, 2, 3, 4, 5]
                >>> sequence = datastructuretools.CyclicTuple(sequence)
                >>> sequence[:15]
                (0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 1, 2)

        Returns tuple.
        '''
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

    def __hash__(self):
        r'''Hashes cyclic tuple.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(CyclicTuple, self).__hash__()

    def __str__(self):
        r'''String representation of cyclic tuple.

        Returns string.
        '''
        if self:
            contents = [str(x) for x in self]
            contents = ', '.join(contents)
            string = '[{!s}]'.format(contents)
            return string
        return '()'

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                list(self),
                ),
            )