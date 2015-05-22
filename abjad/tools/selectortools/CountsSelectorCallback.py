# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools import datastructuretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class CountsSelectorCallback(AbjadValueObject):
    r'''A counts selector callback.

    ::

        >>> callback = selectortools.CountsSelectorCallback([3])
        >>> print(format(callback))
        selectortools.CountsSelectorCallback(
            counts=datastructuretools.CyclicTuple(
                [3]
                ),
            cyclic=True,
            fuse_overhang=False,
            nonempty=False,
            overhang=True,
            rotate=True,
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_cyclic',
        '_fuse_overhang',
        '_overhang',
        '_rotate',
        '_nonempty',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=(3,),
        cyclic=True,
        fuse_overhang=False,
        nonempty=False,
        overhang=True,
        rotate=True,
        ):
        counts = datastructuretools.CyclicTuple(int(_) for _ in counts)
        self._counts = counts
        self._cyclic = bool(cyclic)
        self._fuse_overhang = bool(fuse_overhang)
        self._overhang = bool(overhang)
        self._rotate = bool(rotate)
        self._nonempty = bool(nonempty)

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple in which each item is a selection or component.
        '''
        assert isinstance(expr, tuple), repr(tuple)
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        result = []
        counts = self.counts
        if self.rotate:
            counts = sequencetools.rotate_sequence(counts, -rotation)
        for subexpr in expr:
            groups = sequencetools.partition_sequence_by_counts(
                subexpr,
                [abs(_) for _ in counts],
                cyclic=self.cyclic,
                overhang=self.overhang,
                )
            if self.overhang and self.fuse_overhang and 1 < len(groups):
                last_count = counts[(len(groups) - 1) % len(counts)]
                if len(groups[-1]) != last_count:
                    last_group = groups.pop()
                    groups[-1] += last_group
            subresult = []
            for i, group in enumerate(groups):
                count = counts[i]
                if count < 0:
                    continue
                items = selectiontools.Selection(group)
                subresult.append(items)
            if self.nonempty and not subresult:
                group = selectiontools.Selection(groups[0])
                subresult.append(group)
            result.extend(subresult)
            if self.rotate:
                counts = sequencetools.rotate_sequence(counts, -1)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts selector callback counts.

        Returns tuple.
        '''
        return self._counts

    @property
    def cyclic(self):
        r'''Gets counts selector callback cyclicity.

        Returns boolean.
        '''
        return self._cyclic

    @property
    def fuse_overhang(self):
        r'''Gets counts selector callback fuse overhang flag.

        Returns ordinal constant.
        '''
        return self._fuse_overhang

    @property
    def nonempty(self):
        r'''Gets counts selector callback nonempty flag.

        Returns boolean.
        '''
        return self._nonempty

    @property
    def overhang(self):
        r'''Gets counts selector callback overhang flag.

        Returns boolean.
        '''
        return self._overhang

    @property
    def rotate(self):
        r'''Gets counts selector callback rotate flag.

        Returns boolean.
        '''
        return self._rotate