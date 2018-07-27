import copy
from abjad import enums
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.utilities import Infinity
from abjad.utilities import NegativeInfinity


class Timespan(AbjadValueObject):
    """
    Timespan.

    ..  container:: example

        >>> timespan_1 = abjad.Timespan(0, 10)
        >>> timespan_2 = abjad.Timespan(5, 12)
        >>> timespan_3 = abjad.Timespan(-2, 2)
        >>> timespan_4 = abjad.Timespan(10, 20)

    Timespans are closed-open intervals.

    Timespans are immutable.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Timespans'

    __slots__ = (
        '_start_offset',
        '_stop_offset',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, start_offset=NegativeInfinity, stop_offset=Infinity):
        if start_offset is None:
            start_offset = NegativeInfinity
        if stop_offset is None:
            stop_offset = Infinity
        start_offset = self._initialize_offset(start_offset)
        stop_offset = self._initialize_offset(stop_offset)
        assert start_offset <= stop_offset, repr((start_offset, stop_offset))
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __and__(self, argument):
        """
        Logical AND of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> timespan_1 & timespan_2
            TimespanList([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(10, 1))])

            >>> timespan_1 & timespan_3
            TimespanList([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))])

            >>> timespan_1 & timespan_4
            TimespanList([])

            >>> timespan_2 & timespan_3
            TimespanList([])

            >>> timespan_2 & timespan_4
            TimespanList([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(12, 1))])

            >>> timespan_3 & timespan_4
            TimespanList([])

        Returns timespan list.
        """
        import abjad
        argument = self._get_timespan(argument)
        if not self.intersects_timespan(argument):
            return abjad.TimespanList()
        new_start_offset = max(self._start_offset, argument.start_offset)
        new_stop_offset = min(self._stop_offset, argument.stop_offset)
        timespan = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return abjad.TimespanList([timespan])

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a timespan with equal offsets.

        ..  container:: example

            >>> abjad.Timespan(1, 3) == abjad.Timespan(1, 3)
            True

            >>> abjad.Timespan(1, 3) == abjad.Timespan(2, 3)
            False

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats timespan.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)
            >>> abjad.f(timespan)
            abjad.Timespan(
                start_offset=abjad.Offset(0, 1),
                stop_offset=abjad.Offset(10, 1),
                )

        Returns string.
        """
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __ge__(self, argument):
        """
        Is true when ``argument`` start offset is greater or equal
        to timespan start offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 >= timespan_3
            True

            >>> timespan_1 >= timespan_2
            False

        Returns true or false.
        """
        expr_start_offset, expr_stop_offset = \
            self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self._start_offset >= expr_start_offset:
                return True
            elif (self._start_offset == expr_start_offset and
                self._stop_offset >= expr_stop_offset):
                return True
            return False
        return self._start_offset >= expr_start_offset

    def __gt__(self, argument):
        """
        Is true when ``argument`` start offset is greater than
        timespan start offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 > timespan_3
            True

            >>> timespan_1 > timespan_2
            False

        Returns true or false.
        """
        expr_start_offset, expr_stop_offset = \
            self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self._start_offset > expr_start_offset:
                return True
            elif (self._start_offset == expr_start_offset and
                self._stop_offset > expr_stop_offset):
                return True
            return False
        return self._start_offset > expr_start_offset

    def __hash__(self):
        """
        Hashes timespan.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __illustrate__(self, range_=None, scale=None):
        """
        Illustrates timespan.

        Returns LilyPond file.
        """
        import abjad
        timespans = abjad.TimespanList([self])
        return timespans.__illustrate__(
            range_=range_,
            scale=scale,
            )

    def __le__(self, argument):
        """
        Is true when ``argument`` start offset is less than or equal to
        timespan start offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 <= timespan_3
            False

            >>> timespan_1 <= timespan_2
            True

        Returns true or false.
        """
        expr_start_offset, expr_stop_offset = \
            self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self._start_offset <= expr_start_offset:
                return True
            elif (self._start_offset == expr_start_offset and
                self._stop_offset <= expr_stop_offset):
                return True
            return False
        return self._start_offset <= expr_start_offset

    def __len__(self):
        """
        Defined equal to ``1`` for all timespans.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)

            >>> len(timespan)
            1

        Returns positive integer.
        """
        return 1

    def __lt__(self, argument):
        """
        Is true when ``argument`` start offset is less than timespan start
        offset.

        ..  container::: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_1 < timespan_2
            True

            >>> timespan_2 < timespan_3
            False

        Returns true or false.
        """
        expr_start_offset, expr_stop_offset = \
            self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self._start_offset < expr_start_offset:
                return True
            elif (self._start_offset == expr_start_offset and
                self._stop_offset < expr_stop_offset):
                return True
            return False
        return self._start_offset < expr_start_offset

    def __or__(self, argument):
        """
        Logical OR of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> new_timespan = timespan_1 | timespan_2
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_1 | timespan_3
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_1 | timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_2 | timespan_3
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_2 | timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_3 | timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

        Returns timespan list.
        """
        import abjad
        argument = self._get_timespan(argument)
        if (not self.intersects_timespan(argument) and
            not self.is_tangent_to_timespan(argument)):
            result = abjad.TimespanList([self, argument])
            result.sort()
            return result
        new_start_offset = min(self._start_offset, argument.start_offset)
        new_stop_offset = max(self._stop_offset, argument.stop_offset)
        timespan = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return abjad.TimespanList([timespan])

    def __sub__(self, argument):
        """
        Subtract ``argument`` from timespan.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> timespan_1 - timespan_1
            TimespanList([])

            >>> timespan_1 - timespan_2
            TimespanList([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))])

            >>> timespan_1 - timespan_3
            TimespanList([Timespan(start_offset=Offset(2, 1), stop_offset=Offset(10, 1))])

            >>> timespan_1 - timespan_4
            TimespanList([Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))])

            >>> timespan_2 - timespan_1
            TimespanList([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(12, 1))])

            >>> timespan_2 - timespan_2
            TimespanList([])

            >>> timespan_2 - timespan_3
            TimespanList([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(12, 1))])

            >>> timespan_2 - timespan_4
            TimespanList([Timespan(start_offset=Offset(5, 1), stop_offset=Offset(10, 1))])

            >>> timespan_3 - timespan_3
            TimespanList([])

            >>> timespan_3 - timespan_1
            TimespanList([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(0, 1))])

            >>> timespan_3 - timespan_2
            TimespanList([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(2, 1))])

            >>> timespan_3 - timespan_4
            TimespanList([Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(2, 1))])

            >>> timespan_4 - timespan_4
            TimespanList([])

            >>> timespan_4 - timespan_1
            TimespanList([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(20, 1))])

            >>> timespan_4 - timespan_2
            TimespanList([Timespan(start_offset=Offset(12, 1), stop_offset=Offset(20, 1))])

            >>> timespan_4 - timespan_3
            TimespanList([Timespan(start_offset=Offset(10, 1), stop_offset=Offset(20, 1))])

        Returns timespan list.
        """
        import abjad
        argument = self._get_timespan(argument)
        timespans = abjad.TimespanList()
        if not self.intersects_timespan(argument):
            timespans.append(copy.deepcopy(self))
        elif argument.trisects_timespan(self):
            new_start_offset = self._start_offset
            new_stop_offset = argument.start_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
            new_start_offset = argument.stop_offset
            new_stop_offset = self._stop_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
        elif argument.contains_timespan_improperly(self):
            pass
        elif argument.overlaps_only_start_of_timespan(self):
            new_start_offset = argument.stop_offset
            new_stop_offset = self._stop_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
        elif argument.overlaps_only_stop_of_timespan(self):
            new_start_offset = self._start_offset
            new_stop_offset = argument.start_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
        elif (argument.starts_when_timespan_starts(self) and
            argument.stops_before_timespan_stops(self)):
            new_start_offset = argument.stop_offset
            new_stop_offset = self._stop_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
        elif (argument.stops_when_timespan_stops(self) and
            argument.starts_after_timespan_starts(self)):
            new_start_offset = self._start_offset
            new_stop_offset = argument.start_offset
            timespan = abjad.new(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
                )
            timespans.append(timespan)
        else:
            raise ValueError(self, argument)
        return timespans

    def __xor__(self, argument):
        """
        Logical XOR of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> new_timespan = timespan_1 ^ timespan_2
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_1 ^ timespan_3
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(0, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(2, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_1 ^ timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_2 ^ timespan_3
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_2 ^ timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(12, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

            >>> new_timespan = timespan_3 ^ timespan_4
            >>> abjad.f(new_timespan)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

        Returns timespan list.
        """
        import abjad
        argument = self._get_timespan(argument)
        if (not self.intersects_timespan(argument) or
            self.is_tangent_to_timespan(argument)):
            result = abjad.TimespanList()
            result.append(copy.deepcopy(self))
            result.append(copy.deepcopy(argument))
            result.sort()
            return result
        result = abjad.TimespanList()
        start_offsets = [self._start_offset, argument.start_offset]
        stop_offsets = [self._stop_offset, argument.stop_offset]
        start_offsets.sort()
        stop_offsets.sort()
        timespan_1 = abjad.new(
            self,
            start_offset=start_offsets[0],
            stop_offset=start_offsets[1],
            )
        timespan_2 = abjad.new(
            self,
            start_offset=stop_offsets[0],
            stop_offset=stop_offsets[1],
            )
        if timespan_1.is_well_formed:
            result.append(timespan_1)
        if timespan_2.is_well_formed:
            result.append(timespan_2)
        result.sort()
        return result

    ### PRIVATE METHODS ###

    def _as_postscript(
        self,
        postscript_x_offset,
        postscript_y_offset,
        postscript_scale,
        ):
        import abjad
        start = (float(self._start_offset) * postscript_scale)
        start -= postscript_x_offset
        stop = (float(self._stop_offset) * postscript_scale)
        stop -= postscript_x_offset
        ps = abjad.Postscript()
        ps = ps.moveto(start, postscript_y_offset)
        ps = ps.lineto(stop, postscript_y_offset)
        ps = ps.stroke()
        ps = ps.moveto(start, postscript_y_offset + 0.75)
        ps = ps.lineto(start, postscript_y_offset - 0.75)
        ps = ps.stroke()
        ps = ps.moveto(stop, postscript_y_offset + 0.75)
        ps = ps.lineto(stop, postscript_y_offset - 0.75)
        ps = ps.stroke()
        return ps

    def _can_fuse(self, argument):
        if isinstance(argument, type(self)):
            return self.intersects_timespan(argument) or \
                self.stops_when_timespan_starts(argument)
        return False

    @staticmethod
    def _get_offsets(argument):
        if isinstance(argument, Timespan):
            pass
        elif hasattr(argument, 'timespan'):
            argument = argument.timespan
        elif hasattr(argument, '_get_timespan'):
            argument = argument._get_timespan()
        else:
            raise ValueError(argument)
        return argument._start_offset, argument._stop_offset

    @staticmethod
    def _get_start_offset_and_maybe_stop_offset(argument):
        if isinstance(argument, Timespan):
            pass
        elif hasattr(argument, 'timespan'):
            argument = argument.timespan
        elif hasattr(argument, '_get_timespan'):
            argument = argument._get_timespan()
        start_offset = getattr(argument, 'start_offset', None)
        if start_offset is None:
            raise ValueError(argument)
        stop_offset = getattr(argument, 'stop_offset', None)
        return start_offset, stop_offset

    def _get_timespan(self, argument):
        import abjad
        if isinstance(argument, Timespan):
            start_offset, stop_offset = argument.offsets
        elif hasattr(argument, 'timespan'):
            start_offset, stop_offset = argument.timespan.offsets
        elif hasattr(argument, '_get_timespan'):
            start_offset, stop_offset = argument._get_timespan().offsets
        # TODO: remove this branch in favor of the _get_timespan above
        #elif hasattr(argument, 'timespan'):
        #    start_offset, stop_offset = argument.timespan().offsets
        else:
            raise ValueError(argument)
        return abjad.new(
            self,
            start_offset=start_offset,
            stop_offset=stop_offset,
            )

    @staticmethod
    def _implements_timespan_interface(timespan):
        if (
            getattr(timespan, 'start_offset', 'foo') != 'foo' and
            getattr(timespan, 'stop_offset', 'foo') != 'foo'
            ):
            return True
        if hasattr(timespan, '_get_timespan'):
            return True
        # TODO: remove this branch in favor of the _get_timespan above
        if hasattr(timespan, 'timespan'):
            return True
        if getattr(timespan, 'timespan', 'foo') != 'foo':
            return True
        return False

    def _initialize_offset(self, offset):
        import abjad
        if offset in (NegativeInfinity, Infinity):
            return offset
        return abjad.Offset(offset)

    ### PUBLIC METHODS ###

    def contains_timespan_improperly(self, timespan):
        """
        Is true when timespan contains ``timespan`` improperly.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 10)

            >>> timespan_1.contains_timespan_improperly(timespan_1)
            True
            >>> timespan_1.contains_timespan_improperly(timespan_2)
            True
            >>> timespan_2.contains_timespan_improperly(timespan_1)
            False
            >>> timespan_2.contains_timespan_improperly(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset <= expr_start_offset and
            expr_stop_offset <= self_stop_offset
            )

    def curtails_timespan(self, timespan):
        """
        Is true when timespan curtails ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 10)

            >>> timespan_1.curtails_timespan(timespan_1)
            False
            >>> timespan_1.curtails_timespan(timespan_2)
            False
            >>> timespan_2.curtails_timespan(timespan_1)
            True
            >>> timespan_2.curtails_timespan(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset < self_start_offset and
            self_start_offset <= expr_stop_offset and
            expr_stop_offset <= self_stop_offset
            )

    def delays_timespan(self, timespan):
        """
        Is true when timespan delays ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> timespan_3 = abjad.Timespan(10, 20)

            >>> timespan_1.delays_timespan(timespan_2)
            True
            >>> timespan_2.delays_timespan(timespan_3)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset <= expr_start_offset and
            expr_start_offset < self_stop_offset
            )

    def divide_by_ratio(self, ratio):
        """
        Divides timespan by ``ratio``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> for x in timespan.divide_by_ratio((1, 2, 1)):
            ...     x
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(3, 4))
            Timespan(start_offset=Offset(3, 4), stop_offset=Offset(5, 4))
            Timespan(start_offset=Offset(5, 4), stop_offset=Offset(3, 2))

        Returns tuple of newly constructed timespans.
        """
        import abjad
        if isinstance(ratio, int):
            ratio = ratio * (1, )
        ratio = abjad.Ratio(ratio)
        unit_duration = self.duration / sum(ratio.numbers)
        part_durations = [
            numerator * unit_duration for numerator in ratio.numbers
            ]
        start_offsets = abjad.mathtools.cumulative_sums(
            [self._start_offset] + part_durations,
            start=None,
            )
        offset_pairs = abjad.sequence(start_offsets).nwise()
        result = [type(self)(*offset_pair) for offset_pair in offset_pairs]
        return tuple(result)

    def get_overlap_with_timespan(self, timespan):
        """
        Gets duration of overlap with ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 15)
            >>> timespan_2 = abjad.Timespan(5, 10)
            >>> timespan_3 = abjad.Timespan(6, 6)
            >>> timespan_4 = abjad.Timespan(12, 22)

            >>> timespan_1.get_overlap_with_timespan(timespan_1)
            Duration(15, 1)

            >>> timespan_1.get_overlap_with_timespan(timespan_2)
            Duration(5, 1)

            >>> timespan_1.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

            >>> timespan_1.get_overlap_with_timespan(timespan_4)
            Duration(3, 1)

            >>> timespan_2.get_overlap_with_timespan(timespan_2)
            Duration(5, 1)

            >>> timespan_2.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

            >>> timespan_2.get_overlap_with_timespan(timespan_4)
            Duration(0, 1)

            >>> timespan_3.get_overlap_with_timespan(timespan_3)
            Duration(0, 1)

            >>> timespan_3.get_overlap_with_timespan(timespan_4)
            Duration(0, 1)

            >>> timespan_4.get_overlap_with_timespan(timespan_4)
            Duration(10, 1)

        Returns duration.
        """
        import abjad
        if self._implements_timespan_interface(timespan):
            result = abjad.Duration(
                sum(x.duration for x in self & timespan)
                )
            return result

    def happens_during_timespan(self, timespan):
        """
        Is true when timespan happens during ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 10)

            >>> timespan_1.happens_during_timespan(timespan_1)
            True
            >>> timespan_1.happens_during_timespan(timespan_2)
            False
            >>> timespan_2.happens_during_timespan(timespan_1)
            True
            >>> timespan_2.happens_during_timespan(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset <= self_start_offset and
            self_stop_offset <= expr_stop_offset
            )

    def intersects_timespan(self, timespan):
        """
        Is true when timespan intersects ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> timespan_3 = abjad.Timespan(10, 15)

            >>> timespan_1.intersects_timespan(timespan_1)
            True
            >>> timespan_1.intersects_timespan(timespan_2)
            True
            >>> timespan_1.intersects_timespan(timespan_3)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            (
                expr_start_offset <= self_start_offset and
                self_start_offset < expr_stop_offset
            ) or (
                self_start_offset <= expr_start_offset and
                expr_start_offset < self_stop_offset
                )
            )

    def is_congruent_to_timespan(self, timespan):
        """
        Is true when timespan is congruent to ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.is_congruent_to_timespan(timespan_1)
            True
            >>> timespan_1.is_congruent_to_timespan(timespan_2)
            False
            >>> timespan_2.is_congruent_to_timespan(timespan_1)
            False
            >>> timespan_2.is_congruent_to_timespan(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset == self_start_offset and
            expr_stop_offset == self_stop_offset
            )

    def is_tangent_to_timespan(self, timespan):
        """
        Is true when timespan is tangent to ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.is_tangent_to_timespan(timespan_1)
            False
            >>> timespan_1.is_tangent_to_timespan(timespan_2)
            True
            >>> timespan_2.is_tangent_to_timespan(timespan_1)
            True
            >>> timespan_2.is_tangent_to_timespan(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_stop_offset == expr_start_offset or
            expr_stop_offset == self_start_offset
            )

    def overlaps_all_of_timespan(self, timespan):
        """
        Is true when timespan overlaps all of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 6)
            >>> timespan_3 = abjad.Timespan(5, 10)

            >>> timespan_1.overlaps_all_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_all_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_all_of_timespan(timespan_3)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset < expr_start_offset and
            expr_stop_offset < self_stop_offset
            )

    def overlaps_only_start_of_timespan(self, timespan):
        """
        Is true when timespan overlaps only start of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(-5, 5)
            >>> timespan_3 = abjad.Timespan(4, 6)
            >>> timespan_4 = abjad.Timespan(5, 15)

            >>> timespan_1.overlaps_only_start_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_2)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_3)
            False
            >>> timespan_1.overlaps_only_start_of_timespan(timespan_4)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset < expr_start_offset and
            expr_start_offset < self_stop_offset and
            self_stop_offset <= expr_stop_offset
            )

    def overlaps_only_stop_of_timespan(self, timespan):
        """
        Is true when timespan overlaps only stop of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(-5, 5)
            >>> timespan_3 = abjad.Timespan(4, 6)
            >>> timespan_4 = abjad.Timespan(5, 15)

            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_3)
            False
            >>> timespan_1.overlaps_only_stop_of_timespan(timespan_4)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset <= self_start_offset and
            self_start_offset < expr_stop_offset and
            expr_stop_offset < self_stop_offset
            )

    def overlaps_start_of_timespan(self, timespan):
        """
        Is true when timespan overlaps start of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(-5, 5)
            >>> timespan_3 = abjad.Timespan(4, 6)
            >>> timespan_4 = abjad.Timespan(5, 15)

            >>> timespan_1.overlaps_start_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_start_of_timespan(timespan_2)
            False
            >>> timespan_1.overlaps_start_of_timespan(timespan_3)
            True
            >>> timespan_1.overlaps_start_of_timespan(timespan_4)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset < expr_start_offset and
            expr_start_offset < self_stop_offset
            )

    def overlaps_stop_of_timespan(self, timespan):
        """
        Is true when timespan overlaps start of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(-5, 5)
            >>> timespan_3 = abjad.Timespan(4, 6)
            >>> timespan_4 = abjad.Timespan(5, 15)

            >>> timespan_1.overlaps_stop_of_timespan(timespan_1)
            False
            >>> timespan_1.overlaps_stop_of_timespan(timespan_2)
            True
            >>> timespan_1.overlaps_stop_of_timespan(timespan_3)
            True
            >>> timespan_1.overlaps_stop_of_timespan(timespan_4)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            self_start_offset < expr_stop_offset and
            expr_stop_offset < self_stop_offset
            )

    def reflect(self, axis=None):
        """
        Reflects timespan about ``axis``.

        ..  container:: example

            Reverse timespan about timespan axis:

            >>> abjad.Timespan(3, 6).reflect()
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        ..  container:: example

            Reverse timespan about arbitrary axis:

            >>> abjad.Timespan(3, 6).reflect(axis=abjad.Offset(10))
            Timespan(start_offset=Offset(14, 1), stop_offset=Offset(17, 1))

        Returns new timespan.
        """
        if axis is None:
            axis = self.axis
        start_distance = self._start_offset - axis
        stop_distance = self._stop_offset - axis
        new_start_offset = axis - stop_distance
        new_stop_offset = axis - start_distance
        return self.set_offsets(new_start_offset, new_stop_offset)

    def round_offsets(self, multiplier, anchor=enums.Left, must_be_well_formed=True):
        """
        Rounds timespan offsets to multiple of ``multiplier``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 5), (4, 5))

            >>> timespan.round_offsets(1)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(1, 1))

            >>> timespan.round_offsets(2)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))

            >>> timespan.round_offsets(
            ...     2,
            ...     anchor=abjad.Right,
            ...     )
            Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(0, 1))

            >>> timespan.round_offsets(
            ...     2,
            ...     anchor=abjad.Right,
            ...     must_be_well_formed=False,
            ...     )
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(0, 1))

        Returns new timespan.
        """
        import abjad
        multiplier = abs(abjad.Multiplier(multiplier))
        assert 0 < multiplier
        new_start_offset = abjad.Offset(
            int(round(self._start_offset / multiplier)) * multiplier)
        new_stop_offset = abjad.Offset(
            int(round(self._stop_offset / multiplier)) * multiplier)
        if (new_start_offset == new_stop_offset) and must_be_well_formed:
            if anchor is enums.Left:
                new_stop_offset = new_stop_offset + multiplier
            else:
                new_start_offset = new_start_offset - multiplier
        result = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return result

    def scale(self, multiplier, anchor=enums.Left):
        """
        Scales timespan by ``multiplier``.

            >>> timespan = abjad.Timespan(3, 6)

        ..  container:: example

            Scale timespan relative to timespan start offset:

            >>> timespan.scale(abjad.Multiplier(2))
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(9, 1))

        ..  container:: example

            Scale timespan relative to timespan stop offset:

            >>> timespan.scale(abjad.Multiplier(2), anchor=abjad.Right)
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(6, 1))

        Returns new timespan.
        """
        import abjad
        multiplier = abjad.Multiplier(multiplier)
        assert 0 < multiplier
        new_duration = multiplier * self.duration
        if anchor == enums.Left:
            new_start_offset = self._start_offset
            new_stop_offset = self._start_offset + new_duration
        elif anchor == enums.Right:
            new_stop_offset = self._stop_offset
            new_start_offset = self._stop_offset - new_duration
        else:
            message = 'unknown anchor direction: {!r}.'
            message = message.format(anchor)
            raise ValueError(message)
        result = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return result

    def set_duration(self, duration):
        """
        Sets timespan duration to ``duration``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.set_duration((3, 5))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(11, 10))

        Returns new timespan.
        """
        import abjad
        duration = abjad.Duration(duration)
        new_stop_offset = self._start_offset + duration
        return abjad.new(
            self,
            stop_offset=new_stop_offset,
            )

    def set_offsets(self, start_offset=None, stop_offset=None):
        """
        Sets timespan start offset to ``start_offset`` and
        stop offset to ``stop_offset``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.set_offsets(stop_offset=(7, 8))
            Timespan(start_offset=Offset(1, 2), stop_offset=Offset(7, 8))

        Subtracts negative ``start_offset`` from existing stop offset:

        >>> timespan.set_offsets(start_offset=(-1, 2))
        Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 2))

        Subtracts negative ``stop_offset`` from existing stop offset:

        >>> timespan.set_offsets(stop_offset=(-1, 2))
        Timespan(start_offset=Offset(1, 2), stop_offset=Offset(1, 1))

        Returns new timespan.
        """
        import abjad
        if start_offset is not None:
            start_offset = abjad.Offset(start_offset)

        if stop_offset is not None:
            stop_offset = abjad.Offset(stop_offset)
        if start_offset is not None and 0 <= start_offset:
            new_start_offset = start_offset
        elif start_offset is not None and start_offset < 0:
            new_start_offset = \
                self._stop_offset + abjad.Offset(start_offset)
        else:
            new_start_offset = self._start_offset
        if stop_offset is not None and 0 <= stop_offset:
            new_stop_offset = stop_offset
        elif stop_offset is not None and stop_offset < 0:
            new_stop_offset = \
                self._stop_offset + abjad.Offset(stop_offset)
        else:
            new_stop_offset = self._stop_offset
        result = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return result

    # TODO: extend to self.split_at_offsets()
    def split_at_offset(self, offset):
        """
        Split into two parts when ``offset`` happens during timespan:

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 5)

            >>> left, right = timespan.split_at_offset((2, 1))

            >>> left
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(2, 1))

            >>> right
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))

            Otherwise return a copy of timespan:

            >>> timespan.split_at_offset((12, 1))[0]
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))

        Returns one or two newly constructed timespans.
        """
        import abjad
        offset = abjad.Offset(offset)
        result = abjad.TimespanList()
        if self._start_offset < offset < self._stop_offset:
            left = abjad.new(
                self,
                start_offset=self._start_offset,
                stop_offset=offset,
                )
            right = abjad.new(
                self,
                start_offset=offset,
                stop_offset=self._stop_offset,
                )
            result.append(left)
            result.append(right)
        else:
            result.append(abjad.new(self))
        return result

    def split_at_offsets(self, offsets):
        """
        Split into one or more parts when ``offsets`` happens during
        timespan:

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)

            >>> result = timespan.split_at_offsets((1, 3, 7))
            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(1, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(1, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(7, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(7, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

            Otherwise return a timespan list containing a copy of timespan:

            >>> result = timespan.split_at_offsets((-100,))
            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Returns one or more newly constructed timespans.
        """
        import abjad
        offsets = [abjad.Offset(offset) for offset in offsets]
        offsets = [offset for offset in offsets
            if self._start_offset < offset < self._stop_offset]
        offsets = sorted(set(offsets))
        result = abjad.TimespanList()
        right = abjad.new(self)
        for offset in offsets:
            left, right = right.split_at_offset(offset)
            result.append(left)
        result.append(right)
        return result

    def starts_after_offset(self, offset):
        """
        Is true when timespan overlaps start of ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_after_offset((-5, 1))
            True
            >>> timespan_1.starts_after_offset((0, 1))
            False
            >>> timespan_1.starts_after_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return offset < self._start_offset

    def starts_after_timespan_starts(self, timespan):
        """
        Is true when timespan starts after ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.starts_after_timespan_starts(timespan_1)
            False
            >>> timespan_1.starts_after_timespan_starts(timespan_2)
            False
            >>> timespan_2.starts_after_timespan_starts(timespan_1)
            True
            >>> timespan_2.starts_after_timespan_starts(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return expr_start_offset < self_start_offset

    def starts_after_timespan_stops(self, timespan):
        """
        Is true when timespan starts after ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)
            >>> timespan_3 = abjad.Timespan(10, 20)
            >>> timespan_4 = abjad.Timespan(15, 25)

            >>> timespan_1.starts_after_timespan_stops(timespan_1)
            False
            >>> timespan_2.starts_after_timespan_stops(timespan_1)
            False
            >>> timespan_3.starts_after_timespan_stops(timespan_1)
            True
            >>> timespan_4.starts_after_timespan_stops(timespan_1)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return expr_stop_offset <= self_start_offset

    def starts_at_offset(self, offset):
        """
        Is true when timespan starts at ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_at_offset((-5, 1))
            False
            >>> timespan_1.starts_at_offset((0, 1))
            True
            >>> timespan_1.starts_at_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._start_offset == offset

    def starts_at_or_after_offset(self, offset):
        """
        Is true when timespan starts at or after ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_at_or_after_offset((-5, 1))
            True
            >>> timespan_1.starts_at_or_after_offset((0, 1))
            True
            >>> timespan_1.starts_at_or_after_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return offset <= self._start_offset

    def starts_before_offset(self, offset):
        """
        Is true when timespan starts before ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_before_offset((-5, 1))
            False
            >>> timespan_1.starts_before_offset((0, 1))
            False
            >>> timespan_1.starts_before_offset((5, 1))
            True

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._start_offset < offset

    def starts_before_or_at_offset(self, offset):
        """
        Is true when timespan starts before or at ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_before_or_at_offset((-5, 1))
            False
            >>> timespan_1.starts_before_or_at_offset((0, 1))
            True
            >>> timespan_1.starts_before_or_at_offset((5, 1))
            True

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._start_offset <= offset

    def starts_before_timespan_starts(self, timespan):
        """
        Is true when timespan starts before ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.starts_before_timespan_starts(timespan_1)
            False
            >>> timespan_1.starts_before_timespan_starts(timespan_2)
            True
            >>> timespan_2.starts_before_timespan_starts(timespan_1)
            False
            >>> timespan_2.starts_before_timespan_starts(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_start_offset < expr_start_offset

    def starts_before_timespan_stops(self, timespan):
        """
        Is true when timespan starts before ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.starts_before_timespan_stops(timespan_1)
            True
            >>> timespan_1.starts_before_timespan_stops(timespan_2)
            True
            >>> timespan_2.starts_before_timespan_stops(timespan_1)
            True
            >>> timespan_2.starts_before_timespan_stops(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_start_offset < expr_stop_offset

    def starts_during_timespan(self, timespan):
        """
        Is true when timespan starts during ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.starts_during_timespan(timespan_1)
            True
            >>> timespan_1.starts_during_timespan(timespan_2)
            False
            >>> timespan_2.starts_during_timespan(timespan_1)
            True
            >>> timespan_2.starts_during_timespan(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset <= self_start_offset and
            self_start_offset < expr_stop_offset
            )

    def starts_when_timespan_starts(self, timespan):
        """
        Is true when timespan starts when ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 15)

            >>> timespan_1.starts_when_timespan_starts(timespan_1)
            True
            >>> timespan_1.starts_when_timespan_starts(timespan_2)
            False
            >>> timespan_2.starts_when_timespan_starts(timespan_1)
            False
            >>> timespan_2.starts_when_timespan_starts(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return expr_start_offset == self_start_offset

    def starts_when_timespan_stops(self, timespan):
        """
        Is true when timespan starts when ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.starts_when_timespan_stops(timespan_1)
            False
            >>> timespan_1.starts_when_timespan_stops(timespan_2)
            False
            >>> timespan_2.starts_when_timespan_stops(timespan_1)
            True
            >>> timespan_2.starts_when_timespan_stops(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_start_offset == expr_stop_offset

    def stops_after_offset(self, offset):
        """
        Is true when timespan stops after ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.starts_after_offset((-5, 1))
            True
            >>> timespan_1.starts_after_offset((0, 1))
            False
            >>> timespan_1.starts_after_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return offset < self._stop_offset

    def stops_after_timespan_starts(self, timespan):
        """
        Is true when timespan stops when ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_after_timespan_starts(timespan_1)
            True
            >>> timespan_1.stops_after_timespan_starts(timespan_2)
            False
            >>> timespan_2.stops_after_timespan_starts(timespan_1)
            True
            >>> timespan_2.stops_after_timespan_starts(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return expr_start_offset < self_stop_offset

    def stops_after_timespan_stops(self, timespan):
        """
        Is true when timespan stops when ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_after_timespan_stops(timespan_1)
            False
            >>> timespan_1.stops_after_timespan_stops(timespan_2)
            False
            >>> timespan_2.stops_after_timespan_stops(timespan_1)
            True
            >>> timespan_2.stops_after_timespan_stops(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return expr_stop_offset < self_stop_offset

    def stops_at_offset(self, offset):
        """
        Is true when timespan stops at ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.stops_at_offset((-5, 1))
            False
            >>> timespan_1.stops_at_offset((0, 1))
            False
            >>> timespan_1.stops_at_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._stop_offset == offset

    def stops_at_or_after_offset(self, offset):
        """
        Is true when timespan stops at or after ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.stops_at_or_after_offset((-5, 1))
            True
            >>> timespan_1.stops_at_or_after_offset((0, 1))
            True
            >>> timespan_1.stops_at_or_after_offset((5, 1))
            True

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return offset <= self._stop_offset

    def stops_before_offset(self, offset):
        """
        Is true when timespan stops before ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.stops_before_offset((-5, 1))
            False
            >>> timespan_1.stops_before_offset((0, 1))
            False
            >>> timespan_1.stops_before_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._stop_offset < offset

    def stops_before_or_at_offset(self, offset):
        """
        Is true when timespan stops before or at ``offset``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)

            >>> timespan_1.stops_before_or_at_offset((-5, 1))
            False
            >>> timespan_1.stops_before_or_at_offset((0, 1))
            False
            >>> timespan_1.stops_before_or_at_offset((5, 1))
            False

        Returns true or false.
        """
        import abjad
        offset = abjad.Offset(offset)
        return self._stop_offset <= offset

    def stops_before_timespan_starts(self, timespan):
        """
        Is true when timespan stops before ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_before_timespan_starts(timespan_1)
            False
            >>> timespan_1.stops_before_timespan_starts(timespan_2)
            False
            >>> timespan_2.stops_before_timespan_starts(timespan_1)
            False
            >>> timespan_2.stops_before_timespan_starts(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_stop_offset < expr_start_offset

    def stops_before_timespan_stops(self, timespan):
        """
        Is true when timespan stops before ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_before_timespan_stops(timespan_1)
            False
            >>> timespan_1.stops_before_timespan_stops(timespan_2)
            True
            >>> timespan_2.stops_before_timespan_stops(timespan_1)
            False
            >>> timespan_2.stops_before_timespan_stops(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_stop_offset < expr_stop_offset

    def stops_during_timespan(self, timespan):
        """
        Is true when timespan stops during ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_during_timespan(timespan_1)
            True
            >>> timespan_1.stops_during_timespan(timespan_2)
            False
            >>> timespan_2.stops_during_timespan(timespan_1)
            False
            >>> timespan_2.stops_during_timespan(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset < self_stop_offset and
            self_stop_offset <= expr_stop_offset
            )

    def stops_when_timespan_starts(self, timespan):
        """
        Is true when timespan stops when ``timespan`` starts.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_when_timespan_starts(timespan_1)
            False
            >>> timespan_1.stops_when_timespan_starts(timespan_2)
            True
            >>> timespan_2.stops_when_timespan_starts(timespan_1)
            False
            >>> timespan_2.stops_when_timespan_starts(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_stop_offset == expr_start_offset

    def stops_when_timespan_stops(self, timespan):
        """
        Is true when timespan stops when ``timespan`` stops.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(10, 20)

            >>> timespan_1.stops_when_timespan_stops(timespan_1)
            True
            >>> timespan_1.stops_when_timespan_stops(timespan_2)
            False
            >>> timespan_2.stops_when_timespan_stops(timespan_1)
            False
            >>> timespan_2.stops_when_timespan_stops(timespan_2)
            True

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return self_stop_offset == expr_stop_offset

    def stretch(self, multiplier, anchor=None):
        """
        Stretches timespan by ``multiplier`` relative to ``anchor``.

        .. container:: example

            Stretch relative to timespan start offset:

            >>> abjad.Timespan(3, 10).stretch(abjad.Multiplier(2))
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(17, 1))

        .. container:: example

            Stretch relative to timespan stop offset:

            >>> abjad.Timespan(3, 10).stretch(
            ...     abjad.Multiplier(2),
            ...     abjad.Offset(10),
            ...     )
            Timespan(start_offset=Offset(-4, 1), stop_offset=Offset(10, 1))

        .. container:: example

            Stretch relative to offset prior to timespan:

            >>> abjad.Timespan(3, 10).stretch(
            ...     abjad.Multiplier(2),
            ...     abjad.Offset(0, 1),
            ...     )
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(20, 1))

        .. container:: example

            Stretch relative to offset after timespan:

            >>> abjad.Timespan(3, 10).stretch(
            ...     abjad.Multiplier(3),
            ...     abjad.Offset(12),
            ...     )
            Timespan(start_offset=Offset(-15, 1), stop_offset=Offset(6, 1))

        .. container:: example

            Stretch relative to offset that happens during timespan:

            >>> abjad.Timespan(3, 10).stretch(
            ...     abjad.Multiplier(2),
            ...     abjad.Offset(4),
            ...     )
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(16, 1))

        Returns newly emitted timespan.
        """
        import abjad
        multiplier = abjad.Multiplier(multiplier)
        assert 0 < multiplier
        if anchor is None:
            anchor = self._start_offset
        new_start_offset = (multiplier * (self._start_offset - anchor)) + anchor
        new_stop_offset = (multiplier * (self._stop_offset - anchor)) + anchor
        result = abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )
        return result

    def translate(self, translation=None):
        """
        Translates timespan by ``translation``.

        ..  container:: example

            >>> timespan = abjad.Timespan(5, 10)

            >>> timespan.translate(2)
            Timespan(start_offset=Offset(7, 1), stop_offset=Offset(12, 1))

        Returns new timespan.
        """
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self,
        start_offset_translation=None,
        stop_offset_translation=None,
        ):
        """
        Translates timespan start offset by ``start_offset_translation`` and
        stop offset by ``stop_offset_translation``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.translate_offsets(start_offset_translation=(-1, 8))
            Timespan(start_offset=Offset(3, 8), stop_offset=Offset(3, 2))

        Returns new timespan.
        """
        import abjad
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = abjad.Duration(start_offset_translation)
        stop_offset_translation = abjad.Duration(stop_offset_translation)
        new_start_offset = self._start_offset + start_offset_translation
        new_stop_offset = self._stop_offset + stop_offset_translation
        return abjad.new(
            self,
            start_offset=new_start_offset,
            stop_offset=new_stop_offset,
            )

    def trisects_timespan(self, timespan):
        """
        Is true when timespan trisects ``timespan``.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 6)

            >>> timespan_1.trisects_timespan(timespan_1)
            False
            >>> timespan_1.trisects_timespan(timespan_2)
            False
            >>> timespan_2.trisects_timespan(timespan_1)
            True
            >>> timespan_2.trisects_timespan(timespan_2)
            False

        Returns true or false.
        """
        self_start_offset, self_stop_offset = self.offsets
        expr_start_offset, expr_stop_offset = self._get_offsets(timespan)
        return (
            expr_start_offset < self_start_offset and
            self_stop_offset < expr_stop_offset
            )

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self):
        """
        Arithmetic mean of timespan start- and stop-offsets.

        ..  container:: example

            >>> abjad.Timespan(0, 10).axis
            Offset(5, 1)

        Returns offset.
        """
        return (self._start_offset + self._stop_offset) / 2

    @property
    def duration(self):
        """
        Duration of timespan.

        ..  container:: example

            >>> abjad.Timespan(0, 10).duration
            Duration(10, 1)

        Returns duration.
        """
        return self._stop_offset - self._start_offset

    @property
    def is_well_formed(self):
        """
        Is true when timespan start offset preceeds timespan stop offset.

        ..  container:: example

            >>> abjad.Timespan(0, 10).is_well_formed
            True

        Returns true or false.
        """
        return self._start_offset < self._stop_offset

    @property
    def offsets(self):
        """
        Timespan offsets.

        ..  container:: example

            >>> abjad.Timespan(0, 10).offsets
            (Offset(0, 1), Offset(10, 1))

        Returns offset pair.
        """
        return self._start_offset, self._stop_offset

    @property
    def start_offset(self):
        """
        Timespan start offset.

        ..  container:: example

            >>> abjad.Timespan(0, 10).start_offset
            Offset(0, 1)

        Returns offset.
        """
        return self._start_offset

    @property
    def stop_offset(self):
        """
        Timespan stop offset.

        ..  container:: example

            >>> abjad.Timespan(0, 10).stop_offset
            Offset(10, 1)

        Returns offset.
        """
        return self._stop_offset
