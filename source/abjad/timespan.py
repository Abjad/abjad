"""
Tools for modeling and manipulating timespans.
"""

import collections
import copy
import dataclasses
import fractions
import typing

from . import duration as _duration
from . import enums as _enums
from . import indicators as _indicators
from . import math as _math
from . import sequence as _sequence

infinity = _math.Infinity()
negative_infinity = _math.NegativeInfinity()


@dataclasses.dataclass(slots=True)
class OffsetCounter:
    """
    Offset counter.

    ..  container:: example

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 16),
        ...     abjad.Timespan(5, 12),
        ...     abjad.Timespan(-2, 8),
        ... ])
        >>> timespan_operand = abjad.Timespan(6, 10)
        >>> timespans = timespans - timespan_operand
        >>> offset_counter = abjad.OffsetCounter(timespans)
        >>> for item in offset_counter.items.items(): item
        (Offset((-2, 1)), 1)
        (Offset((0, 1)), 1)
        (Offset((5, 1)), 1)
        (Offset((6, 1)), 3)
        (Offset((10, 1)), 2)
        (Offset((12, 1)), 1)
        (Offset((16, 1)), 1)

        >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

    """

    items: typing.Any = ()
    item_class: typing.Any = _duration.Offset

    def __post_init__(self):
        self.item_class = _duration.Offset
        self.items = self.items or []
        if self.items:
            offsets = []
            for item in self.items:
                try:
                    offsets.append(item.start_offset)
                    offsets.append(item.stop_offset)
                except Exception:
                    if hasattr(item, "_get_timespan"):
                        timespan = item._get_timespan()
                        offsets.append(timespan.start_offset)
                        offsets.append(timespan.stop_offset)
                    else:
                        offset = _duration.Offset(item)
                        offsets.append(offset)
            self.items = offsets
        self.items = [self._coerce_item(_) for _ in self.items]
        self.items = collections.Counter(self.items)
        sorted_item_to_count = {}
        try:
            sorted_items = sorted(self.items.items())
        except TypeError:
            sorted_items = self.items.items()
        for item, count in sorted_items:
            sorted_item_to_count[item] = count
        self.items = sorted_item_to_count

    def _coerce_item(self, item):
        return _duration.Offset(item)

    def _make_markup(self, range_=None, scale=None) -> _indicators.Markup:
        r"""
        Illustrates offset counter.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ... ])
            >>> timespan_operand = abjad.Timespan(6, 10)
            >>> timespans = timespans - timespan_operand
            >>> offset_counter = abjad.OffsetCounter(timespans)
            >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> markup = offset_counter._make_markup()
                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup
                \overlay
                {
                \postscript
                #"
                0.2 setlinewidth
                [ 2 1 ] 0 setdash
                1 -1 moveto
                0 -2 rlineto
                stroke
                17.666666666666668 -1 moveto
                0 -2 rlineto
                stroke
                59.33333333333334 -1 moveto
                0 -2 rlineto
                stroke
                67.66666666666667 -1 moveto
                0 -8 rlineto
                stroke
                101.00000000000001 -1 moveto
                0 -5 rlineto
                stroke
                117.66666666666667 -1 moveto
                0 -2 rlineto
                stroke
                151 -1 moveto
                0 -2 rlineto
                stroke
                "
                \translate #'(1.0 . 1)
                \sans \fontsize #-3 \center-align \fraction -2 1
                \translate #'(17.666666666666668 . 1)
                \sans \fontsize #-3 \center-align \fraction 0 1
                \translate #'(59.33333333333334 . 1)
                \sans \fontsize #-3 \center-align \fraction 5 1
                \translate #'(67.66666666666667 . 1)
                \sans \fontsize #-3 \center-align \fraction 6 1
                \translate #'(101.00000000000001 . 1)
                \sans \fontsize #-3 \center-align \fraction 10 1
                \translate #'(117.66666666666667 . 1)
                \sans \fontsize #-3 \center-align \fraction 12 1
                \translate #'(151.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 16 1
                }

        """
        if not self:
            return _indicators.Markup(r"\markup \null")
        if isinstance(range_, Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = min(self.items), max(self.items)
        minimum_float = float(_duration.Offset(minimum))
        maximum_float = float(_duration.Offset(maximum))
        if scale is None:
            scale = 1.0
        assert 0 < scale
        postscript_scale = 150.0 / (maximum_float - minimum_float)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum_float * postscript_scale) - 1
        postscript_strings = [
            "0.2 setlinewidth",
            "[ 2 1 ] 0 setdash",
        ]
        for offset, count in sorted(self.items.items()):
            offset = float(offset) * postscript_scale
            offset -= postscript_x_offset
            postscript_strings.extend(
                [
                    f"{_fpa(offset)} -1 moveto",
                    f"0 {_fpa((float(count) * -3) + 1)} rlineto",
                    "stroke",
                ]
            )
        strings = [
            r"\markup",
            r"\overlay",
            "{",
            r"\postscript",
            '#"',
            *postscript_strings,
            '"',
        ]
        for offset in sorted(self.items):
            offset = _duration.Offset(offset)
            n, d = offset.numerator, offset.denominator
            x_translation = float(offset) * postscript_scale
            x_translation -= postscript_x_offset
            string = rf"\translate #'({x_translation} . 1)"
            strings.append(string)
            string = rf"\sans \fontsize #-3 \center-align \fraction {n} {d}"
            strings.append(string)
        strings.append("}")
        string = "\n".join(strings)
        markup = _indicators.Markup(string)
        return markup


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Timespan:
    """
    Timespan.

    ..  container:: example

        >>> timespan_1 = abjad.Timespan(0, 10)
        >>> timespan_2 = abjad.Timespan(5, 12)
        >>> timespan_3 = abjad.Timespan(-2, 2)
        >>> timespan_4 = abjad.Timespan(10, 20)

    ..  container:: example

        Annotations work like this:

        >>> annotated_timespan = abjad.Timespan(
        ...     annotation=["a", "b", "c", "foo"],
        ...     start_offset=(1, 4),
        ...     stop_offset=(7, 8),
        ... )
        >>> annotated_timespan.annotation
        ['a', 'b', 'c', 'foo']

        Annotated timespans maintain their annotations duration mutation:

        >>> left, right = annotated_timespan.split_at_offset((1, 2))
        >>> left.annotation.append("foo")
        >>> right
        Timespan(Offset((1, 2)), Offset((7, 8)), annotation=['a', 'b', 'c', 'foo', 'foo'])

    Timespans are closed-open intervals.
    """

    start_offset: typing.Any = None
    stop_offset: typing.Any = None
    annotation: typing.Any = None

    __documentation_section__ = "Timespans"

    def __post_init__(self):
        if isinstance(self.start_offset, type(self)):
            raise Exception("can not initialize from timespan.")
        if isinstance(self.stop_offset, type(self)):
            raise Exception("can not initialize from timespan.")
        if self.start_offset is None:
            self.start_offset = negative_infinity
        if self.stop_offset is None:
            self.stop_offset = infinity
        self.start_offset = self._initialize_offset(self.start_offset)
        self.stop_offset = self._initialize_offset(self.stop_offset)
        assert self.start_offset <= self.stop_offset, repr(
            (self.start_offset, self.stop_offset)
        )

    ### SPECIAL METHODS ###

    def __and__(self, argument) -> "TimespanList":
        """
        Logical AND of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> timespan_1 & timespan_2
            TimespanList([Timespan(Offset((5, 1)), Offset((10, 1)))])

            >>> timespan_1 & timespan_3
            TimespanList([Timespan(Offset((0, 1)), Offset((2, 1)))])

            >>> timespan_1 & timespan_4
            TimespanList([])

            >>> timespan_2 & timespan_3
            TimespanList([])

            >>> timespan_2 & timespan_4
            TimespanList([Timespan(Offset((10, 1)), Offset((12, 1)))])

            >>> timespan_3 & timespan_4
            TimespanList([])

        """
        argument = self._get_timespan(argument)
        if not (
            argument.start_offset <= self.start_offset
            and self.start_offset < argument.stop_offset
        ) and not (
            self.start_offset <= argument.start_offset
            and argument.start_offset < self.stop_offset
        ):
            return TimespanList()
        new_start_offset = max(self.start_offset, argument.start_offset)
        new_stop_offset = min(self.stop_offset, argument.stop_offset)
        timespan = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return TimespanList([timespan])

    def __contains__(self, argument) -> bool:
        """
        Is true when timespan contains ``argument``.

        ..  container:: example

            Works with offsets:

            >>> timespan = abjad.Timespan(0, (1, 4))

            >>> -1 in timespan
            False

            >>> 0 in timespan
            True

            >>> abjad.Offset(1, 8) in timespan
            True

            >>> abjad.Offset(1, 4) in timespan
            True

            >>> abjad.Offset(1, 2) in timespan
            False

        ..  container:: example

            Works with other timespans:

            >>> timespan = abjad.Timespan(0, (1, 4))

            >>> abjad.Timespan(0, (1, 4)) in timespan
            True

            >>> abjad.Timespan((1, 16), (2, 16)) in timespan
            True

            >>> abjad.Timespan(0, (1, 2)) in timespan
            False

        """
        if isinstance(argument, type(self)):
            timespan = argument
        else:
            timespan = type(self)(argument, argument)
        assert isinstance(timespan, type(self))
        return (
            self.start_offset <= timespan.start_offset
            and timespan.stop_offset <= self.stop_offset
        )

    def __eq__(self, argument) -> bool:
        """
        Compares ``start_offset``, ``stop_offset``.

        ..  container:: example

            >>> abjad.Timespan(1, 3) == abjad.Timespan(1, 3)
            True

            >>> abjad.Timespan(1, 3) == abjad.Timespan(2, 3)
            False

        """
        if isinstance(argument, type(self)):
            if self.start_offset == argument.start_offset:
                return self.stop_offset == argument.stop_offset
        return False

    def __ge__(self, argument) -> bool:
        """
        Is true when ``argument`` start offset is greater or equal to timespan start
        offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 >= timespan_3
            True

            >>> timespan_1 >= timespan_2
            False

        """
        (
            expr_start_offset,
            expr_stop_offset,
        ) = self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self.start_offset >= expr_start_offset:
                return True
            elif (
                self.start_offset == expr_start_offset
                and self.stop_offset >= expr_stop_offset
            ):
                return True
            return False
        return self.start_offset >= expr_start_offset

    def __gt__(self, argument) -> bool:
        """
        Is true when ``argument`` start offset is greater than timespan start offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 > timespan_3
            True

            >>> timespan_1 > timespan_2
            False

        """
        (
            expr_start_offset,
            expr_stop_offset,
        ) = self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self.start_offset > expr_start_offset:
                return True
            elif (
                self.start_offset == expr_start_offset
                and self.stop_offset > expr_stop_offset
            ):
                return True
            return False
        return self.start_offset > expr_start_offset

    def __le__(self, argument) -> bool:
        """
        Is true when ``argument`` start offset is less than or equal to timespan start
        offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_2 <= timespan_3
            False

            >>> timespan_1 <= timespan_2
            True

        """
        (
            expr_start_offset,
            expr_stop_offset,
        ) = self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self.start_offset <= expr_start_offset:
                return True
            elif (
                self.start_offset == expr_start_offset
                and self.stop_offset <= expr_stop_offset
            ):
                return True
            return False
        return self.start_offset <= expr_start_offset

    def __len__(self) -> int:
        """
        Defined equal to ``1`` for all timespans.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)

            >>> len(timespan)
            1

        """
        return 1

    def __lt__(self, argument) -> bool:
        r"""
        Is true when ``argument`` start offset is less than timespan start offset.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)

            >>> timespan_1 < timespan_2
            True

            >>> timespan_2 < timespan_3
            False

        """
        (
            expr_start_offset,
            expr_stop_offset,
        ) = self._get_start_offset_and_maybe_stop_offset(argument)
        if expr_stop_offset is not None:
            if self.start_offset < expr_start_offset:
                return True
            elif (
                self.start_offset == expr_start_offset
                and self.stop_offset < expr_stop_offset
            ):
                return True
            return False
        return self.start_offset < expr_start_offset

    def __or__(self, argument) -> "TimespanList":
        """
        Logical OR of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> timespans = timespan_1 | timespan_2
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((12, 1)))

            >>> timespans = timespan_1 | timespan_3
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((10, 1)))

            >>> timespans = timespan_1 | timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((20, 1)))

            >>> timespans = timespan_2 | timespan_3
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((5, 1)), Offset((12, 1)))

            >>> timespans = timespan_2 | timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((20, 1)))

            >>> timespans = timespan_3 | timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((10, 1)), Offset((20, 1)))

        """
        argument = self._get_timespan(argument)
        if (
            not bool(self & argument)
            and not self.stop_offset == argument.start_offset
            and not argument.stop_offset == self.start_offset
        ):
            result = TimespanList([self, argument])
            result.sort()
            return result
        new_start_offset = min(self.start_offset, argument.start_offset)
        new_stop_offset = max(self.stop_offset, argument.stop_offset)
        timespan = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return TimespanList([timespan])

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        if self.annotation is None:
            return f"{type(self).__name__}({self.start_offset!r}, {self.stop_offset!r})"
        else:
            return f"{type(self).__name__}({self.start_offset!r}, {self.stop_offset!r}, annotation={self.annotation!r})"

    def __sub__(self, argument) -> "TimespanList":
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
            TimespanList([Timespan(Offset((0, 1)), Offset((5, 1)))])

            >>> timespan_1 - timespan_3
            TimespanList([Timespan(Offset((2, 1)), Offset((10, 1)))])

            >>> timespan_1 - timespan_4
            TimespanList([Timespan(Offset((0, 1)), Offset((10, 1)))])

            >>> timespan_2 - timespan_1
            TimespanList([Timespan(Offset((10, 1)), Offset((12, 1)))])

            >>> timespan_2 - timespan_2
            TimespanList([])

            >>> timespan_2 - timespan_3
            TimespanList([Timespan(Offset((5, 1)), Offset((12, 1)))])

            >>> timespan_2 - timespan_4
            TimespanList([Timespan(Offset((5, 1)), Offset((10, 1)))])

            >>> timespan_3 - timespan_3
            TimespanList([])

            >>> timespan_3 - timespan_1
            TimespanList([Timespan(Offset((-2, 1)), Offset((0, 1)))])

            >>> timespan_3 - timespan_2
            TimespanList([Timespan(Offset((-2, 1)), Offset((2, 1)))])

            >>> timespan_3 - timespan_4
            TimespanList([Timespan(Offset((-2, 1)), Offset((2, 1)))])

            >>> timespan_4 - timespan_4
            TimespanList([])

            >>> timespan_4 - timespan_1
            TimespanList([Timespan(Offset((10, 1)), Offset((20, 1)))])

            >>> timespan_4 - timespan_2
            TimespanList([Timespan(Offset((12, 1)), Offset((20, 1)))])

            >>> timespan_4 - timespan_3
            TimespanList([Timespan(Offset((10, 1)), Offset((20, 1)))])

        Returns timespan list.
        """
        argument = self._get_timespan(argument)
        timespans = TimespanList()
        if not bool(self & argument):
            timespans.append(copy.deepcopy(self))
        elif (
            self.start_offset < argument.start_offset
            and argument.stop_offset < self.stop_offset
        ):
            new_start_offset = self.start_offset
            new_stop_offset = argument.start_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
            new_start_offset = argument.stop_offset
            new_stop_offset = self.stop_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
        elif self in argument:
            pass
        elif (
            argument.start_offset < self.start_offset
            and self.start_offset < argument.stop_offset
            and argument.stop_offset <= self.stop_offset
        ):
            new_start_offset = argument.stop_offset
            new_stop_offset = self.stop_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
        elif (
            self.start_offset <= argument.start_offset
            and argument.start_offset < self.stop_offset
            and self.stop_offset < argument.stop_offset
        ):
            new_start_offset = self.start_offset
            new_stop_offset = argument.start_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
        elif (
            argument.start_offset == self.start_offset
            and argument.stop_offset < self.stop_offset
        ):
            new_start_offset = argument.stop_offset
            new_stop_offset = self.stop_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
        elif (
            argument.stop_offset == self.stop_offset
            and self.start_offset < argument.start_offset
        ):
            new_start_offset = self.start_offset
            new_stop_offset = argument.start_offset
            timespan = dataclasses.replace(
                self,
                start_offset=new_start_offset,
                stop_offset=new_stop_offset,
            )
            timespans.append(timespan)
        else:
            raise ValueError(self, argument)
        return timespans

    def __xor__(self, argument) -> "TimespanList":
        """
        Logical XOR of two timespans.

        ..  container:: example

            >>> timespan_1 = abjad.Timespan(0, 10)
            >>> timespan_2 = abjad.Timespan(5, 12)
            >>> timespan_3 = abjad.Timespan(-2, 2)
            >>> timespan_4 = abjad.Timespan(10, 20)

            >>> timespans = timespan_1 ^ timespan_2
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((10, 1)), Offset((12, 1)))

            >>> timespans = timespan_1 ^ timespan_3
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((0, 1)))
            Timespan(Offset((2, 1)), Offset((10, 1)))

            >>> timespans = timespan_1 ^ timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((10, 1)))
            Timespan(Offset((10, 1)), Offset((20, 1)))

            >>> timespans = timespan_2 ^ timespan_3
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((5, 1)), Offset((12, 1)))

            >>> timespans = timespan_2 ^ timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((10, 1)))
            Timespan(Offset((12, 1)), Offset((20, 1)))

            >>> timespans = timespan_3 ^ timespan_4
            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((10, 1)), Offset((20, 1)))

        """
        argument = self._get_timespan(argument)
        if (
            not bool(self & argument)
            and not self.stop_offset == argument.start_offset
            and not argument.stop_offset == self.start_offset
        ):
            result = TimespanList()
            result.append(copy.deepcopy(self))
            result.append(copy.deepcopy(argument))
            result.sort()
            return result
        result = TimespanList()
        start_offsets = [self.start_offset, argument.start_offset]
        stop_offsets = [self.stop_offset, argument.stop_offset]
        start_offsets.sort()
        stop_offsets.sort()
        timespan_1 = dataclasses.replace(
            self, start_offset=start_offsets[0], stop_offset=start_offsets[1]
        )
        timespan_2 = dataclasses.replace(
            self, start_offset=stop_offsets[0], stop_offset=stop_offsets[1]
        )
        if timespan_1.wellformed:
            result.append(timespan_1)
        if timespan_2.wellformed:
            result.append(timespan_2)
        result.sort()
        return result

    ### PRIVATE METHODS ###

    def _as_postscript(
        self, postscript_x_offset, postscript_y_offset, postscript_scale
    ):
        start = float(self.start_offset) * postscript_scale
        start -= postscript_x_offset
        stop = float(self.stop_offset) * postscript_scale
        stop -= postscript_x_offset
        strings = [
            f"{_fpa(start)} {_fpa(postscript_y_offset)} moveto",
            f"{_fpa(stop)} {_fpa(postscript_y_offset)} lineto",
            "stroke",
            f"{_fpa(start)} {_fpa(postscript_y_offset + 0.75)} moveto",
            f"{_fpa(start)} {_fpa(postscript_y_offset - 0.75)} lineto",
            "stroke",
            f"{_fpa(stop)} {_fpa(postscript_y_offset + 0.75)} moveto",
            f"{_fpa(stop)} {_fpa(postscript_y_offset - 0.75)} lineto",
            "stroke",
        ]
        return strings

    def _can_fuse(self, argument):
        if isinstance(argument, type(self)):
            return bool(self & argument) or self.stop_offset == argument.start_offset
        return False

    @staticmethod
    def _get_offsets(argument):
        if isinstance(argument, Timespan):
            pass
        elif hasattr(argument, "timespan"):
            argument = argument.timespan
        elif hasattr(argument, "_get_timespan"):
            argument = argument._get_timespan()
        else:
            raise ValueError(argument)
        return argument.start_offset, argument.stop_offset

    @staticmethod
    def _get_start_offset_and_maybe_stop_offset(argument):
        if isinstance(argument, Timespan):
            pass
        elif hasattr(argument, "timespan"):
            argument = argument.timespan
        elif hasattr(argument, "_get_timespan"):
            argument = argument._get_timespan()
        start_offset = getattr(argument, "start_offset", None)
        if start_offset is None:
            raise ValueError(argument)
        stop_offset = getattr(argument, "stop_offset", None)
        return start_offset, stop_offset

    def _get_timespan(self, argument):
        if isinstance(argument, Timespan):
            start_offset, stop_offset = argument.offsets
        elif hasattr(argument, "timespan"):
            start_offset, stop_offset = argument.timespan.offsets
        elif hasattr(argument, "_get_timespan"):
            start_offset, stop_offset = argument._get_timespan().offsets
        else:
            raise ValueError(argument)
        return dataclasses.replace(
            self, start_offset=start_offset, stop_offset=stop_offset
        )

    @staticmethod
    def _implements_timespan_interface(timespan):
        if (
            getattr(timespan, "start_offset", "foo") != "foo"
            and getattr(timespan, "stop_offset", "foo") != "foo"
        ):
            return True
        if hasattr(timespan, "_get_timespan"):
            return True
        if getattr(timespan, "timespan", "foo") != "foo":
            return True
        return False

    def _initialize_offset(self, offset):
        if offset in (negative_infinity, infinity):
            return offset
        return _duration.Offset(offset)

    ### PUBLIC PROPERTIES ###

    @property
    def axis(self) -> _duration.Offset:
        """
        Gets arithmetic mean of timespan start- and stop-offsets.

        ..  container:: example

            >>> abjad.Timespan(0, 10).axis
            Offset((5, 1))

        """
        return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration of timespan.

        ..  container:: example

            >>> abjad.Timespan(0, 10).duration
            Duration(10, 1)

        """
        return self.stop_offset - self.start_offset

    @property
    def offsets(self) -> tuple[_duration.Offset, _duration.Offset]:
        """
        Gets offsets.

        ..  container:: example

            >>> abjad.Timespan(0, 10).offsets
            (Offset((0, 1)), Offset((10, 1)))

        """
        return self.start_offset, self.stop_offset

    @property
    def wellformed(self) -> bool:
        """
        Is true when timespan start offset preceeds timespan stop offset.

        ..  container:: example

            >>> abjad.Timespan(0, 10).wellformed
            True

        """
        return self.start_offset < self.stop_offset

    ### PUBLIC METHODS ###

    def divide_by_ratio(self, ratio) -> tuple["Timespan", ...]:
        """
        Divides timespan by ``ratio``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> for x in timespan.divide_by_ratio((1, 2, 1)):
            ...     x
            ...
            Timespan(Offset((1, 2)), Offset((3, 4)))
            Timespan(Offset((3, 4)), Offset((5, 4)))
            Timespan(Offset((5, 4)), Offset((3, 2)))

        """
        if isinstance(ratio, int):
            ratio = ratio * (1,)
        unit_duration = self.duration / sum(ratio)
        part_durations = [numerator * unit_duration for numerator in ratio]
        start_offsets = _math.cumulative_sums(
            [self.start_offset] + part_durations, start=None
        )
        offset_pairs = _sequence.nwise(start_offsets)
        result = [type(self)(*offset_pair) for offset_pair in offset_pairs]
        return tuple(result)

    def get_overlap_with_timespan(self, timespan) -> _duration.Duration | None:
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

        """
        if self._implements_timespan_interface(timespan):
            result = _duration.Duration(sum(x.duration for x in self & timespan))
            return result
        return None

    def reflect(self, axis=None) -> "Timespan":
        """
        Reflects timespan about ``axis``.

        ..  container:: example

            Reverse timespan about timespan axis:

            >>> abjad.Timespan(3, 6).reflect()
            Timespan(Offset((3, 1)), Offset((6, 1)))

        ..  container:: example

            Reverse timespan about arbitrary axis:

            >>> abjad.Timespan(3, 6).reflect(axis=abjad.Offset(10))
            Timespan(Offset((14, 1)), Offset((17, 1)))

        """
        if axis is None:
            axis = self.axis
        start_distance = self.start_offset - axis
        stop_distance = self.stop_offset - axis
        new_start_offset = axis - stop_distance
        new_stop_offset = axis - start_distance
        return self.set_offsets(new_start_offset, new_stop_offset)

    def round_offsets(
        self, multiplier, anchor=_enums.LEFT, must_be_wellformed=True
    ) -> "Timespan":
        """
        Rounds timespan offsets to multiple of ``multiplier``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 5), (4, 5))

            >>> timespan.round_offsets(1)
            Timespan(Offset((0, 1)), Offset((1, 1)))

            >>> timespan.round_offsets(2)
            Timespan(Offset((0, 1)), Offset((2, 1)))

            >>> timespan.round_offsets(2, anchor=abjad.RIGHT)
            Timespan(Offset((-2, 1)), Offset((0, 1)))

            >>> timespan.round_offsets(
            ...     2, anchor=abjad.RIGHT, must_be_wellformed=False
            ... )
            Timespan(Offset((0, 1)), Offset((0, 1)))

        """
        multiplier = abs(fractions.Fraction(multiplier))
        assert 0 < multiplier
        new_start_offset = _duration.Offset(
            int(round(self.start_offset / multiplier)) * multiplier
        )
        new_stop_offset = _duration.Offset(
            int(round(self.stop_offset / multiplier)) * multiplier
        )
        if (new_start_offset == new_stop_offset) and must_be_wellformed:
            if anchor is _enums.LEFT:
                new_stop_offset = new_stop_offset + multiplier
            else:
                new_start_offset = new_start_offset - multiplier
        result = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return result

    def scale(self, multiplier, anchor=_enums.LEFT) -> "Timespan":
        """
        Scales timespan by ``multiplier``.

        ..  container:: example

            >>> timespan = abjad.Timespan(3, 6)

        ..  container:: example

            Scale timespan relative to timespan start offset:

            >>> timespan.scale(abjad.Fraction(2))
            Timespan(Offset((3, 1)), Offset((9, 1)))

        ..  container:: example

            Scale timespan relative to timespan stop offset:

            >>> timespan.scale(abjad.Fraction(2), anchor=abjad.RIGHT)
            Timespan(Offset((0, 1)), Offset((6, 1)))

        """
        multiplier = fractions.Fraction(multiplier)
        assert 0 < multiplier
        new_duration = multiplier * self.duration
        if anchor == _enums.LEFT:
            new_start_offset = self.start_offset
            new_stop_offset = self.start_offset + new_duration
        elif anchor == _enums.RIGHT:
            new_stop_offset = self.stop_offset
            new_start_offset = self.stop_offset - new_duration
        else:
            raise ValueError(f"unknown anchor direction: {anchor!r}.")
        result = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return result

    def set_duration(self, duration) -> "Timespan":
        """
        Sets timespan duration to ``duration``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.set_duration((3, 5))
            Timespan(Offset((1, 2)), Offset((11, 10)))

        """
        duration = _duration.Duration(duration)
        new_stop_offset = self.start_offset + duration
        return dataclasses.replace(self, stop_offset=new_stop_offset)

    def set_offsets(self, start_offset=None, stop_offset=None) -> "Timespan":
        """
        Sets timespan start offset to ``start_offset`` and
        stop offset to ``stop_offset``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.set_offsets(stop_offset=(7, 8))
            Timespan(Offset((1, 2)), Offset((7, 8)))

        Subtracts negative ``start_offset`` from existing stop offset:

        >>> timespan.set_offsets(start_offset=(-1, 2))
        Timespan(Offset((1, 1)), Offset((3, 2)))

        Subtracts negative ``stop_offset`` from existing stop offset:

        >>> timespan.set_offsets(stop_offset=(-1, 2))
        Timespan(Offset((1, 2)), Offset((1, 1)))

        """
        if start_offset is not None:
            start_offset = _duration.Offset(start_offset)
        if stop_offset is not None:
            stop_offset = _duration.Offset(stop_offset)
        if start_offset is not None and 0 <= start_offset:
            new_start_offset = start_offset
        elif start_offset is not None and start_offset < 0:
            new_start_offset = self.stop_offset + _duration.Offset(start_offset)
        else:
            new_start_offset = self.start_offset
        if stop_offset is not None and 0 <= stop_offset:
            new_stop_offset = stop_offset
        elif stop_offset is not None and stop_offset < 0:
            new_stop_offset = self.stop_offset + _duration.Offset(stop_offset)
        else:
            new_stop_offset = self.stop_offset
        result = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return result

    def split_at_offset(self, offset) -> "TimespanList":
        """
        Split into two parts when ``offset`` happens during timespan.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 5)

            >>> left, right = timespan.split_at_offset((2, 1))

            >>> left
            Timespan(Offset((0, 1)), Offset((2, 1)))

            >>> right
            Timespan(Offset((2, 1)), Offset((5, 1)))

            Otherwise return a copy of timespan:

            >>> timespan.split_at_offset((12, 1))[0]
            Timespan(Offset((0, 1)), Offset((5, 1)))

        """
        offset = _duration.Offset(offset)
        result = TimespanList()
        if self.start_offset < offset < self.stop_offset:
            left = dataclasses.replace(
                self, start_offset=self.start_offset, stop_offset=offset
            )
            right = dataclasses.replace(
                self, start_offset=offset, stop_offset=self.stop_offset
            )
            result.append(left)
            result.append(right)
        else:
            result.append(dataclasses.replace(self))
        return result

    def split_at_offsets(self, offsets) -> "TimespanList":
        """
        Split into one or more parts when ``offsets`` happens during timespan.

        ..  container:: example

            >>> timespan = abjad.Timespan(0, 10)

            >>> timespans = timespan.split_at_offsets((1, 3, 7))
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((1, 1)))
            Timespan(Offset((1, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((7, 1)))
            Timespan(Offset((7, 1)), Offset((10, 1)))

            Otherwise return a timespan list containing a copy of timespan:

            >>> timespans = timespan.split_at_offsets((-100,))
            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((10, 1)))

        """
        offsets = [_duration.Offset(offset) for offset in offsets]
        offsets = [
            offset
            for offset in offsets
            if self.start_offset < offset < self.stop_offset
        ]
        offsets = sorted(set(offsets))
        result = TimespanList()
        right = dataclasses.replace(self)
        for offset in offsets:
            left, right = right.split_at_offset(offset)
            result.append(left)
        result.append(right)
        return result

    def stretch(self, multiplier, anchor=None) -> "Timespan":
        """
        Stretches timespan by ``multiplier`` relative to ``anchor``.

        .. container:: example

            Stretch relative to timespan start offset:

            >>> abjad.Timespan(3, 10).stretch(abjad.Fraction(2))
            Timespan(Offset((3, 1)), Offset((17, 1)))

        .. container:: example

            Stretch relative to timespan stop offset:

            >>> abjad.Timespan(3, 10).stretch(abjad.Fraction(2), abjad.Offset(10))
            Timespan(Offset((-4, 1)), Offset((10, 1)))

        .. container:: example

            Stretch relative to offset prior to timespan:

            >>> abjad.Timespan(3, 10).stretch(abjad.Fraction(2), abjad.Offset(0, 1))
            Timespan(Offset((6, 1)), Offset((20, 1)))

        .. container:: example

            Stretch relative to offset after timespan:

            >>> abjad.Timespan(3, 10).stretch(abjad.Fraction(3), abjad.Offset(12))
            Timespan(Offset((-15, 1)), Offset((6, 1)))

        .. container:: example

            Stretch relative to offset that happens during timespan:

            >>> abjad.Timespan(3, 10).stretch(abjad.Fraction(2), abjad.Offset(4))
            Timespan(Offset((2, 1)), Offset((16, 1)))

        """
        multiplier = fractions.Fraction(multiplier)
        assert 0 < multiplier
        if anchor is None:
            anchor = self.start_offset
        new_start_offset = (multiplier * (self.start_offset - anchor)) + anchor
        new_stop_offset = (multiplier * (self.stop_offset - anchor)) + anchor
        result = dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )
        return result

    def translate(self, translation=None) -> "Timespan":
        """
        Translates timespan by ``translation``.

        ..  container:: example

            >>> timespan = abjad.Timespan(5, 10)

            >>> timespan.translate(2)
            Timespan(Offset((7, 1)), Offset((12, 1)))

        """
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self, start_offset_translation=None, stop_offset_translation=None
    ) -> "Timespan":
        """
        Translates timespan start offset by ``start_offset_translation`` and
        stop offset by ``stop_offset_translation``.

        ..  container:: example

            >>> timespan = abjad.Timespan((1, 2), (3, 2))

            >>> timespan.translate_offsets(start_offset_translation=(-1, 8))
            Timespan(Offset((3, 8)), Offset((3, 2)))

        """
        start_offset_translation = start_offset_translation or 0
        stop_offset_translation = stop_offset_translation or 0
        start_offset_translation = _duration.Duration(start_offset_translation)
        stop_offset_translation = _duration.Duration(stop_offset_translation)
        new_start_offset = self.start_offset + start_offset_translation
        new_stop_offset = self.stop_offset + stop_offset_translation
        return dataclasses.replace(
            self, start_offset=new_start_offset, stop_offset=new_stop_offset
        )


@dataclasses.dataclass(slots=True)
class TimespanList(list):
    """
    Timespan list.

    ..  container:: example

        Contiguous timespan list:

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 3),
        ...     abjad.Timespan(3, 6),
        ...     abjad.Timespan(6, 10),
        ... ])
        >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        >>> for _ in timespans: _
        Timespan(Offset((0, 1)), Offset((3, 1)))
        Timespan(Offset((3, 1)), Offset((6, 1)))
        Timespan(Offset((6, 1)), Offset((10, 1)))

    ..  container:: example

        Overlapping timespan list:

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 16),
        ...     abjad.Timespan(5, 12),
        ...     abjad.Timespan(-2, 8),
        ...     abjad.Timespan(15, 20),
        ...     abjad.Timespan(24, 30),
        ... ])
        >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        >>> for _ in timespans: _
        Timespan(Offset((0, 1)), Offset((16, 1)))
        Timespan(Offset((5, 1)), Offset((12, 1)))
        Timespan(Offset((-2, 1)), Offset((8, 1)))
        Timespan(Offset((15, 1)), Offset((20, 1)))
        Timespan(Offset((24, 1)), Offset((30, 1)))

    ..  container:: example

        Empty timespan list:

        >>> abjad.TimespanList()
        TimespanList([])

    ..  container:: example

        Coerces input:

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, (1, 2)),
        ...     ((1, 2), (3, 4)),
        ...     abjad.Timespan((3, 4), 1),
        ... ])

        >>> for _ in timespans: _
        Timespan(Offset((0, 1)), Offset((1, 2)))
        Timespan(Offset((1, 2)), Offset((3, 4)))
        Timespan(Offset((3, 4)), Offset((1, 1)))


    Operations on timespan currently work in place.
    """

    __documentation_section__ = "Timespans"

    def __init__(self, argument=()):
        timespans = [self._coerce_item(_) for _ in argument]
        list.__init__(self, timespans)

    def __setitem__(self, i, argument):
        """
        Coerces ``argument`` and sets at ``i``.
        """
        if isinstance(i, int):
            item = self._coerce_item(argument)
            list.__setitem__(self, i, item)
        elif isinstance(i, slice):
            items = [self._coerce_item(_) for _ in argument]
            list.__setitem__(self, i, items)

    def append(self, item):
        """
        Coerces ``item`` and appends.
        """
        item = self._coerce_item(item)
        list.append(self, item)

    def extend(self, items):
        """
        Coerces ``items`` and extends.
        """
        items = [self._coerce_item(_) for _ in items]
        list.extend(self, items)

    def remove(self, item):
        """
        Coerces ``item`` and removes.
        """
        item = self._coerce_item(item)
        list.remove(self, item)

    def __and__(self, timespan) -> "TimespanList":
        """
        Keeps material that intersects ``timespan``.

        ..  container:: example

            Keeps material that intersects timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ... ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(5, 10)
            >>> timespans = timespans & timespan
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((8, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))

        """
        new_timespans: list[Timespan] = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}({list(self)})"

    def _make_markup(
        self,
        key=None,
        range_=None,
        sort_callable=None,
        sortkey=None,
        scale=None,
    ) -> _indicators.Markup:
        r"""
        Makes markup.

        ..  container:: example

            Illustrates timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan_operand = abjad.Timespan(6, 10)
            >>> timespans = timespans - timespan_operand
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = abjad.illustrate(timespans)
                >>> markup = lilypond_file.items[-1]
                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup \column {
                \overlay {
                \translate #'(1.0 . 1)
                \sans \fontsize #-3 \center-align \fraction -2 1
                \translate #'(17.666666666666668 . 1)
                \sans \fontsize #-3 \center-align \fraction 0 1
                \translate #'(59.33333333333334 . 1)
                \sans \fontsize #-3 \center-align \fraction 5 1
                \translate #'(67.66666666666667 . 1)
                \sans \fontsize #-3 \center-align \fraction 6 1
                \translate #'(101.00000000000001 . 1)
                \sans \fontsize #-3 \center-align \fraction 10 1
                \translate #'(117.66666666666667 . 1)
                \sans \fontsize #-3 \center-align \fraction 12 1
                \translate #'(151.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 16 1
                }
                \pad-to-box #'(0 . 82.33333333333333) #'(0 . 8.5)
                \postscript #"
                0.2 setlinewidth
                1 6.5 moveto
                67.66666666666667 6.5 lineto
                stroke
                1 7.25 moveto
                1 5.75 lineto
                stroke
                67.66666666666667 7.25 moveto
                67.66666666666667 5.75 lineto
                stroke
                17.666666666666668 3.5 moveto
                67.66666666666667 3.5 lineto
                stroke
                17.666666666666668 4.25 moveto
                17.666666666666668 2.75 lineto
                stroke
                67.66666666666667 4.25 moveto
                67.66666666666667 2.75 lineto
                stroke
                101.00000000000001 3.5 moveto
                151 3.5 lineto
                stroke
                101.00000000000001 4.25 moveto
                101.00000000000001 2.75 lineto
                stroke
                151 4.25 moveto
                151 2.75 lineto
                stroke
                59.33333333333334 0.5 moveto
                67.66666666666667 0.5 lineto
                stroke
                59.33333333333334 1.25 moveto
                59.33333333333334 -0.25 lineto
                stroke
                67.66666666666667 1.25 moveto
                67.66666666666667 -0.25 lineto
                stroke
                101.00000000000001 0.5 moveto
                117.66666666666667 0.5 lineto
                stroke
                101.00000000000001 1.25 moveto
                101.00000000000001 -0.25 lineto
                stroke
                117.66666666666667 1.25 moveto
                117.66666666666667 -0.25 lineto
                stroke
                0.1 setlinewidth
                [ 0.1 0.2 ] 0 setdash
                1 8.5 moveto
                1 7 lineto
                stroke
                17.666666666666668 8.5 moveto
                17.666666666666668 4 lineto
                stroke
                59.33333333333334 8.5 moveto
                59.33333333333334 1 lineto
                stroke
                67.66666666666667 8.5 moveto
                67.66666666666667 1 lineto
                stroke
                101.00000000000001 8.5 moveto
                101.00000000000001 1 lineto
                stroke
                117.66666666666667 8.5 moveto
                117.66666666666667 1 lineto
                stroke
                151 8.5 moveto
                151 4 lineto
                stroke
                0 0 moveto
                0.99 setgray
                0 0.01 rlineto
                stroke"
                }

        ..  container:: example

            Set ``key`` and ``sort_callable`` together like this to customize timespan
            sorting:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, (1, 4), annotation="voice 1"),
            ...     abjad.Timespan(0, (1, 4), annotation="voice 2"),
            ...     abjad.Timespan(0, (1, 4), annotation="voice 10"),
            ... ])

            >>> def to_digit(string):
            ...     return int(string) if string.isdigit() else string

            >>> def human_sorted_keys(pair):
            ...     key, timespan = pair
            ...     values = [to_digit(_) for _ in key.split()]
            ...     hashable_key = tuple(values)
            ...     return hashable_key

            >>> abjad.show(
            ...     timespans,
            ...     key="annotation",
            ...     sort_callable=human_sorted_keys,
            ...     scale=0.5,
            ... ) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = abjad.illustrate(
                ...     timespans,
                ...     key="annotation",
                ...     sort_callable=human_sorted_keys,
                ... )
                >>> markup = lilypond_file.items[-1]
                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup
                \left-column {
                \fontsize #-1 \sans \line { "voice 1:" }
                \vspace #0.5
                \column {
                \overlay {
                \translate #'(1.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 0 1
                \translate #'(151.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 1 4
                }
                \pad-to-box #'(0 . 149.0) #'(0 . 2.5)
                \postscript #"
                0.2 setlinewidth
                1 0.5 moveto
                151 0.5 lineto
                stroke
                1 1.25 moveto
                1 -0.25 lineto
                stroke
                151 1.25 moveto
                151 -0.25 lineto
                stroke
                0.1 setlinewidth
                [ 0.1 0.2 ] 0 setdash
                1 2.5 moveto
                1 1 lineto
                stroke
                151 2.5 moveto
                151 1 lineto
                stroke
                0 0 moveto
                0.99 setgray
                0 0.01 rlineto
                stroke"
                }
                \vspace #0.5
                \fontsize #-1 \sans \line { "voice 2:" }
                \vspace #0.5
                \column {
                \overlay {
                \translate #'(1.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 0 1
                \translate #'(151.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 1 4
                }
                \pad-to-box #'(0 . 149.0) #'(0 . 2.5)
                \postscript #"
                0.2 setlinewidth
                1 0.5 moveto
                151 0.5 lineto
                stroke
                1 1.25 moveto
                1 -0.25 lineto
                stroke
                151 1.25 moveto
                151 -0.25 lineto
                stroke
                0.1 setlinewidth
                [ 0.1 0.2 ] 0 setdash
                1 2.5 moveto
                1 1 lineto
                stroke
                151 2.5 moveto
                151 1 lineto
                stroke
                0 0 moveto
                0.99 setgray
                0 0.01 rlineto
                stroke"
                }
                \vspace #0.5
                \fontsize #-1 \sans \line { "voice 10:" }
                \vspace #0.5
                \column {
                \overlay {
                \translate #'(1.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 0 1
                \translate #'(151.0 . 1)
                \sans \fontsize #-3 \center-align \fraction 1 4
                }
                \pad-to-box #'(0 . 149.0) #'(0 . 2.5)
                \postscript #"
                0.2 setlinewidth
                1 0.5 moveto
                151 0.5 lineto
                stroke
                1 1.25 moveto
                1 -0.25 lineto
                stroke
                151 1.25 moveto
                151 -0.25 lineto
                stroke
                0.1 setlinewidth
                [ 0.1 0.2 ] 0 setdash
                1 2.5 moveto
                1 1 lineto
                stroke
                151 2.5 moveto
                151 1 lineto
                stroke
                0 0 moveto
                0.99 setgray
                0 0.01 rlineto
                stroke"
                }
                }

        """
        if not self:
            return _indicators.Markup(r"\markup \null")
        maximum: _duration.Offset | _math.Infinity
        minimum: _duration.Offset | _math.NegativeInfinity
        if isinstance(range_, Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = self.start_offset, self.stop_offset
        if scale is None:
            scale = 1.0
        assert 0 < scale
        minimum_float = float(_duration.Offset(minimum))
        maximum_float = float(_duration.Offset(maximum))
        postscript_scale = 150.0 / (maximum_float - minimum_float)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum_float * postscript_scale) - 1
        if key is None:
            string = _make_timespan_list_markup(
                self, postscript_x_offset, postscript_scale, sortkey=sortkey
            )
            markup = _indicators.Markup(rf"\markup {string}")
        else:
            timespan_lists = {}
            for timespan in self:
                value = getattr(timespan, key)
                if value not in timespan_lists:
                    timespan_lists[value] = type(self)()
                timespan_lists[value].append(timespan)
            strings = []
            generator = sorted(timespan_lists.items(), key=sort_callable)
            for i, item in enumerate(generator):
                value, timespans = item
                timespans.sort()
                if 0 < i:
                    string = r"\vspace #0.5"
                    strings.append(string)
                string = rf'\fontsize #-1 \sans \line {{ "{value}:" }}'
                strings.append(string)
                string = r"\vspace #0.5"
                strings.append(string)
                string = _make_timespan_list_markup(
                    timespans,
                    postscript_x_offset,
                    postscript_scale,
                    sortkey=sortkey,
                )
                strings.append(string)
            string = "\n".join(strings)
            markup = _indicators.Markup(f"\\markup\n\\left-column {{\n{string}\n}}")
        return markup

    def __invert__(self) -> "TimespanList":
        """
        Inverts timespans.

        ..  container:: example

            Inverts timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(~timespans, range_=(-2, 30), scale=0.5) # doctest: +SKIP

            >>> for _ in ~timespans: _
            Timespan(Offset((8, 1)), Offset((15, 1)))
            Timespan(Offset((20, 1)), Offset((24, 1)))

        ..  container:: example

            Inverts contiguous timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> ~timespans
            TimespanList([])

        """
        result = type(self)()
        result.append(self.timespan)
        for timespan in self:
            result = result - timespan
        return result

    def __sub__(self, timespan) -> "TimespanList":
        """
        Deletes material that intersects ``timespan``.

        ..  container:: example

            Deletes material that intersects timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(5, 10)
            >>> timespans = timespans - timespan

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((5, 1)))
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((10, 1)), Offset((12, 1)))
            Timespan(Offset((10, 1)), Offset((16, 1)))


            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        """
        new_timespans: list[Timespan] = []
        for current_timespan in self[:]:
            result = current_timespan - timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    @staticmethod
    def _coerce_item(item):
        if Timespan._implements_timespan_interface(item):
            return item
        elif isinstance(item, Timespan):
            return item
        elif isinstance(item, tuple) and len(item) == 2:
            return Timespan(*item)
        else:
            return Timespan(item)

    @staticmethod
    def _get_offsets(argument):
        try:
            return argument.start_offset, argument.stop_offset
        except AttributeError:
            pass
        try:
            return argument.timespan.offsets
        except AttributeError:
            pass
        raise TypeError(argument)

    @staticmethod
    def _get_timespan(argument):
        start_offset, stop_offset = Timespan._get_offsets(argument)
        return Timespan(start_offset, stop_offset)

    @property
    def all_are_contiguous(self) -> bool:
        """
        Is true when all timespans are contiguous.

        ..  container:: example

            Is true when all timespans are contiguous:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_contiguous
            True

        ..  container:: example

            Is false when timespans not contiguous:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_contiguous
            False

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_contiguous
            True

        """
        if len(self) <= 1:
            return True
        timespans = sorted(self[:])
        last_stop_offset = timespans[0].stop_offset
        for timespan in timespans[1:]:
            if timespan.start_offset != last_stop_offset:
                return False
            last_stop_offset = timespan.stop_offset
        return True

    @property
    def all_are_nonoverlapping(self) -> bool:
        """
        Is true when all timespans are nonoverlapping.

        ..  container:: example

            Is true when all timespans are nonoverlapping:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_nonoverlapping
            True

        ..  container:: example

            Is false when timespans are overlapping:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_nonoverlapping
            False

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_nonoverlapping
            True

        """
        if len(self) <= 1:
            return True
        timespans = sorted(self[:])
        last_stop_offset = timespans[0].stop_offset
        for timespan in timespans[1:]:
            if timespan.start_offset < last_stop_offset:
                return False
            if last_stop_offset < timespan.stop_offset:
                last_stop_offset = timespan.stop_offset
        return True

    @property
    def all_are_wellformed(self) -> bool:
        """
        Is true when all timespans are wellformed.

        ..  container:: example

            Is true when all timespans are wellformed:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_wellformed
            True

        ..  container:: example

            Is true when all timespans are wellformed:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_wellformed
            True

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_wellformed
            True

        Is false when timespans are not all wellformed.
        """
        return all(self._get_timespan(argument).wellformed for argument in self)

    @property
    def axis(self) -> _duration.Offset | None:
        """
        Gets axis defined equal to arithmetic mean of start- and stop-offsets.

        ..  container:: example

            Gets axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.axis
            Offset((5, 1))

        ..  container:: example

            Gets axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.axis
            Offset((14, 1))

        ..  container:: example

            Gets none when timespan list is empty:

            >>> abjad.TimespanList().axis is None
            True

        """
        if self:
            assert isinstance(self.start_offset, _duration.Offset)
            assert isinstance(self.stop_offset, _duration.Offset)
            return (self.start_offset + self.stop_offset) / 2
        return None

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration of timespan list.

        ..  container:: example

            Gets duration:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.duration
            Duration(10, 1)

        ..  container:: example

            Gets duration:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.duration
            Duration(32, 1)

        ..  container:: example

            Gets zero when timespan list is empty:

            >>> abjad.TimespanList().duration
            Duration(0, 1)

        """
        if self.stop_offset != infinity and self.start_offset != negative_infinity:
            return self.stop_offset - self.start_offset
        else:
            return _duration.Duration(0)

    @property
    def is_sorted(self) -> bool:
        """
        Is true when timespans are in time order.

        ..  container:: example

            Is true when timespans are sorted:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.is_sorted
            True

        ..  container:: example

            Is false when timespans are not sorted:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(6, 10),
            ...     abjad.Timespan(3, 6),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.is_sorted
            False

        """
        if len(self) < 2:
            return True
        pairs = _sequence.nwise(self)
        for left_timespan, right_timespan in pairs:
            if right_timespan.start_offset < left_timespan.start_offset:
                return False
            if left_timespan.start_offset == right_timespan.start_offset:
                if right_timespan.stop_offset < left_timespan.stop_offset:
                    return False
        return True

    @property
    def start_offset(self) -> _duration.Offset | _math.NegativeInfinity:
        """
        Gets start offset.

        Defined equal to earliest start offset of any timespan in list.

        ..  container:: example

            Gets start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.start_offset
            Offset((0, 1))

        ..  container:: example

            Gets start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.start_offset
            Offset((-2, 1))

        ..  container:: example

            Gets negative infinity when timespan list is empty:

            >>> abjad.TimespanList().start_offset
            NegativeInfinity()

        """
        if self:
            return min([self._get_timespan(argument).start_offset for argument in self])
        else:
            return negative_infinity

    @property
    def stop_offset(self) -> _duration.Offset | _math.Infinity:
        """
        Gets stop offset.

        Defined equal to latest stop offset of any timespan.

        ..  container:: example

            Gets stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.stop_offset
            Offset((10, 1))

        ..  container:: example

            Gets stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.stop_offset
            Offset((30, 1))

        ..  container:: example


            Gets infinity when timespan list is empty:

            >>> abjad.TimespanList().stop_offset
            Infinity()

        """
        if self:
            return max([self._get_timespan(argument).stop_offset for argument in self])
        else:
            return infinity

    @property
    def timespan(self):
        """
        Gets timespan of timespan list.

        ..  container:: example

            Gets timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(timespans.timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> timespans.timespan
            Timespan(Offset((0, 1)), Offset((10, 1)))

        ..  container:: example

            Gets timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(timespans.timespan, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> timespans.timespan
            Timespan(Offset((-2, 1)), Offset((30, 1)))

        ..  container:: example

            Gets infinite timespan when list is empty:

            >>> abjad.TimespanList().timespan
            Timespan(NegativeInfinity(), Infinity())

        Returns timespan.
        """
        return Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def clip_timespan_durations(
        self, minimum=None, maximum=None, anchor=_enums.LEFT
    ) -> "TimespanList":
        """
        Clips timespan durations.

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.clip_timespan_durations(minimum=5)
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((0, 1)), Offset((10, 1)))

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.clip_timespan_durations(maximum=5)
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((1, 1)))
            Timespan(Offset((0, 1)), Offset((5, 1)))

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.clip_timespan_durations(
            ...     minimum=3,
            ...     maximum=7,
            ... )
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((0, 1)), Offset((7, 1)))

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.clip_timespan_durations(
            ...     minimum=3,
            ...     maximum=7,
            ...     anchor=abjad.RIGHT,
            ... )
            >>> abjad.show(timespans, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((1, 1)))
            Timespan(Offset((3, 1)), Offset((10, 1)))


        """
        assert anchor in (_enums.LEFT, _enums.RIGHT)
        if minimum is not None:
            minimum = _duration.Duration(minimum)
        if maximum is not None:
            maximum = _duration.Duration(maximum)
        if minimum is not None and maximum is not None:
            assert minimum <= maximum
        timespans = type(self)()
        for timespan in self:
            if minimum is not None and timespan.duration < minimum:
                if anchor is _enums.LEFT:
                    new_timespan = timespan.set_duration(minimum)
                else:
                    new_start_offset = timespan.stop_offset - minimum
                    new_timespan = dataclasses.replace(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                    )
            elif maximum is not None and maximum < timespan.duration:
                if anchor is _enums.LEFT:
                    new_timespan = timespan.set_duration(maximum)
                else:
                    new_start_offset = timespan.stop_offset - maximum
                    new_timespan = dataclasses.replace(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                    )
            else:
                new_timespan = timespan
            timespans.append(new_timespan)
        return timespans

    def compute_logical_and(self) -> "TimespanList":
        """
        Computes logical AND of timespans.

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((10, 1)))

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((10, 1)))

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ... ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((8, 1)))

        Same as setwise intersection.

        Operates in place and returns timespan list.
        """
        if 1 < len(self):
            result = self[0]
            for timespan in self:
                if not bool(timespan & result):
                    self[:] = []
                    return self
                else:
                    timespans = result & timespan
                    result = timespans[0]
            self[:] = [result]
        return self

    def compute_logical_or(self) -> "TimespanList":
        """
        Computes logical OR of timespans.

        ..  container:: example

            >>> timespans = abjad.TimespanList()
            >>> timespans = timespans.compute_logical_or()

            >>> timespans
            TimespanList([])

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((10, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((12, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 2),
            ... ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((12, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 2),
            ...     abjad.Timespan(10, 20),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((10, 1)), Offset((20, 1)))

        Operates in place and returns timespan list.
        """
        timespans: list[Timespan] = []
        if self:
            timespans = [self[0]]
            for timespan in self[1:]:
                if timespans[-1]._can_fuse(timespan):
                    timespans_ = timespans[-1] | timespan
                    timespans[-1:] = timespans_[:]
                else:
                    timespans.append(timespan)
        self[:] = timespans
        return self

    def compute_logical_xor(self) -> "TimespanList":
        """
        Computes logical XOR of timespans.

        ..  container:: example

            >>> timespans = abjad.TimespanList()
            >>> timespans = timespans.compute_logical_xor()

            >>> timespans
            TimespanList([])

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((10, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ... ])
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((10, 1)), Offset((12, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 2),
            ... ])
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((0, 1)))
            Timespan(Offset((2, 1)), Offset((5, 1)))
            Timespan(Offset((10, 1)), Offset((12, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 2),
            ...     abjad.Timespan(10, 20),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-2, 1)), Offset((2, 1)))
            Timespan(Offset((10, 1)), Offset((20, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(4, 8),
            ...     abjad.Timespan(2, 6),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((2, 1)))
            Timespan(Offset((8, 1)), Offset((10, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(0, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.compute_logical_xor()

            >>> timespans
            TimespanList([])

        Operates in place and returns timespan list.
        """
        all_fragments = []
        for i, timespan_1 in enumerate(self):
            timespan_1_fragments = [timespan_1]
            for j, timespan_2 in enumerate(self):
                if i == j:
                    continue
                revised_timespan_1_fragments: list[Timespan] = []
                for timespan_1_fragment in timespan_1_fragments:
                    if bool(timespan_2 & timespan_1_fragment):
                        result = timespan_1_fragment - timespan_2
                        revised_timespan_1_fragments.extend(result)
                    else:
                        revised_timespan_1_fragments.append(timespan_1_fragment)
                timespan_1_fragments = revised_timespan_1_fragments
            all_fragments.extend(timespan_1_fragments)
        self[:] = all_fragments
        self.sort()
        return self

    def compute_overlap_factor(self, timespan=None) -> fractions.Fraction:
        """
        Computes overlap factor of timespans.

        ..  container:: example

            Example timespan list:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 15),
            ...     abjad.Timespan(20, 25),
            ...     abjad.Timespan(20, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Computes overlap factor across the entire list:

            >>> timespans.compute_overlap_factor()
            Fraction(7, 6)

        ..  container:: example

            Computes overlap factor within a specific timespan:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(-15, 0))
            Fraction(0, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(timespan=abjad.Timespan(-10, 5))
            Fraction(1, 3)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(-5, 10))
            Fraction(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(0, 15))
            Fraction(4, 3)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(5, 20))
            Fraction(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(10, 25))
            Fraction(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(15, 30))
            Fraction(1, 1)

        """
        if timespan is None:
            timespan = self.timespan
        timespans = self.get_timespans_that_satisfy_time_relation(
            lambda _: bool(_ & timespan)
        )
        total_overlap = _duration.Duration(
            sum(x.get_overlap_with_timespan(timespan) for x in timespans)
        )
        overlap_factor = fractions.Fraction(total_overlap / timespan.duration)
        return overlap_factor

    def compute_overlap_factor_mapping(self) -> dict:
        """
        Computes overlap factor for each consecutive offset pair in timespans.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 15),
            ...     abjad.Timespan(20, 25),
            ...     abjad.Timespan(20, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> mapping = timespans.compute_overlap_factor_mapping()
            >>> for timespan, overlap_factor in mapping.items():
            ...     timespan.start_offset, timespan.stop_offset, overlap_factor
            ...
            (Offset((0, 1)), Offset((5, 1)), Fraction(1, 1))
            (Offset((5, 1)), Offset((10, 1)), Fraction(2, 1))
            (Offset((10, 1)), Offset((15, 1)), Fraction(1, 1))
            (Offset((15, 1)), Offset((20, 1)), Fraction(0, 1))
            (Offset((20, 1)), Offset((25, 1)), Fraction(2, 1))
            (Offset((25, 1)), Offset((30, 1)), Fraction(1, 1))

        Returns mapping.
        """
        mapping: dict = dict()
        offsets = list(sorted(self.count_offsets().items))
        for start_offset, stop_offset in _sequence.nwise(offsets):
            timespan = Timespan(start_offset, stop_offset)
            overlap_factor = self.compute_overlap_factor(timespan=timespan)
            mapping[timespan] = overlap_factor
        return mapping

    def count_offsets(self):
        """
        Counts offsets.

        ..  container:: example

            Counts offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items.items()):
            ...     offset, count
            ...
            (Offset((0, 1)), 1)
            (Offset((3, 1)), 2)
            (Offset((6, 1)), 2)
            (Offset((10, 1)), 1)

        ..  container:: example

            Counts offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((16, 1)))
            Timespan(Offset((5, 1)), Offset((12, 1)))
            Timespan(Offset((-2, 1)), Offset((8, 1)))
            Timespan(Offset((15, 1)), Offset((20, 1)))
            Timespan(Offset((24, 1)), Offset((30, 1)))

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items.items()):
            ...     offset, count
            ...
            (Offset((-2, 1)), 1)
            (Offset((0, 1)), 1)
            (Offset((5, 1)), 1)
            (Offset((8, 1)), 1)
            (Offset((12, 1)), 1)
            (Offset((15, 1)), 1)
            (Offset((16, 1)), 1)
            (Offset((20, 1)), 1)
            (Offset((24, 1)), 1)
            (Offset((30, 1)), 1)

        ..  container:: example

            Counts offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(0, 6),
            ...     abjad.Timespan(0, 9),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 9), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items.items()):
            ...     offset, count
            ...
            (Offset((0, 1)), 3)
            (Offset((3, 1)), 1)
            (Offset((6, 1)), 1)
            (Offset((9, 1)), 1)

        Returns counter.
        """
        return OffsetCounter(self)

    def explode(self, inventory_count=None) -> tuple["TimespanList", ...]:
        """
        Explodes timespans into timespan lists, avoiding overlap, and
        distributing density as evenly as possible.

        ..  container:: example

            Example timespan list:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(5, 13),
            ...     abjad.Timespan(6, 10),
            ...     abjad.Timespan(8, 9),
            ...     abjad.Timespan(15, 23),
            ...     abjad.Timespan(16, 21),
            ...     abjad.Timespan(17, 19),
            ...     abjad.Timespan(19, 20),
            ...     abjad.Timespan(25, 30),
            ...     abjad.Timespan(26, 29),
            ...     abjad.Timespan(32, 34),
            ...     abjad.Timespan(34, 37),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Explodes timespans into the optimal number of non-overlapping timespan_lists:

            >>> for exploded_timespan_list in timespans.explode():
            ...     for _ in exploded_timespan_list: _
            ...     "---"
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((5, 1)), Offset((13, 1)))
            Timespan(Offset((17, 1)), Offset((19, 1)))
            Timespan(Offset((19, 1)), Offset((20, 1)))
            Timespan(Offset((34, 1)), Offset((37, 1)))
            '---'
            Timespan(Offset((6, 1)), Offset((10, 1)))
            Timespan(Offset((16, 1)), Offset((21, 1)))
            Timespan(Offset((25, 1)), Offset((30, 1)))
            '---'
            Timespan(Offset((8, 1)), Offset((9, 1)))
            Timespan(Offset((15, 1)), Offset((23, 1)))
            Timespan(Offset((26, 1)), Offset((29, 1)))
            Timespan(Offset((32, 1)), Offset((34, 1)))
            '---'


        ..  container:: example

            Explodes timespans into a less-than-optimal number of overlapping
            timespan_lists:

            >>> for exploded_timespan_list in timespans.explode(inventory_count=6):
            ...     for _ in exploded_timespan_list: _
            ...     "---"
            ...
            Timespan(Offset((16, 1)), Offset((21, 1)))
            Timespan(Offset((34, 1)), Offset((37, 1)))
            '---'
            Timespan(Offset((15, 1)), Offset((23, 1)))
            '---'
            Timespan(Offset((8, 1)), Offset((9, 1)))
            Timespan(Offset((17, 1)), Offset((19, 1)))
            Timespan(Offset((19, 1)), Offset((20, 1)))
            Timespan(Offset((26, 1)), Offset((29, 1)))
            '---'
            Timespan(Offset((6, 1)), Offset((10, 1)))
            Timespan(Offset((32, 1)), Offset((34, 1)))
            '---'
            Timespan(Offset((5, 1)), Offset((13, 1)))
            '---'
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((25, 1)), Offset((30, 1)))
            '---'

        """
        assert isinstance(inventory_count, type(None) | int)
        if isinstance(inventory_count, int):
            assert 0 < inventory_count
        bounding_timespan = self.timespan
        global_overlap_factors = []
        empty_timespans_pairs = []
        result_timespan_lists = []
        if inventory_count is not None:
            for i in range(inventory_count):
                global_overlap_factors.append(0)
                result_timespans = type(self)([])
                empty_timespans_pairs.append((i, result_timespans))
                result_timespan_lists.append(result_timespans)
        for current_timespan in self:
            current_overlap_factor = (
                current_timespan.duration / bounding_timespan.duration
            )
            if empty_timespans_pairs:
                i, empty_timespans = empty_timespans_pairs.pop()
                empty_timespans.append(current_timespan)
                global_overlap_factors[i] = current_overlap_factor
                continue
            nonoverlapping_timespan_lists = []
            overlapping_timespan_lists = []
            for i, result_timespans in enumerate(result_timespan_lists):
                local_overlap_factor = result_timespans.compute_overlap_factor(
                    current_timespan
                )
                global_overlap_factor = global_overlap_factors[i]
                if not local_overlap_factor:
                    nonoverlapping_timespan_lists.append((i, global_overlap_factor))
                else:
                    overlapping_timespan_lists.append(
                        (i, local_overlap_factor, global_overlap_factor)
                    )
            nonoverlapping_timespan_lists.sort(key=lambda x: x[1])
            overlapping_timespan_lists.sort(key=lambda x: (x[1], x[2]))
            if not nonoverlapping_timespan_lists and inventory_count is None:
                result_timespans = type(self)([current_timespan])
                global_overlap_factors.append(current_overlap_factor)
                result_timespan_lists.append(result_timespans)
                continue
            if nonoverlapping_timespan_lists:
                i = nonoverlapping_timespan_lists[0][0]
            else:
                i = overlapping_timespan_lists[0][0]
            result_timespans = result_timespan_lists[i]
            result_timespans.append(current_timespan)
            global_overlap_factors[i] += current_overlap_factor
        return tuple(result_timespan_lists)

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        """
        Gets timespan that satisifies ``time_relation``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 5)
            >>> time_relation = lambda _: timespan.start_offset < _.start_offset < timespan.stop_offset
            >>> timespan = timespans.get_timespan_that_satisfies_time_relation(
            ...     time_relation
            ... )
            >>> abjad.show(timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> timespan
            Timespan(Offset((3, 1)), Offset((6, 1)))

        Returns timespan when timespan list contains exactly one
        timespan that satisfies ``time_relation``.

        Raises exception when timespan list contains no timespan
        that satisfies ``time_relation``.

        Raises exception when timespan list contains more than one
        timespan that satisfies ``time_relation``.
        """
        timespans = self.get_timespans_that_satisfy_time_relation(time_relation)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception("extra timespan.")
        else:
            raise Exception("missing timespan.")

    def get_timespans_that_satisfy_time_relation(self, time_relation) -> "TimespanList":
        """
        Gets timespans that satisfy ``time_relation``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 8)
            >>> time_relation = lambda _: timespan.start_offset < _.start_offset < timespan.stop_offset
            >>> timespans = timespans.get_timespans_that_satisfy_time_relation(
            ...     time_relation)
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))

        """
        result = []
        for timespan in self:
            if time_relation(timespan):
                result.append(timespan)
        return type(self)(result)

    def has_timespan_that_satisfies_time_relation(self, time_relation) -> bool:
        """
        Is true when list has matching timespan.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 8)
            >>> time_relation = lambda _: timespan.start_offset < _.start_offset < timespan.stop_offset
            >>> timespans.has_timespan_that_satisfies_time_relation(time_relation)
            True

            Is false when list does not have matching timespan:

            >>> timespan = abjad.Timespan(10, 20)
            >>> timespans.has_timespan_that_satisfies_time_relation(time_relation)
            False

        """
        return bool(self.get_timespans_that_satisfy_time_relation(time_relation))

    def partition(self, include_tangent_timespans=False) -> tuple["TimespanList", ...]:
        """
        Partitions timespans into timespan lists.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))

            >>> for timespan_list in timespans.partition():
            ...     for _ in timespan_list: _
            ...     "---"
            ...
            Timespan(Offset((0, 1)), Offset((3, 1)))
            '---'
            Timespan(Offset((3, 1)), Offset((6, 1)))
            '---'
            Timespan(Offset((6, 1)), Offset((10, 1)))
            '---'

        ..  container:: example

            Partitions timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((16, 1)))
            Timespan(Offset((5, 1)), Offset((12, 1)))
            Timespan(Offset((-2, 1)), Offset((8, 1)))
            Timespan(Offset((15, 1)), Offset((20, 1)))
            Timespan(Offset((24, 1)), Offset((30, 1)))

            >>> for timespan_list in timespans.partition():
            ...     for _ in timespan_list: _
            ...     "---"
            ...
            Timespan(Offset((-2, 1)), Offset((8, 1)))
            Timespan(Offset((0, 1)), Offset((16, 1)))
            Timespan(Offset((5, 1)), Offset((12, 1)))
            Timespan(Offset((15, 1)), Offset((20, 1)))
            '---'
            Timespan(Offset((24, 1)), Offset((30, 1)))
            '---'

        ..  container:: example

            Treats tangent timespans as part of the same group when
            ``include_tangent_timespans`` is true:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for timespan_list in timespans.partition(
            ...     include_tangent_timespans=True,
            ... ):
            ...     for _ in timespan_list: _
            ...     "---"
            ...
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))
            '---'

        Returns zero or more timespan_lists.
        """
        if not self:
            return ()
        timespan_lists = []
        timespans = sorted(self[:])
        current_list = type(self)([timespans[0]])
        latest_stop_offset = current_list[0].stop_offset
        for current_timespan in timespans[1:]:
            if current_timespan.start_offset < latest_stop_offset:
                current_list.append(current_timespan)
            elif (
                include_tangent_timespans
                and current_timespan.start_offset == latest_stop_offset
            ):
                current_list.append(current_timespan)
            else:
                timespan_lists.append(current_list)
                current_list = type(self)([current_timespan])
            if latest_stop_offset < current_timespan.stop_offset:
                latest_stop_offset = current_timespan.stop_offset
        if current_list:
            timespan_lists.append(current_list)
        return tuple(timespan_lists)

    def reflect(self, axis=None) -> "TimespanList":
        """
        Reflects timespans.

        ..  container:: example

            Reflects timespans about timespan list axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.reflect()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((4, 1)))
            Timespan(Offset((4, 1)), Offset((7, 1)))
            Timespan(Offset((7, 1)), Offset((10, 1)))

        ..  container:: example

            Reflects timespans about arbitrary axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.reflect(axis=abjad.Offset(15))
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((20, 1)), Offset((24, 1)))
            Timespan(Offset((24, 1)), Offset((27, 1)))
            Timespan(Offset((27, 1)), Offset((30, 1)))

        Operates in place and returns timespan list.
        """
        if axis is None:
            axis = self.axis
        timespans = []
        for timespan in self:
            timespan = timespan.reflect(axis=axis)
            timespans.append(timespan)
        timespans.reverse()
        self[:] = timespans
        return self

    def remove_degenerate_timespans(self) -> "TimespanList":
        """
        Removes degenerate timespans.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(5, 5),
            ...     abjad.Timespan(5, 10),
            ...     abjad.Timespan(5, 25),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.remove_degenerate_timespans()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((5, 1)), Offset((10, 1)))
            Timespan(Offset((5, 1)), Offset((25, 1)))

        Operates in place and returns timespan list.
        """
        timespans = [x for x in self if x.wellformed]
        self[:] = timespans
        return self

    def repeat_to_stop_offset(self, stop_offset) -> "TimespanList":
        """
        Repeats timespans to ``stop_offset``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 15), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.repeat_to_stop_offset(15)
            >>> abjad.show(timespans, range_=(0, 15), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))
            Timespan(Offset((10, 1)), Offset((13, 1)))
            Timespan(Offset((13, 1)), Offset((15, 1)))

        Operates in place and returns timespan list.
        """
        assert self.is_sorted
        stop_offset = _duration.Offset(stop_offset)
        assert self.stop_offset <= stop_offset
        current_timespan_index = 0
        if self:
            while self.stop_offset < stop_offset:
                current_timespan = self[current_timespan_index]
                translation = self.stop_offset - current_timespan.start_offset
                new_timespan = current_timespan.translate(translation)
                self.append(new_timespan)
                current_timespan_index += 1
            if stop_offset < self.stop_offset:
                self[-1] = self[-1].set_offsets(stop_offset=stop_offset)
        return self

    def rotate(self, count) -> "TimespanList":
        """
        Rotates by ``count`` contiguous timespans.

        ..  container:: example

            Rotates by one timespan to the left:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 4),
            ...     abjad.Timespan(4, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.rotate(-1)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((1, 1)))
            Timespan(Offset((1, 1)), Offset((7, 1)))
            Timespan(Offset((7, 1)), Offset((10, 1)))

        ..  container:: example

            Rotates by one timespan to the right:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 4),
            ...     abjad.Timespan(4, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.rotate(1)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((9, 1)))
            Timespan(Offset((9, 1)), Offset((10, 1)))

        Operates in place and returns timespan list.
        """
        assert isinstance(count, int)
        assert self.all_are_contiguous
        elements_to_move = count % len(self)
        if elements_to_move == 0:
            return self
        left_timespans = self[:-elements_to_move]
        right_timespans = self[-elements_to_move:]
        split_offset = right_timespans[0].start_offset
        translation_to_left = split_offset - self.start_offset
        translation_to_left *= -1
        translation_to_right = self.stop_offset - split_offset
        translated_right_timespans = []
        for right_timespan in right_timespans:
            translated_right_timespan = right_timespan.translate_offsets(
                translation_to_left, translation_to_left
            )
            translated_right_timespans.append(translated_right_timespan)
        translated_left_timespans = []
        for left_timespan in left_timespans:
            translated_left_timespan = left_timespan.translate_offsets(
                translation_to_right, translation_to_right
            )
            translated_left_timespans.append(translated_left_timespan)
        new_timespans = translated_right_timespans + translated_left_timespans
        self[:] = new_timespans
        return self

    def round_offsets(
        self, multiplier, anchor=_enums.LEFT, must_be_wellformed=True
    ) -> "TimespanList":
        """
        Rounds offsets of timespans in list to multiples of ``multiplier``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(3)
            >>> abjad.show(rounded_timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in rounded_timespans: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((9, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(5)
            >>> abjad.show(rounded_timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in rounded_timespans: _
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(
            ...     5,
            ...     anchor=abjad.RIGHT,
            ... )
            >>> abjad.show(rounded_timespans, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in rounded_timespans: _
            Timespan(Offset((-5, 1)), Offset((0, 1)))
            Timespan(Offset((0, 1)), Offset((5, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(
            ...     5,
            ...     anchor=abjad.RIGHT,
            ...     must_be_wellformed=False,
            ... )

            >>> for _ in rounded_timespans: _
            Timespan(Offset((0, 1)), Offset((0, 1)))
            Timespan(Offset((5, 1)), Offset((5, 1)))
            Timespan(Offset((5, 1)), Offset((10, 1)))

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.round_offsets(
                multiplier,
                anchor=anchor,
                must_be_wellformed=must_be_wellformed,
            )
            timespans.append(timespan)
        self[:] = timespans
        return self

    def scale(self, multiplier, anchor=_enums.LEFT) -> "TimespanList":
        """
        Scales timespan by ``multiplier`` relative to ``anchor``.

        ..  container:: example

            Scales timespans relative to timespan list start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 14), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.scale(2)
            >>> abjad.show(timespans, range_=(0, 14), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((6, 1)))
            Timespan(Offset((3, 1)), Offset((9, 1)))
            Timespan(Offset((6, 1)), Offset((14, 1)))

        ..  container:: example

            Scales timespans relative to timespan list stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.scale(2, anchor=abjad.RIGHT)
            >>> abjad.show(timespans, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-3, 1)), Offset((3, 1)))
            Timespan(Offset((0, 1)), Offset((6, 1)))
            Timespan(Offset((2, 1)), Offset((10, 1)))

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.scale(multiplier, anchor=anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def split_at_offset(self, offset) -> tuple["TimespanList", "TimespanList"]:
        """
        Splits timespans at ``offset``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(4)

            >>> abjad.show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> for _ in left: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((4, 1)))

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> for _ in right: _
            Timespan(Offset((4, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))

        ..  container:: example

            Splits at offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(6)

            >>> abjad.show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> for _ in left: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> for _ in right: _
            Timespan(Offset((6, 1)), Offset((10, 1)))

        ..  container:: example

            Splits at offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(-1)

            >>> left
            TimespanList([])

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> for _ in right: _
            Timespan(Offset((0, 1)), Offset((3, 1)))
            Timespan(Offset((3, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((10, 1)))

        """
        offset = _duration.Offset(offset)
        before_list = type(self)()
        during_list = type(self)()
        after_list = type(self)()
        for timespan in self:
            if timespan.stop_offset <= offset:
                before_list.append(timespan)
            elif offset <= timespan.start_offset:
                after_list.append(timespan)
            else:
                during_list.append(timespan)
        for timespan in during_list:
            before_timespan, after_timespan = timespan.split_at_offset(offset)
            before_list.append(before_timespan)
            after_list.append(after_timespan)
        before_list.sort()
        after_list.sort()
        return before_list, after_list

    def split_at_offsets(self, offsets) -> list["TimespanList"]:
        """
        Splits timespans at ``offsets``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(4, 10),
            ...     abjad.Timespan(15, 20),
            ... ])
            >>> abjad.show(timespans, range_=(0, 20), scale=0.5) # doctest: +SKIP

            >>> offsets = [-1, 3, 6, 12, 13]
            >>> for timespan_list in timespans.split_at_offsets(offsets):
            ...     abjad.show(timespan_list, range_=(0, 20), scale=0.5) # doctest: +SKIP
            ...     for _ in timespan_list: _
            ...     "---"
            ...

        ..  container:: example

            Splits empty list:

            >>> timespans = abjad.TimespanList([])
            >>> timespans.split_at_offsets(offsets)
            [TimespanList([])]

        """
        timespan_lists = [self]
        if not self:
            return timespan_lists
        offsets = sorted(set(_duration.Offset(x) for x in offsets))
        offsets = [x for x in offsets if self.start_offset < x < self.stop_offset]
        for offset in offsets:
            shards = [x for x in timespan_lists[-1].split_at_offset(offset) if x]
            if shards:
                timespan_lists[-1:] = shards
        return timespan_lists

    def stretch(self, multiplier, anchor=None) -> "TimespanList":
        """
        Stretches timespans by ``multiplier`` relative to ``anchor``.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 20), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.stretch(2)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((6, 1)))
            Timespan(Offset((6, 1)), Offset((12, 1)))
            Timespan(Offset((12, 1)), Offset((20, 1)))

        ..  container:: example

            Stretches timespans relative to arbitrary anchor:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(-8, 12), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.stretch(2, anchor=abjad.Offset(8))
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((-8, 1)), Offset((-2, 1)))
            Timespan(Offset((-2, 1)), Offset((4, 1)))
            Timespan(Offset((4, 1)), Offset((12, 1)))

        Operates in place and returns timespan list.
        """
        timespans = []
        if anchor is None:
            anchor = self.start_offset
        for timespan in self:
            timespan = timespan.stretch(multiplier, anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def translate(self, translation=None) -> "TimespanList":
        """
        Translates timespans by ``translation``.

        ..  container:: example

            Translates timespan by offset ``50``:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.translate(50)
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((50, 1)), Offset((53, 1)))
            Timespan(Offset((53, 1)), Offset((56, 1)))
            Timespan(Offset((56, 1)), Offset((60, 1)))

        Operates in place and returns timespan list.
        """
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self, start_offset_translation=None, stop_offset_translation=None
    ) -> "TimespanList":
        """
        Translates timespans by ``start_offset_translation`` and
        ``stop_offset_translation``.

        ..  container:: example

            Translates timespan start- and stop-offsets equally:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.translate_offsets(50, 50)
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((50, 1)), Offset((53, 1)))
            Timespan(Offset((53, 1)), Offset((56, 1)))
            Timespan(Offset((56, 1)), Offset((60, 1)))

        Translates timespan stop-offsets only:

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ... ])
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> timespans = timespans.translate_offsets(stop_offset_translation=20)
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> for _ in timespans: _
            Timespan(Offset((0, 1)), Offset((23, 1)))
            Timespan(Offset((3, 1)), Offset((26, 1)))
            Timespan(Offset((6, 1)), Offset((30, 1)))

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.translate_offsets(
                start_offset_translation, stop_offset_translation
            )
            timespans.append(timespan)
        self[:] = timespans
        return self


def _format_postscript_argument(argument):
    if isinstance(argument, str):
        if argument.startswith("/"):
            return argument
        return f"({argument})"
    elif isinstance(argument, collections.abc.Sequence):
        if not argument:
            return "[ ]"
        string = " ".join(_format_postscript_argument(_) for _ in argument)
        return f"[ {string} ]"
    elif isinstance(argument, bool):
        return str(argument).lower()
    elif isinstance(argument, int | float):
        argument = _math.integer_equivalent_number_to_integer(argument)
        return str(argument)
    return str(argument)


_fpa = _format_postscript_argument


def _make_timespan_list_markup(
    timespans,
    postscript_x_offset,
    postscript_scale,
    draw_offsets=True,
    sortkey=None,
):
    exploded_timespan_lists = []
    if not sortkey:
        exploded_timespan_lists.extend(timespans.explode())
    else:
        sorted_timespan_lists = {}
        for timespan in timespans:
            value = getattr(timespan, sortkey)
            if value not in sorted_timespan_lists:
                sorted_timespan_lists[value] = TimespanList()
            sorted_timespan_lists[value].append(timespan)
        for key, timespans in sorted(sorted_timespan_lists.items()):
            exploded_timespan_lists.extend(timespans.explode())
    postscript_strings = ["0.2 setlinewidth"]
    offset_mapping = {}
    height = ((len(exploded_timespan_lists) - 1) * 3) + 1
    for level, timespans in enumerate(exploded_timespan_lists, 0):
        postscript_y_offset = height - (level * 3) - 0.5
        for timespan in timespans:
            offset_mapping[timespan.start_offset] = level
            offset_mapping[timespan.stop_offset] = level
            strings = timespan._as_postscript(
                postscript_x_offset, postscript_y_offset, postscript_scale
            )
            postscript_strings.extend(strings)
    if not draw_offsets:
        strings = [
            r"\postscript",
            '#"',
            *postscript_strings,
            '"',
        ]
        string = "\n".join(strings)
        markup = _indicators.Markup(string)
        return markup
    postscript_strings.extend(
        [
            "0.1 setlinewidth",
            "[ 0.1 0.2 ] 0 setdash",
        ]
    )
    for offset in sorted(offset_mapping):
        level = offset_mapping[offset]
        x_offset = float(offset) * postscript_scale
        x_offset -= postscript_x_offset
        postscript_strings.extend(
            [
                f"{_fpa(x_offset)} {_fpa(height + 1.5)} moveto",
                f"{_fpa(x_offset)} {_fpa(height - (level * 3))} lineto",
                "stroke",
            ]
        )
    postscript_strings.extend(
        [
            "0 0 moveto",
            "0.99 setgray",
            "0 0.01 rlineto",
            "stroke",
        ]
    )
    string = "\n".join(postscript_strings)
    postscript = string
    x_extent = float(timespans.stop_offset)
    x_extent *= postscript_scale
    x_extent += postscript_x_offset
    y_extent = height + 1.5
    lines_string = rf"\pad-to-box #'(0 . {x_extent}) #'(0 . {y_extent})"
    lines_string += f'\n\\postscript #"\n{postscript}"'
    fraction_strings = []
    for offset in sorted(offset_mapping):
        offset = _duration.Offset(offset)
        numerator, denominator = offset.numerator, offset.denominator
        x_translation = float(offset) * postscript_scale
        x_translation -= postscript_x_offset
        string = rf"\translate #'({x_translation} . 1)"
        fraction_strings.append(string)
        string = r"\sans \fontsize #-3 \center-align"
        string += rf" \fraction {numerator} {denominator}"
        fraction_strings.append(string)
    fraction_string = "\n".join(fraction_strings)
    fraction_string = f"\\overlay {{\n{fraction_string}\n}}"
    string = f"\\column {{\n{fraction_string}\n{lines_string}\n}}"
    return string
