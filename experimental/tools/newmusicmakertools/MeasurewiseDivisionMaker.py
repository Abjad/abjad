# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MeasurewiseDivisionMaker(AbjadValueObject):
    r'''Measurewise division-maker.

    Follows the two-step configure-the-call pattern implemented
    against all rhythm-makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_divisions',
        '_hypermeasure_counts',
        '_remainder_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        divisions=None,
        hypermeasure_counts=None,
        remainder_direction=Right,
        ):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, measures=()):
        r'''Calls measurewise division-maker.

        Returns list of nonreduced fractions.
        '''
        divisions = []
        return divisions

    ### PUBLIC PROPERTIES ###

    @property
    def divisions(self):
        r'''Gets divisions.

        Returns tuple or cylic tuple of nonreduced fractions.
        '''
        return self._divisions

    @property
    def hypermeasure_counts(self):
        r'''Gets hypermeasure counts.

        Returns possibly empty tuple or cyclic tuple of positive integers.
        '''
        return self._hypermeasure _counts

    @property
    def remainder_direction(self):
        r'''Gets direction of any remainder division.

        Returns left, right or none.
        '''
        return self._remainder_direction