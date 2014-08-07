# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class HypermeasureDivisionMaker(AbjadValueObject):
    r'''Hypermeasure division-maker.

    ..  container:: example

        ::

            >>> hypermeasure_specifier = makertools.HypermeasureSpecifier(
            ...     counts=[2],
            ...     cyclic=True,
            ...     )
            >>> maker = makertools.HypermeasureDivisionMaker(
            ...     hypermeasure_specifier=hypermeasure_specifier,
            ...     )

        ::

            >>> print(format(maker, 'storage'))
            makertools.HypermeasureDivisionMaker(
                hypermeasure_specifier=makertools.HypermeasureSpecifier(
                    counts=(2,),
                    cyclic=True,
                    ),
                )

    Object model of a partially evaluated function that accepts divisions as
    input and returns a nested list of divisions as output.

    Treats input as time signatures. Glues input together into hypermeasures
    according to optional hypermeasure specifier. Postprocesses resulting
    hypermeasures with optional hypermeasure postprocessor.

    Follows the two-step configure-once / call-repeatly pattern established
    by the rhythm-makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_hypermeasure_postprocessor',
        '_hypermeasure_specifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        hypermeasure_postprocessor=None,
        hypermeasure_specifier=None,
        ):
        from experimental import makertools
        if hypermeasure_postprocessor is not None:
            prototype = (makertools.DivisionMaker,)
            assert isinstance(hypermeasure_postprocessor, prototype)
        self._hypermeasure_postprocessor = hypermeasure_postprocessor
        if hypermeasure_specifier is not None:
            prototype = (makertools.HypermeasureSpecifier,)
            assert isinstance(hypermeasure_specifier, prototype)
        self._hypermeasure_specifier = hypermeasure_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls hypermeasure division-maker.

        ..  container:: example

            **Example 1.** Glues divisions together two at a time:

            ::

                >>> hypermeasures = makertools.HypermeasureSpecifier(
                ...     counts=[2],
                ...     cyclic=True,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=None,
                ...     hypermeasure_specifier=hypermeasures,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(6, 8)]
                [NonreducedFraction(5, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(6, 8)]
                [NonreducedFraction(3, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(6, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 2.** Glues divisions together two at a time. Fills
            resulting hypermeasure divisions with ``1/4`` divisions. Positions
            remainders to the right of each list of divisions:
            
            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder=Right,
                ...     )
                >>> hypermeasures = makertools.HypermeasureSpecifier(
                ...     counts=[2],
                ...     cyclic=True,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=divisions,
                ...     hypermeasure_specifier=hypermeasures,
                ...     )

            Example output:

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
                [NonreducedFraction(1, 4)]

            ::

                >>> divisions = [(2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4), NonreducedFraction(1, 4), NonreducedFraction(1, 8)]

            ::

                >>> divisions = [(2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 3.** As above but with remainders at left of each
            list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     )
                >>> hypermeasures = makertools.HypermeasureSpecifier(
                ...     counts=[2],
                ...     cyclic=True,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=divisions,
                ...     hypermeasure_specifier=hypermeasures,
                ...     )

            Example output:

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]


            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]
                [NonreducedFraction(1, 4)]

            ::

                >>> divisions = [(2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(1, 4), NonreducedFraction(1, 4)]

            ::

                >>> divisions = [(2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 4)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 4.** Similiar to the two makers above. Glues divisions
            together two at a time. But then fills resulting hypermeasures with
            ``2/8`` divisions instead of ``1/4`` divisions. Remainders at right
            of each list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(2, 8)],
                ...     remainder=Right,
                ...     )
                >>> hypermeasures = makertools.HypermeasureSpecifier(
                ...     counts=[2],
                ...     cyclic=True,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=divisions,
                ...     hypermeasure_specifier=hypermeasures,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(2, 8)]
                [NonreducedFraction(2, 8), NonreducedFraction(1, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(2, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(2, 8), NonreducedFraction(1, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 5.** As above but with remainders at left of each
            list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(2, 8)],
                ...     remainder=Left,
                ...     )
                >>> hypermeasures = makertools.HypermeasureSpecifier(
                ...     counts=[2],
                ...     cyclic=True,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=divisions,
                ...     hypermeasure_specifier=hypermeasures,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(2, 8)]
                [NonreducedFraction(1, 8), NonreducedFraction(2, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(2, 8), NonreducedFraction(2, 8), NonreducedFraction(2, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(1, 8), NonreducedFraction(2, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 6.** Trivial hypermeasure division-maker.
            Returns nested list of divisions with one division per list:

            ::

                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     hypermeasure_postprocessor=None,
                ...     hypermeasure_specifier=None,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(2, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(3, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8)]
                [NonreducedFraction(3, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [NonreducedFraction(3, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        Returns nested list of divisions structued one list per hypermeasure.
        '''
        divisions = divisions or ()
        divisions = self._coerce_divisions(divisions)
        if self.hypermeasure_specifier is not None:
            parts = sequencetools.partition_sequence_by_counts(
                divisions,
                self.hypermeasure_specifier.counts,
                cyclic=self.hypermeasure_specifier.cyclic,
                overhang=True,
                )
            divisions = [sum(_) for _ in parts]
        division_lists = []
        for division in divisions:
            if self.hypermeasure_postprocessor is not None:
                division_list = self.hypermeasure_postprocessor(division)
            else:
                division_list = [division]
            division_lists.append(division_list)
        return division_lists

    ### PRIVATE METHODS ###

    def _coerce_divisions(self, divisions):
        nonreduced_fractions = []
        for division in divisions:
            if hasattr(division, 'time_signature'):
                nonreduced_fraction = mathtools.NonreducedFraction(
                    division.time_signature.pair
                    )
            else:
                nonreduced_fraction = mathtools.NonreducedFraction(division)
            nonreduced_fractions.append(nonreduced_fraction)
        return nonreduced_fractions

    ### PUBLIC PROPERTIES ###

    @property
    def hypermeasure_postprocessor(self):
        r'''Gets hypermeasure postprocessor of hypermeasure division-maker.

        Returns division-maker or none.
        '''
        return self._hypermeasure_postprocessor

    @property
    def hypermeasure_specifier(self):
        r'''Gets hypermeasure specifier of hypermeasure division-maker.

        Returns hypermeasure specifier or none.
        '''
        return self._hypermeasure_specifier