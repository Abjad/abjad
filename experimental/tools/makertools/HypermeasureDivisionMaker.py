# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class HypermeasureDivisionMaker(AbjadValueObject):
    r'''Hypermeasure division-maker.

    ..  container:: example

        ::

            >>> maker = makertools.HypermeasureDivisionMaker(
            ...     measure_counts=[2],
            ...     )

        ::

            >>> print(format(maker, 'storage'))
            makertools.HypermeasureDivisionMaker(
                measure_counts=[2],
                )

    Object model of a partially evaluated function that accepts a (possibly
    empty) list of divisions as input and returns a (possibly empty) nested 
    list of divisions as output (structured one output list per input
    division.)

    Treats input as time signatures. Glues input together into hypermeasures
    according to optional measure counts. Postprocesses resulting
    hypermeasures with optional secondary division maker.

    Follows the two-step configure-once / call-repeatly pattern established
    for the rhythm-makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cyclic',
        '_measure_counts',
        '_secondary_division_maker',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        cyclic=True,
        measure_counts=None,
        secondary_division_maker=None,
        ):
        from experimental import makertools
        assert isinstance(cyclic, bool), repr(cyclic)
        self._cyclic = cyclic
        measure_counts = measure_counts or ()
        if measure_counts == mathtools.Infinity:
            self._measure_counts = measure_counts
        else:
            assert mathtools.all_are_positive_integers(measure_counts)
            self._measure_counts = measure_counts
        if secondary_division_maker is not None:
            prototype = (makertools.DivisionMaker,)
            assert isinstance(secondary_division_maker, prototype)
        self._secondary_division_maker = secondary_division_maker

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls hypermeasure division-maker.

        ..  container:: example

            **Example 1.** Trivial hypermeasure division-maker.
            Returns nested list of output divisions with one output division 
            per list:

            ::

                >>> maker = makertools.HypermeasureDivisionMaker()

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]
                [Division(3, 8)]
                [Division(3, 8)]
                [Division(2, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]
                [Division(3, 8)]
                [Division(3, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]
                [Division(3, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 2.** Glues divisions together two at a time:

            ::

                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=None,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(6, 8)]
                [Division(5, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(6, 8)]
                [Division(3, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(6, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 3.** Glues divisions together two at a time. Fills
            resulting hypermeasure divisions with ``1/4`` divisions. Positions
            remainders to the right of each list of divisions:
            
            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder=Right,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            Example output:

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4), Division(1, 4), Division(1, 8)]

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 8)]
                [Division(1, 4)]

            ::

                >>> divisions = [(2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4), Division(1, 4), Division(1, 8)]

            ::

                >>> divisions = [(2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 4.** As above but with remainders at left of each
            list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(1, 4)],
                ...     remainder=Left,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            Example output:

            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(1, 4), Division(1, 4)]
                [Division(1, 8), Division(1, 4), Division(1, 4)]


            ::

                >>> divisions = [(2, 8), (3, 8), (2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(1, 4), Division(1, 4)]
                [Division(1, 4)]

            ::

                >>> divisions = [(2, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(1, 4), Division(1, 4)]

            ::

                >>> divisions = [(2, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 4)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 5.** Similiar to the two makers above. Glues divisions
            together two at a time. But then fills resulting hypermeasures with
            ``2/8`` divisions instead of ``1/4`` divisions. Remainders at right
            of each list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(2, 8)],
                ...     remainder=Right,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8)]
                [Division(2, 8), Division(1, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(1, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 6.** As above but with remainders at left of each
            list of divisions:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(2, 8)],
                ...     remainder=Left,
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=[2],
                ...     secondary_division_maker=divisions,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8)]
                [Division(1, 8), Division(2, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(1, 8), Division(2, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 7.** Glues all input divisions together:

            ::

                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=mathtools.Infinity,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(9, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(6, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(3, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        ..  container:: example

            **Example 8.** Glues all input divisions together and then divides
            into divisions of ``2/8`` with remainder at right of output
            division list:

            ::

                >>> divisions = makertools.DivisionMaker(
                ...     pattern=[(2, 8)],
                ...     )
                >>> maker = makertools.HypermeasureDivisionMaker(
                ...     measure_counts=mathtools.Infinity,
                ...     secondary_division_maker=divisions,
                ...     )

            Example output:

            ::

                >>> divisions = [(3, 8), (3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8), Division(2, 8), Division(1, 8)]

            ::

                >>> divisions = [(3, 8), (3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(2, 8), Division(2, 8)]

            ::

                >>> divisions = [(3, 8)]
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_
                [Division(2, 8), Division(1, 8)]

            ::

                >>> divisions = []
                >>> lists = maker(divisions)
                >>> for list_ in lists:
                ...     list_

        Returns nested list of divisions structured one list per hypermeasure.
        '''
        divisions = divisions or ()
        divisions = self._coerce_divisions(divisions)
        if not divisions:
            pass
        elif self.measure_counts == mathtools.Infinity:
            divisions = [sum(divisions)]
        elif self.measure_counts:
            parts = sequencetools.partition_sequence_by_counts(
                divisions,
                self.measure_counts,
                cyclic=self.cyclic,
                overhang=True,
                )
            divisions = [sum(_) for _ in parts]
        division_lists = []
        for division in divisions:
            if self.secondary_division_maker is not None:
                division_list = self.secondary_division_maker([division])[0]
            else:
                division_list = [division]
            division_list = [durationtools.Division(_) for _ in division_list]
            division_lists.append(division_list)
        return division_lists

    ### PRIVATE PROPERTIES ###
    
    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        keyword_argument_names = \
            manager.get_signature_keyword_argument_names(self)
        keyword_argument_names = list(keyword_argument_names)
        if self.cyclic == True:
            keyword_argument_names.remove('cyclic')
        if not self.measure_counts:
            keyword_argument_names.remove('measure_counts')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PRIVATE METHODS ###

    def _coerce_divisions(self, divisions):
        nonreduced_fractions = []
        for division in divisions:
            if hasattr(division, 'time_signature'):
                nonreduced_fraction = durationtools.Division(
                    division.time_signature.pair
                    )
            else:
                nonreduced_fraction = durationtools.Division(division)
            nonreduced_fractions.append(nonreduced_fraction)
        return nonreduced_fractions

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        r'''Is true when hypermeasure division maker should treat measure 
        counts cyclically. Otherwise false.

        Set to true or false.
        '''
        return self._cyclic

    @property
    def measure_counts(self):
        r'''Gets measure counts of hypermeasure division maker.

        Set to (possibly empty) list or tuple of positive integers.

        Or set to infinity.
        '''
        return self._measure_counts

    @property
    def secondary_division_maker(self):
        r'''Gets hypermeasure postprocessor of hypermeasure division-maker.

        Returns division-maker or none.
        '''
        return self._secondary_division_maker