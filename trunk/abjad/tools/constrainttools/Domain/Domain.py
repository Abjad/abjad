import random
from abjad.tools.abctools import AbjadObject


class Domain(AbjadObject):
    '''A two-dimensional constraints search domain:

    ::

        abjad> from abjad.tools.constrainttools import Domain
    
    May be instantiated from a non-empty sequence of non-empty sequences.

    ::

        abjad> domain = Domain([(1, 2, 3), (4, 5, 6), (7, 8, 9)])

    May also be instantiated from one non-empty sequence and an integer greater
    than zero, indicating how many "columns" to create from the first sequence:

    ::

        abjad> domain = Domain([1, 2, 3, 4], 5)
    
    ``Domains`` are immutable.

    Returns ``Domain`` instance.
    '''

    __slots__ = ('_domain')

    def __init__(self, *args):
        if 1 == len(args):
            assert 0 < len(args[0])
            assert all([len(x) for x in args[0]])
            domain = tuple([tuple(x) for x in args[0]])
        elif 2 == len(args):
            assert 0 < len(args[0])
            assert len(args[0])
            assert 0 < int(args[1])
            domain = tuple([tuple(args[0]) for _ in range(args[1])])
        else:
            raise Exception("Cannot instantiate %s from %s." % (type(self).__name__, args))
        object.__setattr__(self, '_domain', domain)

    ### OVERRIDES ###

    def __getitem__(self, item):
        return self._domain[item]

    def __iter__(self):
        for x in self._domain:
            yield x

    def __len__(self):
        return len(self._domain)

    ### PUBLIC METHODS ###

    def randomized(self):
        '''Create a new Domain containing the same values, but with every 
        column randomly reordered:

        ::

            abjad> original = Domain([1, 2, 3, 4], 4)
            abjad> randomized = original.randomized( )
            abjad> randomized[0]  # doctest: +SKIP
            (4, 1, 2, 3) # doctest: +SKIP

        Returns Domain instance.
        '''
        new_domain = [ ]
        for slice in self._domain:
            new_slice = list(slice)
            random.shuffle(new_slice)
            new_domain.append(tuple(new_slice))
        return type(self)(tuple(new_domain))
