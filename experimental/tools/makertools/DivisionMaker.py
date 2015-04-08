# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import new


class DivisionMaker(AbjadValueObject):
    r'''A division-maker.

    ..  container:: example

        **Example 1.** Makes divisions:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> divisions = [(4, 8), (3, 8), (4, 8), (2, 8)]
            >>> division_maker(divisions)
            [Division(4, 8), Division(3, 8), Division(4, 8), Division(2, 8)]

    Division-makers aggregate a sequence of callable classes which describe the
    process of making (fusing, splitting, partitioning) divisions (arbitrary
    units of musical time).

    Division-makers provide methods for configuring and making new selectors.

    Composers may chain division-makers together.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        callbacks=None,
        ):
        callbacks = callbacks or ()
        if callbacks:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Makes divisions from `divisions`.

        Returns a (possibly empty) list of division lists.
        '''
        divisions = [durationtools.Division(_) for _ in divisions]
        for callback in self.callbacks:
            divisions = callback(divisions)
        return divisions

    ### PRIVATE METHODS ###

    def _with_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = new(self)
        result._callbacks = callbacks
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets division-maker callbacks.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def fuse_by_counts(
        self,
        cyclic=True,
        counts=None,
        ):
        r'''Fuses divisions by `counts`.

        ..  container:: example

            **Example 1.** Makes divisions:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> divisions = [(4, 8), (3, 8), (4, 8), (2, 8)]
                >>> division_maker(divisions)
                [Division(4, 8), Division(3, 8), Division(4, 8), Division(2, 8)]

        ..  container:: example

            **Example 2.** Fuses divisions two at a time:

            ::

                >>> division_maker = makertools.DivisionMaker()
                >>> division_maker = division_maker.fuse_by_counts(
                ...     counts=[2],
                ...     )
                >>> divisions = [(4, 8), (3, 8), (4, 8), (2, 8)]
                >>> division_maker(divisions)
                [[Division(7, 8)], [Division(6, 8)]]

        '''
        from experimental.tools import makertools
        callback = makertools.FuseDivisionMaker(
            cyclic=cyclic,
            measure_counts=counts,
            )
        return self._with_callback(callback)