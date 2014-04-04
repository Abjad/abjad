# -*- encoding: utf-8 -*-
import random
from abjad.tools.abctools import AbjadObject


class Domain(AbjadObject):
    r'''A two-dimensional constraints search domain:

    ::

        >>> from experimental.tools.constrainttools import Domain

    May be instantiated from a non-empty sequence of non-empty sequences.

    ::

        >>> domain = Domain([(1, 2, 3), (4, 5, 6), (7, 8, 9)])

    May also be instantiated from one non-empty sequence and an integer
    greater than zero, indicating how many "columns" to create from the
    first sequence:

    ::

        >>> domain = Domain([1, 2, 3, 4], 5)

    ``Domains`` are immutable.

    Returns ``Domain`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ('_domain')

    ### INITIALIZER ###

    def __init__(self, *args):
        if 1 == len(args):
            assert 0 < len(args[0])
            assert all(len(x) for x in args[0])
            domain = tuple([tuple(x) for x in args[0]])
        elif 2 == len(args):
            assert 0 < len(args[0])
            assert len(args[0])
            assert 0 < int(args[1])
            domain = tuple([tuple(args[0]) for _ in range(args[1])])
        else:
            message = "can not instantiate %s from %s."
            raise Exception(message % (type(self).__name__, args))
        object.__setattr__(self, '_domain', domain)

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._domain[item]

    def __iter__(self):
        for x in self._domain:
            yield x

    def __len__(self):
        return len(self._domain)

    ### PUBLIC METHODS ###

    def randomized(self):
        r'''Create a new Domain containing the same values, but with every
        column randomly reordered:

        ::

            >>> original = Domain([1, 2, 3, 4], 4)
            >>> randomized = original.randomized()
            >>> randomized[0]  # doctest: +SKIP
            (4, 1, 2, 3) # doctest: +SKIP

        Returns Domain instance.
        '''
        new_domain = []
        for slice in self._domain:
            new_slice = list(slice)
            random.shuffle(new_slice)
            new_domain.append(tuple(new_slice))
        return type(self)(tuple(new_domain))