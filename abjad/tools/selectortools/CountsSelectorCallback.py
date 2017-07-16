# -*- coding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class CountsSelectorCallback(AbjadValueObject):
    r'''Counts selector callback.

    ::

        >>> import abjad

    ..  container:: example

        Initializes callback by hand:

        ::

            >>> callback = abjad.CountsSelectorCallback([3])
            >>> f(callback)
            abjad.CountsSelectorCallback(
                counts=abjad.CyclicTuple(
                    [3]
                    ),
                cyclic=True,
                fuse_overhang=False,
                nonempty=False,
                overhang=True,
                rotate=True,
                )

    ..  container:: example

        Selects components:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_leaf()
            >>> selector = selector.by_counts([3])
            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8 b'8 r8 c''8")
            >>> selector(staff)
            Selection([Selection([Note("c'8"), Rest('r8'), Note("d'8")])])

    ..  container:: example

        Selects objects:

        ::

            >>> selector = abjad.select()
            >>> selector = selector.by_counts([3])
            >>> numbers = [1, 'two', 'three', 4, -5, 'foo', 7.0, 8]
            >>> selector(numbers)
            Selection([Selection([1, 'two', 'three'])])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_counts',
        '_cyclic',
        '_fuse_overhang',
        '_overhang',
        '_rotate',
        '_nonempty',
        )

    _publish_storage_format = True

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

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        Returns tuple in which each item is a selection or component.
        '''
        assert isinstance(argument, collections.Iterable), repr(argument)
        if rotation is None:
            rotation = 0
        rotation = int(rotation)
        result = []
        counts = self.counts
        if self.rotate:
            counts = datastructuretools.Sequence(counts).rotate(n=-rotation)
            counts = datastructuretools.CyclicTuple(counts)
        for subexpr in argument:
            groups = datastructuretools.Sequence(subexpr).partition_by_counts(
                [abs(_) for _ in counts],
                cyclic=self.cyclic,
                overhang=self.overhang,
                )
            groups = list(groups)
            if self.overhang and self.fuse_overhang and 1 < len(groups):
                last_count = counts[(len(groups) - 1) % len(counts)]
                if len(groups[-1]) != last_count:
                    last_group = groups.pop()
                    groups[-1] += last_group
            subresult = []
            for i, group in enumerate(groups):
                try:
                    count = counts[i]
                except:
                    raise Exception(counts, i)
                if count < 0:
                    continue
                items = selectiontools.Selection(group)
                subresult.append(items)
            if self.nonempty and not subresult:
                group = selectiontools.Selection(groups[0])
                subresult.append(group)
            result.extend(subresult)
            if self.rotate:
                counts = datastructuretools.Sequence(counts).rotate(n=-1)
                counts = datastructuretools.CyclicTuple(counts)
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

        Returns true or false.
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

        Returns true or false.
        '''
        return self._nonempty

    @property
    def overhang(self):
        r'''Gets counts selector callback overhang flag.

        Returns true or false.
        '''
        return self._overhang

    @property
    def rotate(self):
        r'''Gets counts selector callback rotate flag.

        Returns true or false.
        '''
        return self._rotate
