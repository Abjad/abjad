# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DivisionMaker(AbjadValueObject):
    r'''A division-maker.

    ..  container:: example

        **Example 1.** Makes divisions:

        ::

            >>> division_maker = makertools.DivisionMaker()
            >>> divisions = [(4, 8), (3, 8), (4, 8), (2, 8)]
            >>> division_maker(divisions)
            [(4, 8), (3, 8), (4, 8), (2, 8)]

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
        division_lists = divisions
        for callback in self.callbacks:
            divisions = sequencetools.flatten_sequence(division_lists)
            division_lists = callback(divisions)
        return division_lists

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