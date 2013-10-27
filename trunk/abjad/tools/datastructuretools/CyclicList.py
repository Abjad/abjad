# -*- encoding: utf-8 -*-
class CyclicList(list):
    '''Abjad model of cyclic list:

    ::

        >>> cyclic_list = datastructuretools.CyclicList('abcd')

    ::

        >>> cyclic_list
        CyclicList([a, b, c, d])

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

    def __getitem__(self, expr):
        if len(self):
            return list.__getitem__(self, expr % len(self))
        else:
            raise IndexError

    def __getslice__(self, start_index, stop_index):
        result = []
        result = [self[n] for n in range(start_index, stop_index)]
        return result

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        return '[%s]' % ', '.join([str(x) for x in self])

    ### PRIVATE METHODS ###

    @property
    def _tools_package_name(self):
        module_path = self.__module__
        parts = module_path.split('.')
        for part in reversed(parts):
            if part.endswith('tools'):
                return part

    @property
    def _tools_package_qualified_indented_repr(self):
        return self._tools_package_qualified_repr

    @property
    def _tools_package_qualified_repr(self):
        return '{}.{}'.format(self._tools_package_name, repr(self))
