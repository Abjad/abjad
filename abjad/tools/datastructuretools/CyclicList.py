# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class CyclicList(abctools.AbjadObject, list):
    '''A cyclic list.

    ::

        >>> cyclic_list = datastructuretools.CyclicList('abcd')

    ::

        >>> cyclic_list
        CyclicList(['a', 'b', 'c', 'd'])

    ::

        >>> for x in range(8):
        ...     print x, cyclic_list[x]
        ...
        0 a
        1 b
        2 c
        3 d
        4 a
        5 b
        6 c
        7 d

    Cyclic lists overload the item-getting method of built-in lists.

    Cyclic lists return a value for any integer index.

    Cyclic lists otherwise behave exactly like built-in lists.
    '''

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when `expr` has items equal to those of this cyclic list.
        Otherwise false.

        Returns boolean.
        '''
        return list.__eq__(self, expr)
    
    def __getitem__(self, i):
        r'''Gets `i` from cyclic list.

        Raise index error when `i` can not be found in cyclic list.

        Returns item.
        '''
        if len(self):
            i = i % len(self)
            return list.__getitem__(self, i)
        else:
            raise IndexError

    def __getslice__(self, start_index, stop_index):
        r'''Gets items in cyclic list from `start_index` to `stop_index`.

        Returns list.
        '''
        result = []
        result = [self[n] for n in range(start_index, stop_index)]
        return result

    def __str__(self):
        r'''String representation of cyclic list.

        Returns string.
        '''
        return '[{!s}]' % ', '.join([str(x) for x in self])

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
