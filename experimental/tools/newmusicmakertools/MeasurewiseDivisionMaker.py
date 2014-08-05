# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MeasurewiseDivisionMaker(AbjadValueObject):
    r'''Measurewise division-maker.

    ..  container:: example

        ::

            >>> division_maker = newmusicmakertools.DivisionMaker(
            ...     pattern=[(1, 4)],
            ...     )
            >>> hypermeasure_specifier = newmusicmakertools.HypermeasureSpecifier(
            ...     counts=[2],
            ...     cyclic=True,
            ...     )
            >>> maker = newmusicmakertools.MeasurewiseDivisionMaker(
            ...     division_maker=division_maker,
            ...     hypermeasure_specifier=hypermeasure_specifier,
            ...     )

        ::

            >>> print(format(maker, 'storage'))
            newmusicmakertools.MeasurewiseDivisionMaker(
                division_maker=newmusicmakertools.DivisionMaker(
                    cyclic=True,
                    pattern=(
                        mathtools.NonreducedFraction(1, 4),
                        ),
                    remainder=Right,
                    ),
                hypermeasure_specifier=newmusicmakertools.HypermeasureSpecifier(
                    counts=(2,),
                    cyclic=True,
                    ),
                )

    Object model of a partially evaluated function that accepts measures (or
    time signatures) as input and returns nonreduced fractions as output.

    Follows the two-step configure-once / call-repeatly pattern established
    in the rhythm-makers.
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
        self._division_maker = division_maker
        self._hypermeasure_specifier = hypermeasure_specifier

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
        return self._division_maker

    @property
    def hypermeasure_specifier(self):
        r'''Gets hypermeasure specifier bundled in measurewise division-maker.

        Returns hypermeasure specifier or none.
        '''
        return self._hypermeasure_specifier