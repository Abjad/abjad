# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class HypermeasureSpecifier(AbjadValueObject):
    r'''Hypermeasure specifier.

    ..  container:: example:

        ::

            >>> from experimental import makertools
            >>> counts = [1, 1, 1, 2]
            >>> specifier = makertools.HypermeasureSpecifier(counts)
            >>> specifier
            HypermeasureSpecifier(counts=(1, 1, 1, 2), cyclic=True)

    ..  container:: example

        Storage format works:

        ::

            >>> print(format(specifier, 'storage'))
            makertools.HypermeasureSpecifier(
                counts=(1, 1, 1, 2),
                cyclic=True,
                )

    Specifies way in which consecutive measures should be grouped
    into hypermeasures.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_cyclic',
        )

    ### INITIALIZER ###

    def __init__(self, counts=(), cyclic=True):
        counts = counts or ()
        counts = tuple(counts)
        assert mathtools.all_are_positive_integers(counts), repr(counts)
        self._counts = counts
        assert isinstance(cyclic, type(True)), repr(cyclic)
        self._cyclic = cyclic

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of hypermeasure specifier.

        ..  container:: example

            ::

                >>> specifier.counts
                (1, 1, 1, 2)

        Returns possibly empty tuple of positive integers.
        '''
        return self._counts

    @property
    def cyclic(self):
        r'''Is true when hypermeasure specifier should treat counts cyclically.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier.cyclic
                True

        Returns boolean.
        '''
        return self._cyclic