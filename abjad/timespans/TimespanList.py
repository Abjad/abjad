import collections
from abjad import enums
from abjad.utilities import Infinity
from abjad.utilities import NegativeInfinity
from abjad.utilities.TypedList import TypedList
from abjad.top.new import new


class TimespanList(TypedList):
    """
    Timespan list.

    ..  container:: example

        Contiguous timespan list:

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 3),
        ...     abjad.Timespan(3, 6),
        ...     abjad.Timespan(6, 10),
        ...     ])
        >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        >>> abjad.f(timespans)
        abjad.TimespanList(
            [
                abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(3, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(3, 1),
                    stop_offset=abjad.Offset(6, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(6, 1),
                    stop_offset=abjad.Offset(10, 1),
                    ),
                ]
            )

    ..  container:: example

        Overlapping timespan list:

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 16),
        ...     abjad.Timespan(5, 12),
        ...     abjad.Timespan(-2, 8),
        ...     abjad.Timespan(15, 20),
        ...     abjad.Timespan(24, 30),
        ...     ])
        >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        >>> abjad.f(timespans)
        abjad.TimespanList(
            [
                abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(16, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(5, 1),
                    stop_offset=abjad.Offset(12, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(-2, 1),
                    stop_offset=abjad.Offset(8, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(15, 1),
                    stop_offset=abjad.Offset(20, 1),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(24, 1),
                    stop_offset=abjad.Offset(30, 1),
                    ),
                ]
            )

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
        ...     ])

        >>> abjad.f(timespans)
        abjad.TimespanList(
            [
                abjad.Timespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(1, 2),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(3, 4),
                    ),
                abjad.Timespan(
                    start_offset=abjad.Offset(3, 4),
                    stop_offset=abjad.Offset(1, 1),
                    ),
                ]
            )

    Operations on timespan currently work in place.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Timespans'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        """
        Keeps material that intersects ``timespan``.

        ..  container:: example

            Keeps material that intersects timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(5, 10)
            >>> _ = timespans & timespan
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(8, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __illustrate__(self, key=None, range_=None, sortkey=None, scale=None):
        """
        Illustrates timespans.

        ..  container:: example

            Illustrates timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan_operand = abjad.Timespan(6, 10)
            >>> timespans = timespans - timespan_operand
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> illustration = timespans.__illustrate__()

        Returns LilyPond file.
        """
        import abjad
        if not self:
            return abjad.Markup.null().__illustrate__()
        if isinstance(range_, abjad.Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = self.start_offset, self.stop_offset
        if scale is None:
            scale = 1.
        assert 0 < scale
        minimum = float(abjad.Offset(minimum))
        maximum = float(abjad.Offset(maximum))
        postscript_scale = 150. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        if key is None:
            markup = self._make_timespan_list_markup(
                self,
                postscript_x_offset,
                postscript_scale,
                sortkey=sortkey,
                )
        else:
            timespan_lists = {}
            for timespan in self:
                value = getattr(timespan, key)
                if value not in timespan_lists:
                    timespan_lists[value] = type(self)()
                timespan_lists[value].append(timespan)
            markups = []
            for i, item in enumerate(sorted(timespan_lists.items())):
                value, timespans = item
                timespans.sort()
                if 0 < i:
                    vspace_markup = abjad.Markup.vspace(0.5)
                    markups.append(vspace_markup)
                value_markup = abjad.Markup('{}:'.format(value))
                value_markup = abjad.Markup.line([value_markup])
                value_markup = value_markup.sans().fontsize(-1)
                markups.append(value_markup)
                vspace_markup = abjad.Markup.vspace(0.5)
                markups.append(vspace_markup)
                timespan_markup = self._make_timespan_list_markup(
                    timespans,
                    postscript_x_offset,
                    postscript_scale,
                    sortkey=sortkey,
                    )
                markups.append(timespan_markup)
            markup = abjad.Markup.left_column(markups)
        return markup.__illustrate__()

    def __invert__(self):
        """
        Inverts timespans.

        ..  container:: example

            Inverts timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(~timespans, range_=(-2, 30), scale=0.5) # doctest: +SKIP

            >>> abjad.f(~timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(8, 1),
                        stop_offset=abjad.Offset(15, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(20, 1),
                        stop_offset=abjad.Offset(24, 1),
                        ),
                    ]
                )

        ..  container:: example

            Inverts contiguous timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> ~timespans
            TimespanList([])

        Returns new timespan list.
        """
        result = type(self)()
        result.append(self.timespan)
        for timespan in self:
            result = result - timespan
        return result

    def __sub__(self, timespan):
        """
        Deletes material that intersects ``timespan``.

        ..  container:: example

            Deletes material that intersects timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(5, 10)
            >>> _ = timespans - timespan
            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(16, 1),
                        ),
                    ]
                )

            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        Operates in place and returns timespan list.
        """
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan - timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def _coerce(argument):
            if timespans.Timespan._implements_timespan_interface(argument):
                return argument
            elif isinstance(argument, timespans.Timespan):
                return argument
            elif isinstance(argument, tuple) and len(argument) == 2:
                return timespans.Timespan(*argument)
            else:
                return timespans.Timespan(argument)

        from abjad import timespans
        return _coerce

    ### PRIVATE METHODS ###

    def _get_offsets(self, argument):
        try:
            return argument.start_offset, argument.stop_offset
        except AttributeError:
            pass
        try:
            return argument.timespan.offsets
        except AttributeError:
            pass
        raise TypeError(argument)

    def _get_timespan(self, argument):
        import abjad
        start_offset, stop_offset = self._get_offsets(argument)
        return abjad.Timespan(start_offset, stop_offset)

    @staticmethod
    def _make_timespan_list_markup(
        timespans,
        postscript_x_offset,
        postscript_scale,
        draw_offsets=True,
        sortkey=None,
        ):
        import abjad
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
        ps = abjad.Postscript()
        ps = ps.setlinewidth(0.2)
        offset_mapping = {}
        height = ((len(exploded_timespan_lists) - 1) * 3) + 1
        for level, timespans in enumerate(exploded_timespan_lists, 0):
            postscript_y_offset = height - (level * 3) - 0.5
            for timespan in timespans:
                offset_mapping[timespan.start_offset] = level
                offset_mapping[timespan.stop_offset] = level
                ps += timespan._as_postscript(
                    postscript_x_offset,
                    postscript_y_offset,
                    postscript_scale,
                    )
        if not draw_offsets:
            markup = abjad.Markup.postscript(ps)
            return markup
        ps = ps.setlinewidth(0.1)
        ps = ps.setdash([0.1, 0.2])
        for offset in sorted(offset_mapping):
            level = offset_mapping[offset]
            x_offset = (float(offset) * postscript_scale)
            x_offset -= postscript_x_offset
            ps = ps.moveto(x_offset, height + 1.5)
            ps = ps.lineto(x_offset, height - (level * 3))
            ps = ps.stroke()
        ps = ps.moveto(0, 0)
        ps = ps.setgray(0.99)
        ps = ps.rlineto(0, 0.01)
        ps = ps.stroke()
        x_extent = float(timespans.stop_offset)
        x_extent *= postscript_scale
        x_extent += postscript_x_offset
        x_extent = (0, x_extent)
        y_extent = (0, height + 1.5)
        lines_markup = abjad.Markup.postscript(ps)
        lines_markup = lines_markup.pad_to_box(x_extent, y_extent)
        fraction_markups = []
        for offset in sorted(offset_mapping):
            offset = abjad.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = abjad.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            fraction_markups.append(fraction)
        fraction_markup = abjad.Markup.overlay(fraction_markups)
        markup = abjad.Markup.column([fraction_markup, lines_markup])
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        """
        Is true when all timespans are contiguous.

        ..  container:: example

            Is true when all timespans are contiguous:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_contiguous
            False

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_contiguous
            True

        Returns true or false.
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
    def all_are_nonoverlapping(self):
        """
        Is true when all timespans are nonoverlapping.

        ..  container:: example

            Is true when all timespans are nonoverlapping:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_nonoverlapping
            False

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_nonoverlapping
            True

        Returns true or false.
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
    def all_are_well_formed(self):
        """
        Is true when all timespans are well-formed.

        ..  container:: example

            Is true when all timespans are well-formed:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_well_formed
            True

        ..  container:: example

            Is true when all timespans are well-formed:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.all_are_well_formed
            True

        ..  container:: example

            Is true when timespan list is empty:

            >>> abjad.TimespanList().all_are_well_formed
            True

        Is false when timespans are not all well-formed.

        Returns true or false.
        """
        return all(self._get_timespan(argument).is_well_formed for argument in self)

    @property
    def axis(self):
        """
        Gets axis defined equal to arithmetic mean of start- and stop-offsets.

        ..  container:: example

            Gets axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.axis
            Offset(5, 1)

        ..  container:: example

            Gets axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.axis
            Offset(14, 1)

        ..  container:: example

            Gets none when timespan list is empty:

            >>> abjad.TimespanList().axis is None
            True

        Returns offset or none.
        """
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        """
        Gets duration of timespan list.

        ..  container:: example

            Gets duration:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.duration
            Duration(32, 1)

        ..  container:: example

            Gets zero when timespan list is empty:

            >>> abjad.TimespanList().duration
            Duration(0, 1)

        Returns duration.
        """
        import abjad
        if (self.stop_offset is not Infinity and
            self.start_offset is not NegativeInfinity):
            return self.stop_offset - self.start_offset
        else:
            return abjad.Duration(0)

    @property
    def is_sorted(self):
        """
        Is true when timespans are in time order.

        ..  container:: example

            Is true when timespans are sorted:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.is_sorted
            True

        ..  container:: example

            Is false when timespans are not sorted:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(6, 10),
            ...     abjad.Timespan(3, 6),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.is_sorted
            False

        Returns true or false.
        """
        import abjad
        if len(self) < 2:
            return True
        pairs = abjad.sequence(self).nwise()
        for left_timespan, right_timespan in pairs:
            if right_timespan.start_offset < left_timespan.start_offset:
                return False
            if left_timespan.start_offset == right_timespan.start_offset:
                if right_timespan.stop_offset < left_timespan.stop_offset:
                    return False
        return True

    @property
    def start_offset(self):
        """
        Gets start offset.

        Defined equal to earliest start offset of any timespan in list.

        ..  container:: example

            Gets start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.start_offset
            Offset(0, 1)

        ..  container:: example

            Gets start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.start_offset
            Offset(-2, 1)

        ..  container:: example

            Gets negative infinity when timespan list is empty:

            >>> abjad.TimespanList().start_offset
            NegativeInfinity

        Returns offset or none.
        """
        if self:
            return min([self._get_timespan(argument).start_offset
                for argument in self])
        else:
            return NegativeInfinity

    @property
    def stop_offset(self):
        """
        Gets stop offset.

        Defined equal to latest stop offset of any timespan.

        ..  container:: example

            Gets stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.stop_offset
            Offset(10, 1)

        ..  container:: example

            Gets stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespans.stop_offset
            Offset(30, 1)

        ..  container:: example


            Gets infinity when timespan list is empty:

            >>> abjad.TimespanList().stop_offset
            Infinity

        Returns offset or none.
        """
        if self:
            return max([self._get_timespan(argument).stop_offset for argument in self])
        else:
            return Infinity

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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(timespans.timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> timespans.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ..  container:: example

            Gets timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.show(timespans.timespan, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> timespans.timespan
            Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(30, 1))

        ..  container:: example

            Gets infinite timespan when list is empty:

            >>> abjad.TimespanList().timespan
            Timespan(start_offset=NegativeInfinity, stop_offset=Infinity)

        Returns timespan.
        """
        from abjad import timespans
        return timespans.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def clip_timespan_durations(self, minimum=None, maximum=None, anchor=enums.Left):
        """
        Clips timespan durations.

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> result = timespans.clip_timespan_durations(
            ...     minimum=5,
            ...     )
            >>> abjad.show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> result = timespans.clip_timespan_durations(
            ...     maximum=5,
            ...     )
            >>> abjad.show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(1, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    ]
                )

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> result = timespans.clip_timespan_durations(
            ...     minimum=3,
            ...     maximum=7,
            ...     )
            >>> abjad.show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(7, 1),
                        ),
                    ]
                )

        ..  container:: example

            Clips timespan durations:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 1),
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            >>> result = timespans.clip_timespan_durations(
            ...     minimum=3,
            ...     maximum=7,
            ...     anchor=abjad.Right,
            ...     )
            >>> abjad.show(result, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(1, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Returns new timespan list.
        """
        import abjad
        assert anchor in (enums.Left, enums.Right)
        if minimum is not None:
            minimum = abjad.Duration(minimum)
        if maximum is not None:
            maximum = abjad.Duration(maximum)
        if minimum is not None and maximum is not None:
            assert minimum <= maximum
        timespans = type(self)()
        for timespan in self:
            if minimum is not None and timespan.duration < minimum:
                if anchor is enums.Left:
                    new_timespan = timespan.set_duration(minimum)
                else:
                    new_start_offset = timespan.stop_offset - minimum
                    new_timespan = abjad.new(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                        )
            elif maximum is not None and maximum < timespan.duration:
                if anchor is enums.Left:
                    new_timespan = timespan.set_duration(maximum)
                else:
                    new_start_offset = timespan.stop_offset - maximum
                    new_timespan = abjad.new(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                        )
            else:
                new_timespan = timespan
            timespans.append(new_timespan)
        return timespans

    def compute_logical_and(self):
        """
        Computes logical AND of timespans.

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical AND:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_and()
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(8, 1),
                        ),
                    ]
                )

        Same as setwise intersection.

        Operates in place and returns timespan list.
        """
        if 1 < len(self):
            result = self[0]
            for timespan in self:
                if not timespan.intersects_timespan(result):
                    self[:] = []
                    return self
                else:
                    timespans = result & timespan
                    result = timespans[0]
            self[:] = [result]
        return self

    def compute_logical_or(self):
        """
        Computes logical OR of timespans.

        ..  container:: example

            Computes logical OR:

            >>> timespans = abjad.TimespanList()
            >>> _ = timespans.compute_logical_or()

            >>> timespans
            TimespanList([])

        ..  container:: example

            Computes logical OR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical OR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical OR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 2),
            ...     ])
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical OR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 2),
            ...     abjad.Timespan(10, 20),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_or()
            >>> abjad.show(timespans, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
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

        Operates in place and returns timespan list.
        """
        timespans = []
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

    def compute_logical_xor(self):
        """
        Computes logical XOR of timespans.

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList()
            >>> _ = timespans.compute_logical_xor()

            >>> timespans
            TimespanList([])

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(timespans)
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

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 2),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 12), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(timespans)
                abjad.TimespanList(
                    [
                        abjad.Timespan(
                            start_offset=abjad.Offset(-2, 1),
                            stop_offset=abjad.Offset(0, 1),
                            ),
                        abjad.Timespan(
                            start_offset=abjad.Offset(2, 1),
                            stop_offset=abjad.Offset(5, 1),
                            ),
                        abjad.Timespan(
                            start_offset=abjad.Offset(10, 1),
                            stop_offset=abjad.Offset(12, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(-2, 2),
            ...     abjad.Timespan(10, 20),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(timespans)
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

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(4, 8),
            ...     abjad.Timespan(2, 6),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()
            >>> abjad.show(timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(8, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Computes logical XOR:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(0, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.compute_logical_xor()

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
                revised_timespan_1_fragments = []
                for timespan_1_fragment in timespan_1_fragments:
                    if timespan_2.intersects_timespan(timespan_1_fragment):
                        result = timespan_1_fragment - timespan_2
                        revised_timespan_1_fragments.extend(result)
                    else:
                        revised_timespan_1_fragments.append(
                            timespan_1_fragment)
                timespan_1_fragments = revised_timespan_1_fragments
            all_fragments.extend(timespan_1_fragments)
        self[:] = all_fragments
        self.sort()
        return self

    def compute_overlap_factor(self, timespan=None):
        """
        Computes overlap factor of timespans.

        ..  container:: example

            Example timespan list:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 15),
            ...     abjad.Timespan(20, 25),
            ...     abjad.Timespan(20, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Computes overlap factor across the entire list:

            >>> timespans.compute_overlap_factor()
            Multiplier(7, 6)

        ..  container:: example

            Computes overlap factor within a specific timespan:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(-15, 0))
            Multiplier(0, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(-10, 5),
            ...     )
            Multiplier(1, 3)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(-5, 10))
            Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(0, 15))
            Multiplier(4, 3)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(5, 20))
            Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(10, 25))
            Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            >>> timespans.compute_overlap_factor(
            ...     timespan=abjad.Timespan(15, 30))
            Multiplier(1, 1)

        Returns multiplier.
        """
        import abjad
        if timespan is None:
            timespan = self.timespan
        time_relation = abjad.timespans.timespan_2_intersects_timespan_1(
            timespan_1=timespan)
        timespans = self.get_timespans_that_satisfy_time_relation(
            time_relation)
        total_overlap = abjad.Duration(sum(
            x.get_overlap_with_timespan(timespan) for x in timespans))
        overlap_factor = total_overlap / timespan.duration
        return overlap_factor

    def compute_overlap_factor_mapping(self):
        """
        Computes overlap factor for each consecutive offset pair in timespans.

        ..  container:: example

            Computes overlap factor mapping:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 10),
            ...     abjad.Timespan(5, 15),
            ...     abjad.Timespan(20, 25),
            ...     abjad.Timespan(20, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> mapping = timespans.compute_overlap_factor_mapping()
            >>> for timespan, overlap_factor in mapping.items():
            ...     timespan.start_offset, timespan.stop_offset, overlap_factor
            ...
            (Offset(0, 1), Offset(5, 1), Multiplier(1, 1))
            (Offset(5, 1), Offset(10, 1), Multiplier(2, 1))
            (Offset(10, 1), Offset(15, 1), Multiplier(1, 1))
            (Offset(15, 1), Offset(20, 1), Multiplier(0, 1))
            (Offset(20, 1), Offset(25, 1), Multiplier(2, 1))
            (Offset(25, 1), Offset(30, 1), Multiplier(1, 1))

        Returns mapping.
        """
        import abjad
        mapping = collections.OrderedDict()
        offsets = abjad.sequence(sorted(self.count_offsets()))
        for start_offset, stop_offset in offsets.nwise():
            timespan = abjad.Timespan(start_offset, stop_offset)
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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items()):
            ...     offset, count
            ...
            (Offset(0, 1), 1)
            (Offset(3, 1), 2)
            (Offset(6, 1), 2)
            (Offset(10, 1), 1)

        ..  container:: example

            Counts offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(16, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(8, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(24, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items()):
            ...     offset, count
            ...
            (Offset(-2, 1), 1)
            (Offset(0, 1), 1)
            (Offset(5, 1), 1)
            (Offset(8, 1), 1)
            (Offset(12, 1), 1)
            (Offset(15, 1), 1)
            (Offset(16, 1), 1)
            (Offset(20, 1), 1)
            (Offset(24, 1), 1)
            (Offset(30, 1), 1)

        ..  container:: example

            Counts offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(0, 6),
            ...     abjad.Timespan(0, 9),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> offset_counter = timespans.count_offsets()
            >>> abjad.show(offset_counter, range_=(0, 9), scale=0.5) # doctest: +SKIP

            >>> for offset, count in sorted(
            ...     timespans.count_offsets().items()):
            ...     offset, count
            ...
            (Offset(0, 1), 3)
            (Offset(3, 1), 1)
            (Offset(6, 1), 1)
            (Offset(9, 1), 1)

        Returns counter.
        """
        from abjad import meter
        return meter.OffsetCounter(self)

    def explode(self, inventory_count=None):
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
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Explodes timespans into the optimal number of non-overlapping
            timespan_lists:

            >>> for exploded_timespan_list in timespans.explode():
            ...     abjad.f(exploded_timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(13, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(17, 1),
                        stop_offset=abjad.Offset(19, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(19, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(34, 1),
                        stop_offset=abjad.Offset(37, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(16, 1),
                        stop_offset=abjad.Offset(21, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(25, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(8, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(23, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(26, 1),
                        stop_offset=abjad.Offset(29, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(32, 1),
                        stop_offset=abjad.Offset(34, 1),
                        ),
                    ]
                )

        ..  container:: example

            Explodes timespans into a less-than-optimal number of overlapping
            timespan_lists:

            >>> for exploded_timespan_list in timespans.explode(
            ...     inventory_count=2):
            ...     abjad.f(exploded_timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(13, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(23, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(25, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(34, 1),
                        stop_offset=abjad.Offset(37, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(8, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(16, 1),
                        stop_offset=abjad.Offset(21, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(17, 1),
                        stop_offset=abjad.Offset(19, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(19, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(26, 1),
                        stop_offset=abjad.Offset(29, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(32, 1),
                        stop_offset=abjad.Offset(34, 1),
                        ),
                    ]
                )

        ..  container:: example

            Explodes timespans into a greater-than-optimal number of
            non-overlapping timespan lists:

            >>> for exploded_timespan_list in timespans.explode(
            ...     inventory_count=6):
            ...     abjad.f(exploded_timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(16, 1),
                        stop_offset=abjad.Offset(21, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(34, 1),
                        stop_offset=abjad.Offset(37, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(23, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(8, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(17, 1),
                        stop_offset=abjad.Offset(19, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(19, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(26, 1),
                        stop_offset=abjad.Offset(29, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(32, 1),
                        stop_offset=abjad.Offset(34, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(13, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(25, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

        Returns timespan lists.
        """
        assert isinstance(inventory_count, (type(None), int))
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
            current_overlap_factor = \
                current_timespan.duration / bounding_timespan.duration
            if empty_timespans_pairs:
                i, empty_timespans = empty_timespans_pairs.pop()
                empty_timespans.append(current_timespan)
                global_overlap_factors[i] = current_overlap_factor
                continue
            nonoverlapping_timespan_lists = []
            overlapping_timespan_lists = []
            for i, result_timespans in enumerate(result_timespan_lists):
                local_overlap_factor = result_timespans.compute_overlap_factor(
                    current_timespan)
                global_overlap_factor = global_overlap_factors[i]
                if not local_overlap_factor:
                    nonoverlapping_timespan_lists.append(
                        (i, global_overlap_factor))
                else:
                    overlapping_timespan_lists.append(
                        (i, local_overlap_factor, global_overlap_factor))
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

            Gets timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 5)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)

            >>> timespan = timespans.get_timespan_that_satisfies_time_relation(
            ...     time_relation)
            >>> abjad.show(timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> timespan
            Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Returns timespan when timespan list contains exactly one
        timespan that satisfies ``time_relation``.

        Raises exception when timespan list contains no timespan
        that satisfies ``time_relation``.

        Raises exception when timespan list contains more than one
        timespan that satisfies ``time_relation``.
        """
        timespans = self.get_timespans_that_satisfy_time_relation(
            time_relation)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            message = 'extra timespan.'
            raise Exception(message)
        else:
            message = 'missing timespan.'
            raise Exception(message)

    def get_timespans_that_satisfy_time_relation(self, time_relation):
        """
        Gets timespans that satisfy ``time_relation``.

        ..  container:: example

            Gets timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 8)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)
            >>> result = timespans.get_timespans_that_satisfy_time_relation(
            ...     time_relation)
            >>> abjad.show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(result)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Returns new timespan list.
        """
        from abjad import timespans
        result = []
        for timespan in self:
            if isinstance(
                time_relation,
                timespans.TimespanTimespanTimeRelation):
                if time_relation(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(
                time_relation,
                timespans.OffsetTimespanTimeRelation):
                if time_relation(timespan=timespan):
                    result.append(timespan)
            else:
                message = 'unknown time relation: {!r}.'
                message = message.format(time_relation)
                raise ValueError(message)
        return type(self)(result)

    def has_timespan_that_satisfies_time_relation(self, time_relation):
        """
        Is true when timespan list has timespan that satisfies ``time_relation``.

        ..  container:: example

            Is true when list has matching timespan:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> timespan = abjad.Timespan(2, 8)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)
            >>> timespans.has_timespan_that_satisfies_time_relation(
            ...     time_relation)
            True

        ..  container:: example

            Is false when list does not have matching timespan:

            >>> timespan = abjad.Timespan(10, 20)
            >>> time_relation = abjad.timespans.timespan_2_starts_during_timespan_1(
            ...     timespan_1=timespan)

            >>> timespans.has_timespan_that_satisfies_time_relation(
            ...     time_relation)
            False

        Returns true or false.
        """
        return bool(
            self.get_timespans_that_satisfy_time_relation(time_relation))

    def partition(self, include_tangent_timespans=False):
        """
        Partitions timespans into timespan_lists.

        ..  container:: example

            Partitions timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

            >>> for timespan_list in timespans.partition():
            ...     abjad.f(timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Partitions timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     abjad.Timespan(15, 20),
            ...     abjad.Timespan(24, 30),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(16, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(8, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(24, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

            >>> for timespan_list in timespans.partition():
            ...     abjad.f(timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(8, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(16, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(15, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(24, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

        ..  container:: example

            Treats tangent timespans as part of the same group when
            ``include_tangent_timespans`` is true:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> for timespan_list in timespans.partition(
            ...     include_tangent_timespans=True,
            ...     ):
            ...     abjad.f(timespan_list)
            ...
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Returns zero or more timespan_lists.
        """
        if not self:
            return []
        timespan_lists = []
        timespans = sorted(self[:])
        current_list = type(self)([timespans[0]])
        latest_stop_offset = current_list[0].stop_offset
        for current_timespan in timespans[1:]:
            if current_timespan.start_offset < latest_stop_offset:
                current_list.append(current_timespan)
            elif (include_tangent_timespans and
                current_timespan.start_offset == latest_stop_offset):
                current_list.append(current_timespan)
            else:
                timespan_lists.append(current_list)
                current_list = type(self)([current_timespan])
            if latest_stop_offset < current_timespan.stop_offset:
                latest_stop_offset = current_timespan.stop_offset
        if current_list:
            timespan_lists.append(current_list)
        return tuple(timespan_lists)

    def reflect(self, axis=None):
        """
        Reflects timespans.

        ..  container:: example

            Reflects timespans about timespan list axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.reflect()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(4, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(4, 1),
                        stop_offset=abjad.Offset(7, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(7, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Reflects timespans about arbitrary axis:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.reflect(axis=abjad.Offset(15))
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(20, 1),
                        stop_offset=abjad.Offset(24, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(24, 1),
                        stop_offset=abjad.Offset(27, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(27, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

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

    def remove_degenerate_timespans(self):
        """
        Removes degenerate timespans.

        ..  container:: example

            Removes degenerate timespans:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(5, 5),
            ...     abjad.Timespan(5, 10),
            ...     abjad.Timespan(5, 25),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.remove_degenerate_timespans()
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(25, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        timespans = [x for x in self if x.is_well_formed]
        self[:] = timespans
        return self

    def repeat_to_stop_offset(self, stop_offset):
        """
        Repeats timespans to ``stop_offset``.

        ..  container:: example

            Repeats timespans to stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 15), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.repeat_to_stop_offset(15)
            >>> abjad.show(timespans, range_=(0, 15), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(13, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(13, 1),
                        stop_offset=abjad.Offset(15, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        import abjad
        assert self.is_sorted
        stop_offset = abjad.Offset(stop_offset)
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

    def rotate(self, count):
        """
        Rotates by ``count`` contiguous timespans.

        ..  container:: example

            Rotates by one timespan to the left:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 4),
            ...     abjad.Timespan(4, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.rotate(-1)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(1, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(1, 1),
                        stop_offset=abjad.Offset(7, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(7, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Rotates by one timespan to the right:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 4),
            ...     abjad.Timespan(4, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> _ = timespans.rotate(1)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(9, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        assert isinstance(count, int)
        assert self.all_are_contiguous
        elements_to_move = count % len(self)
        if elements_to_move == 0:
            return
        left_timespans = self[:-elements_to_move]
        right_timespans = self[-elements_to_move:]
        split_offset = right_timespans[0].start_offset
        translation_to_left = split_offset - self.start_offset
        translation_to_left *= -1
        translation_to_right = self.stop_offset - split_offset
        translated_right_timespans = []
        for right_timespan in right_timespans:
            translated_right_timespan = right_timespan.translate_offsets(
                translation_to_left, translation_to_left)
            translated_right_timespans.append(translated_right_timespan)
        translated_left_timespans = []
        for left_timespan in left_timespans:
            translated_left_timespan = left_timespan.translate_offsets(
                translation_to_right, translation_to_right)
            translated_left_timespans.append(translated_left_timespan)
        new_timespans = translated_right_timespans + translated_left_timespans
        self[:] = new_timespans
        return self

    def round_offsets(self, multiplier, anchor=enums.Left, must_be_well_formed=True):
        """
        Rounds offsets of timespans in list to multiples of ``multiplier``.

        ..  container:: example

            Rounds offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(3)
            >>> abjad.show(rounded_timespans, range_=(0, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(rounded_timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    ]
                )

        ..  container:: example

            Rounds offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(5)
            >>> abjad.show(rounded_timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(rounded_timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Rounds offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(
            ...     5,
            ...     anchor=abjad.Right,
            ...     )
            >>> abjad.show(rounded_timespans, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(rounded_timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-5, 1),
                        stop_offset=abjad.Offset(0, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Rounds offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 2),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> rounded_timespans = timespans.round_offsets(
            ...     5,
            ...     anchor=abjad.Right,
            ...     must_be_well_formed=False,
            ...     )

            >>> abjad.f(rounded_timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(0, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(5, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.round_offsets(
                multiplier,
                anchor=anchor,
                must_be_well_formed=must_be_well_formed,
                )
            timespans.append(timespan)
        self[:] = timespans
        return self

    def scale(self, multiplier, anchor=enums.Left):
        """
        Scales timespan by ``multiplier`` relative to ``anchor``.

        ..  container:: example

            Scales timespans relative to timespan list start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 14), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.scale(2)
            >>> abjad.show(timespans, range_=(0, 14), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(9, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(14, 1),
                        ),
                    ]
                )

        ..  container:: example

            Scales timespans relative to timespan list stop offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.scale(2, anchor=abjad.Right)
            >>> abjad.show(timespans, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-3, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(2, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.scale(multiplier, anchor=anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def split_at_offset(self, offset):
        """
        Splits timespans at ``offset``.

        ..  container:: example

            Splits at offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(4)

            >>> abjad.show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> abjad.f(left)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(4, 1),
                        ),
                    ]
                )

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> abjad.f(right)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(4, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Splits at offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(6)

            >>> abjad.show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> abjad.f(left)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    ]
                )

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> abjad.f(right)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        ..  container:: example

            Splits at offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> left, right = timespans.split_at_offset(-1)

            >>> left
            TimespanList([])

            >>> abjad.show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
            >>> abjad.f(right)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(3, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(10, 1),
                        ),
                    ]
                )

        Returns timespan_lists.
        """
        import abjad
        offset = abjad.Offset(offset)
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

    def split_at_offsets(self, offsets):
        """
        Splits timespans at ``offsets``.

        ..  container:: example

            Splits at offsets:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(4, 10),
            ...     abjad.Timespan(15, 20),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 20), scale=0.5) # doctest: +SKIP

            >>> offsets = [-1, 3, 6, 12, 13]
            >>> for timespan_list in timespans.split_at_offsets(offsets):
            ...     abjad.show(timespan_list, range_=(0, 20), scale=0.5) # doctest: +SKIP
            ...     abjad.f(timespan_list)
            ...


        ..  container:: example

            Splits empty list:

            >>> timespans = abjad.TimespanList([])
            >>> timespans.split_at_offsets(offsets)
            [TimespanList([])]

        Returns one or more timespan_lists.
        """
        import abjad
        timespan_lists = [self]
        if not self:
            return timespan_lists
        offsets = sorted(set(abjad.Offset(x) for x in offsets))
        offsets = [x for x in offsets
            if self.start_offset < x < self.stop_offset]
        for offset in offsets:
            shards = [x for x in timespan_lists[-1].split_at_offset(offset)
                if x]
            if shards:
                timespan_lists[-1:] = shards
        return timespan_lists

    def stretch(self, multiplier, anchor=None):
        """
        Stretches timespans by ``multiplier`` relative to ``anchor``.

        ..  container:: example

            Stretches timespans relative to timespan list start offset:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 20), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.stretch(2)
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(6, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(12, 1),
                        stop_offset=abjad.Offset(20, 1),
                        ),
                    ]
                )

        ..  container:: example

            Stretches timespans relative to arbitrary anchor:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(-8, 12), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.stretch(2, anchor=abjad.Offset(8))
            >>> abjad.show(timespans, scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(-8, 1),
                        stop_offset=abjad.Offset(-2, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(4, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(4, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    ]
                )

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

    def translate(self, translation=None):
        """
        Translates timespans by ``translation``.

        ..  container:: example

            Translates timespan by offset ``50``:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.translate(50)
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(50, 1),
                        stop_offset=abjad.Offset(53, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(53, 1),
                        stop_offset=abjad.Offset(56, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(56, 1),
                        stop_offset=abjad.Offset(60, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self,
        start_offset_translation=None,
        stop_offset_translation=None,
        ):
        """
        Translates timespans by ``start_offset_translation`` and
        ``stop_offset_translation``.

        ..  container:: example

            Translates timespan start- and stop-offsets equally:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.translate_offsets(50, 50)
            >>> abjad.show(timespans, range_=(0, 60), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(50, 1),
                        stop_offset=abjad.Offset(53, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(53, 1),
                        stop_offset=abjad.Offset(56, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(56, 1),
                        stop_offset=abjad.Offset(60, 1),
                        ),
                    ]
                )

        ..  container:: example

            Translates timespan stop-offsets only:

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 3),
            ...     abjad.Timespan(3, 6),
            ...     abjad.Timespan(6, 10),
            ...     ])
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> _ = timespans.translate_offsets(
            ...     stop_offset_translation=20)
            >>> abjad.show(timespans, range_=(0, 30), scale=0.5) # doctest: +SKIP

            >>> abjad.f(timespans)
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(23, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(3, 1),
                        stop_offset=abjad.Offset(26, 1),
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset(6, 1),
                        stop_offset=abjad.Offset(30, 1),
                        ),
                    ]
                )

        Operates in place and returns timespan list.
        """
        timespans = []
        for timespan in self:
            timespan = timespan.translate_offsets(
                start_offset_translation,
                stop_offset_translation,
                )
            timespans.append(timespan)
        self[:] = timespans
        return self
