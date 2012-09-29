from abjad.tools import durationtools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    SymbolicTimespan inventory::

        >>> timespan_inventory = timetools.TimespanInventory()

    ::

        >>> timespan_inventory.append(durationtools.TimespanConstant(0, 3))
        >>> timespan_inventory.append(durationtools.TimespanConstant(3, 6))
        >>> timespan_inventory.append(durationtools.TimespanConstant(6, 10))

    ::

        >>> z(timespan_inventory)
        timetools.TimespanInventory([
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(3, 1)
                ),
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(3, 1),
                stop_offset=durationtools.Offset(6, 1)
                ),
            durationtools.TimespanConstant(
                start_offset=durationtools.Offset(6, 1),
                stop_offset=durationtools.Offset(10, 1)
                )
            ])

    SymbolicTimespan inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ObjectInventory.__init__(self, *args, **kwargs)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        '''True when all elements in inventory are time-contiguous.
        Also true when inventory is empty.
        Otherwise false.

        .. note:: add example.

        Return boolean.
        '''
        if len(self) <= 1:
            return True
        last_stop_offset = self[0].stop_offset
        for timespan in self[1:]:
            if timespan.start_offset != last_stop_offset:
                return False
            last_stop_offset = timespan.stop_offset
        return True

    ### PUBLIC METHODS ###

    def delete_timespans_between(self, start_offset, stop_offset):
        from experimental import timetools
        timespan_2 = durationtools.TimespanConstant(start_offset, stop_offset)
        for timespan_1 in self[:]:
            if timetools.timespan_2_curtails_timespan_1(timespan_1, timespan_2):
                timespan_1.trim_to_stop_offset(timespan_2.start_offset)
            elif timetools.timespan_2_delays_timespan_1(timespan_1, timespan_2):
                timespan_1.trim_to_start_offset(timespan_2.stop_offset)
            elif timetools.timespan_2_contains_timespan_1_improperly(timespan_1, timespan_2):
                self.remove(timespan_1)

    def get_timespan_that_satisfies_inequality(self, timespan_inequality):
        r'''Get timespan that satisifies `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 5))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.get_timespan_that_satisfies_inequality(timespan_inequality)
            TimespanConstant(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Return timespan when timespan inventory contains exactly one timespan
        that satisfies `timespan_inequality`.

        Raise exception when timespan inventory contains no timespan
        that satisfies `timespan_inequality`.

        Raise exception when timespan inventory contains more than one timespan
        that satisfies `timespan_inequality`.
        '''
        timespans = self.get_timespans_that_satisfy_inequality(timespan_inequality)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception('extra timespan error.')
        else:
            raise Exception('missing timespan error.')

    def get_timespans_that_satisfy_inequality(self, timespan_inequality):
        r'''Get timespans that satisfy `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 8))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespans = timespan_inventory.get_timespans_that_satisfy_inequality(timespan_inequality)

        ::

            >>> for timespan in timespans:
            ...     timespan
            TimespanConstant(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))
            TimespanConstant(start_offset=Offset(6, 1), stop_offset=Offset(10, 1))

        Return list of ``0`` or more timespans.
        '''
        from experimental import timetools
        result = []
        for timespan in self:
            if isinstance(timespan_inequality, timetools.TimespanInequality):
                if timespan_inequality(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(timespan_inequality, timetools.TimepointInequality):
                if timespan_inequality(timespan=timespan):
                    result.append(timespan)
            else:
                raise ValueError
        return result

    def has_timespan_that_satisfies_inequality(self, timespan_inequality):
        r'''True when timespan inventory has timespan that satisfies `timespan_inequality`::

            >>> timespan_1 = timetools.expr_to_timespan((2, 8))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_inequality(timespan_inequality)
            True

        Otherwise false::

            >>> timespan_1 = timetools.expr_to_timespan((10, 20))
            >>> timespan_inequality = timetools.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan_1)

        ::

            >>> timespan_inventory.has_timespan_that_satisfies_inequality(timespan_inequality)
            False

        Return boolean.
        '''
        return bool(self.get_timespans_that_satisfy_inequality(timespan_inequality))
