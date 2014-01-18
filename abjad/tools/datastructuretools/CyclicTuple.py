# -*- encoding: utf-8 -*-
from abjad.tools import abctools


# TODO: remove multiple inheritance; hold a private _tuple instead
class CyclicTuple(abctools.AbjadObject, tuple):
    '''A cylic tuple.

    ::

        >>> cyclic_tuple = datastructuretools.CyclicTuple('abcd')

    ::

        >>> cyclic_tuple
        CyclicTuple(['a', 'b', 'c', 'd'])

    ::

        >>> for x in range(8):
        ...     print x, cyclic_tuple[x]
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
        i = i % len(self)
        return tuple.__getitem__(self, i)

    def __getslice__(self, start_index, stop_index):
        r'''Gets slice of items from `start_index` to `stop_index` in cyclic
        tuple.

        Returns tuple.
        '''
        result = []
        result = [self[n] for n in range(start_index, stop_index)]
        return tuple(result)

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
