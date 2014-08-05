# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MeasurewiseDivisionMaker(AbjadValueObject):
    r'''Measurewise division-maker.

    Follows the two-step configure-once / call-repeatly pattern established
    in rhythm-makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_division_maker',
        '_hypermeasure_specifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        division_maker=None,
        hypermeasure_specifier=None,
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
    def division_maker(self):
        r'''Gets division-maker bundled in measurewise division-maker.

        Returns division-maker.
        '''
        return self._divisions

    @property
    def hypermeasure_specifier(self):
        r'''Gets hypermeasure specifier bundled in measurewise division-maker.

        Returns hypermeasure specifier or none.
        '''
        return self._hypermeasure_specifier