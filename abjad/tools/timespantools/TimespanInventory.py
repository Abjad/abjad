# -*- coding: utf-8 -*-
import collections
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import sequencetools
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.topleveltools import new


class TimespanInventory(TypedList):
    r'''A timespan inventory.

    ..  container:: example

        Contiguous timespan inventory:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(3, 6),
            ...     timespantools.Timespan(6, 10),
            ...     ])
            >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

        ::

            >>> f(timespan_inventory)
            timespantools.TimespanInventory(
                [
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(3, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(3, 1),
                        stop_offset=durationtools.Offset(6, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(6, 1),
                        stop_offset=durationtools.Offset(10, 1),
                        ),
                    ]
                )

    ..  container:: example

        Overlapping timespan inventory:

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8),
            ...     timespantools.Timespan(15, 20),
            ...     timespantools.Timespan(24, 30),
            ...     ])
            >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

        ::

            >>> f(timespan_inventory)
            timespantools.TimespanInventory(
                [
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(0, 1),
                        stop_offset=durationtools.Offset(16, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(5, 1),
                        stop_offset=durationtools.Offset(12, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(-2, 1),
                        stop_offset=durationtools.Offset(8, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(15, 1),
                        stop_offset=durationtools.Offset(20, 1),
                        ),
                    timespantools.Timespan(
                        start_offset=durationtools.Offset(24, 1),
                        stop_offset=durationtools.Offset(30, 1),
                        ),
                    ]
                )

    ..  container:: example

        Empty timespan inventory:

        ::

            >>> timespantools.TimespanInventory()
            TimespanInventory([])

    Operations on timespan currently work in place.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Timespans'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        r'''Keeps material that intersects `timespan`.

        ..  container:: example

            Keeps material that intersects timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> timespan = timespantools.Timespan(5, 10)
                >>> _ = timespan_inventory & timespan
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(8, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __illustrate__(self, key=None, range_=None, sortkey=None, scale=None):
        r'''Illustrates timespan inventory.

        ..  container:: example

            Illustrates inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_operand = timespantools.Timespan(6, 10)
                >>> timespan_inventory = timespan_inventory - timespan_operand
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ..  doctest::

                >>> illustration = timespan_inventory.__illustrate__()

        Returns LilyPond file.
        '''
        from abjad.tools import timespantools
        if not self:
            return markuptools.Markup.null().__illustrate__()
        if isinstance(range_, timespantools.Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = self.start_offset, self.stop_offset
        if scale is None:
            scale = 1.
        assert 0 < scale
        minimum = float(durationtools.Offset(minimum))
        maximum = float(durationtools.Offset(maximum))
        postscript_scale = 150. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        if key is None:
            markup = self._make_timespan_inventory_markup(
                self,
                postscript_x_offset,
                postscript_scale,
                sortkey=sortkey,
                )
        else:
            inventories = {}
            for timespan in self:
                value = getattr(timespan, key)
                if value not in inventories:
                    inventories[value] = type(self)()
                inventories[value].append(timespan)
            markups = []
            for i, item in enumerate(sorted(inventories.items())):
                value, timespans = item
                timespans.sort()
                if 0 < i:
                    vspace_markup = markuptools.Markup.vspace(0.5)
                    markups.append(vspace_markup)
                value_markup = markuptools.Markup('{}:'.format(value))
                value_markup = markuptools.Markup.line([value_markup])
                value_markup = value_markup.sans().fontsize(-1)
                markups.append(value_markup)
                vspace_markup = markuptools.Markup.vspace(0.5)
                markups.append(vspace_markup)
                timespan_markup = self._make_timespan_inventory_markup(
                    timespans,
                    postscript_x_offset,
                    postscript_scale,
                    sortkey=sortkey,
                    )
                markups.append(timespan_markup)
            markup = markuptools.Markup.left_column(markups)
        return markup.__illustrate__()

    def __invert__(self):
        r'''Inverts timespan inventory.

        ..  container:: example

            Inverts inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> show(~timespan_inventory, range_=(-2, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> f(~timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(8, 1),
                            stop_offset=durationtools.Offset(15, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(20, 1),
                            stop_offset=durationtools.Offset(24, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Inverts contiguous inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> ~timespan_inventory
                TimespanInventory([])

        Returns new timespan inventory.
        '''
        result = type(self)()
        result.append(self.timespan)
        for timespan in self:
            result = result - timespan
        return result

    def __sub__(self, timespan):
        r'''Deletes material that intersects `timespan`.

        ..  container:: example

            Deletes material that intersects timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan = timespantools.Timespan(5, 10)
                >>> _ = timespan_inventory - timespan
                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(16, 1),
                            ),
                        ]
                    )

            ::

                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

        Operates in place and returns timespan inventory.
        '''
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan - timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    ### PRIVATE METHODS ###

    def _get_offsets(self, expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return expr.start_offset, expr.stop_offset
        elif hasattr(expr, 'timespan'):
            return expr.timespan.offsets
        else:
            raise TypeError(expr)

    def _get_timespan(self, expr):
        from abjad.tools import timespantools
        start_offset, stop_offset = self._get_offsets(expr)
        return timespantools.Timespan(start_offset, stop_offset)

    @staticmethod
    def _make_timespan_inventory_markup(
        timespan_inventory,
        postscript_x_offset,
        postscript_scale,
        draw_offsets=True,
        sortkey=None,
        ):
        exploded_inventories = []
        if not sortkey:
            exploded_inventories.extend(timespan_inventory.explode())
        else:
            sorted_inventories = {}
            for timespan in timespan_inventory:
                value = getattr(timespan, sortkey)
                if value not in sorted_inventories:
                    sorted_inventories[value] = TimespanInventory()
                sorted_inventories[value].append(timespan)
            for key, inventory in sorted(sorted_inventories.items()):
                exploded_inventories.extend(inventory.explode())
        ps = markuptools.Postscript()
        ps = ps.setlinewidth(0.2)
        offset_mapping = {}
        height = ((len(exploded_inventories) - 1) * 3) + 1
        for level, inventory in enumerate(exploded_inventories, 0):
            postscript_y_offset = height - (level * 3) - 0.5
            for timespan in inventory:
                offset_mapping[timespan.start_offset] = level
                offset_mapping[timespan.stop_offset] = level
                ps += timespan._as_postscript(
                    postscript_x_offset,
                    postscript_y_offset,
                    postscript_scale,
                    )
        if not draw_offsets:
            markup = markuptools.Markup.postscript(ps)
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
        x_extent = float(timespan_inventory.stop_offset)
        x_extent *= postscript_scale
        x_extent += postscript_x_offset
        x_extent = (0, x_extent)
        y_extent = (0, height + 1.5)
        lines_markup = markuptools.Markup.postscript(ps)
        lines_markup = lines_markup.pad_to_box(x_extent, y_extent)
        fraction_markups = []
        for offset in sorted(offset_mapping):
            offset = durationtools.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = markuptools.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            fraction_markups.append(fraction)
        fraction_markup = markuptools.Markup.overlay(fraction_markups)
        markup = markuptools.Markup.column([fraction_markup, lines_markup])
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def all_are_contiguous(self):
        r'''Is true when all timespans are contiguous.

        ..  container:: example

            Is true when all timespans are contiguous:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_contiguous
                True

        ..  container:: example

            Is false when timespans not contiguous:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_contiguous
                False

        ..  container:: example

            Is true when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().all_are_contiguous
                True

        Returns true or false.
        '''
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
        r'''Is true when all timespans are nonoverlapping.

        ..  container:: example

            Is true when all timespans are nonoverlapping:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_nonoverlapping
                True

        ..  container:: example

            Is false when timespans are overlapping:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_nonoverlapping
                False

        ..  container:: example

            Is true when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().all_are_nonoverlapping
                True

        Returns true or false.
        '''
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
        r'''Is true when all timespans are well-formed.

        ..  container:: example

            Is true when all timespans are well-formed:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_well_formed
                True

        ..  container:: example

            Is true when all timespans are well-formed:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.all_are_well_formed
                True

        ..  container:: example

            Is true when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().all_are_well_formed
                True

        Is false when timespans are not all well-formed.

        Returns true or false.
        '''
        return all(self._get_timespan(expr).is_well_formed for expr in self)

    @property
    def axis(self):
        r'''Gets axis defined equal to arithmetic mean of start- and
        stop-offsets.

        ..  container:: example

            Gets axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.axis
                Offset(5, 1)

        ..  container:: example

            Gets axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.axis
                Offset(14, 1)

        ..  container:: example

            Gets none when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().axis is None
                True

        Returns offset or none.
        '''
        if self:
            return (self.start_offset + self.stop_offset) / 2

    @property
    def duration(self):
        r'''Gets duration of timespan inventory.
        
        ..  container:: example

            Gets duration:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.duration
                Duration(10, 1)

        ..  container:: example

            Gets duration:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.duration
                Duration(32, 1)

        ..  container:: example

            Gets zero when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().duration
                Duration(0, 1)

        Returns duration.
        '''
        if (self.stop_offset is not Infinity and
            self.start_offset is not NegativeInfinity):
            return self.stop_offset - self.start_offset
        else:
            return durationtools.Duration(0)

    @property
    def is_sorted(self):
        r'''Is true when timespans are in time order.

        ..  container:: example

            Is true when timespans are sorted:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.is_sorted
                True

        ..  container:: example

            Is false when timespans are not sorted:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(6, 10),
                ...     timespantools.Timespan(3, 6),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.is_sorted
                False

        Returns true or false.
        '''
        if len(self) < 2:
            return True
        pairs = sequencetools.iterate_sequence_nwise(self)
        for left_timespan, right_timespan in pairs:
            if right_timespan.start_offset < left_timespan.start_offset:
                return False
            if left_timespan.start_offset == right_timespan.start_offset:
                if right_timespan.stop_offset < left_timespan.stop_offset:
                    return False
        return True

    @property
    def start_offset(self):
        r'''Gets start offset.
        
        Defined equal to earliest start offset of any timespan in inventory.

        ..  container:: example

            Gets start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.start_offset
                Offset(0, 1)

        ..  container:: example

            Gets start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.start_offset
                Offset(-2, 1)

        ..  container:: example

            Gets negative infinity when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().start_offset
                NegativeInfinity

        Returns offset or none.
        '''
        if self:
            return min([self._get_timespan(expr).start_offset
                for expr in self])
        else:
            return NegativeInfinity

    @property
    def stop_offset(self):
        r'''Gets stop offset.
        
        Defined equal to latest stop offset of any timespan.

        ..  container:: example

            Gets stop offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.stop_offset
                Offset(10, 1)

        ..  container:: example

            Gets stop offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.stop_offset
                Offset(30, 1)

        ..  container:: example


            Gets infinity when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().stop_offset
                Infinity

        Returns offset or none.
        '''
        if self:
            return max([self._get_timespan(expr).stop_offset for expr in self])
        else:
            return Infinity

    @property
    def timespan(self):
        r'''Gets timespan of inventory.

        ..  container:: example

            Gets timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> show(timespan_inventory.timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.timespan
                Timespan(start_offset=Offset(0, 1), stop_offset=Offset(10, 1))

        ..  container:: example

            Gets timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> show(timespan_inventory.timespan, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> timespan_inventory.timespan
                Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(30, 1))

        ..  container:: example

            Gets infinite timespan when inventory is empty:

            ::

                >>> timespantools.TimespanInventory().timespan
                Timespan(start_offset=NegativeInfinity, stop_offset=Infinity)

        Returns timespan.
        '''
        from abjad.tools import timespantools
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def clip_timespan_durations(self, minimum=None, maximum=None, anchor=Left):
        r'''Clips timespan durations.

        ..  container:: example

            Clips timespan durations:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 1),
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> result = timespan_inventory.clip_timespan_durations(
                ...     minimum=5,
                ...     )
                >>> show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(result)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Clips timespan durations:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 1),
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::
            
                >>> result = timespan_inventory.clip_timespan_durations(
                ...     maximum=5,
                ...     )
                >>> show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(result)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(1, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Clips timespan durations:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 1),
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> result = timespan_inventory.clip_timespan_durations(
                ...     minimum=3,
                ...     maximum=7,
                ...     )
                >>> show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(result)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(7, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Clips timespan durations:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 1),
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> result = timespan_inventory.clip_timespan_durations(
                ...     minimum=3,
                ...     maximum=7,
                ...     anchor=Right,
                ...     )
                >>> show(result, range_=(-2, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(result)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(1, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Returns new inventory.
        '''
        assert anchor in (Left, Right)
        if minimum is not None:
            minimum = durationtools.Duration(minimum)
        if maximum is not None:
            maximum = durationtools.Duration(maximum)
        if minimum is not None and maximum is not None:
            assert minimum <= maximum
        timespan_inventory = type(self)()
        for timespan in self:
            if minimum is not None and timespan.duration < minimum:
                if anchor == Left:
                    new_timespan = timespan.set_duration(minimum)
                else:
                    new_start_offset = timespan.stop_offset - minimum
                    new_timespan = new(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                        )
            elif maximum is not None and maximum < timespan.duration:
                if anchor == Left:
                    new_timespan = timespan.set_duration(maximum)
                else:
                    new_start_offset = timespan.stop_offset - maximum
                    new_timespan = new(
                        timespan,
                        start_offset=new_start_offset,
                        stop_offset=timespan.stop_offset,
                        )
            else:
                new_timespan = timespan
            timespan_inventory.append(new_timespan)
        return timespan_inventory

    def compute_logical_and(self):
        r'''Computes logical AND of timespans.

        ..  container:: example

            Computes logical AND:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_and()
                >>> show(timespan_inventory, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical AND:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_and()
                >>> show(timespan_inventory, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical AND:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_and()
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(8, 1),
                            ),
                        ]
                    )

        Same as setwise intersection.

        Operates in place and returns timespan inventory.
        '''
        if 1 < len(self):
            result = self[0]
            for timespan in self:
                if not timespan.intersects_timespan(result):
                    self[:] = []
                    return self
                else:
                    inventory = result & timespan
                    result = inventory[0]
            self[:] = [result]
        return self

    def compute_logical_or(self):
        r'''Computes logical OR of timespans.

        ..  container:: example

            Computes logical OR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory()
                >>> _ = timespan_inventory.compute_logical_or()

            ::

                >>> timespan_inventory
                TimespanInventory([])

        ..  container:: example

            Computes logical OR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_or()
                >>> show(timespan_inventory, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical OR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_or()
                >>> show(timespan_inventory, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical OR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 2),
                ...     ])
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_or()
                >>> show(timespan_inventory, range_=(-2, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical OR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(-2, 2),
                ...     timespantools.Timespan(10, 20),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_or()
                >>> show(timespan_inventory, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(2, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        if self:
            timespans = [self[0]]
            for timespan in self[1:]:
                if timespans[-1]._can_fuse(timespan):
                    inventory = timespans[-1] | timespan
                    timespans[-1:] = inventory[:]
                else:
                    timespans.append(timespan)
        self[:] = timespans
        return self

    def compute_logical_xor(self):
        r'''Computes logical XOR of timespans.

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory()
                >>> _ = timespan_inventory.compute_logical_xor()

            ::

                >>> timespan_inventory
                TimespanInventory([]) 

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()
                >>> show(timespan_inventory, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()
                >>> show(timespan_inventory, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ..  doctest::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 2),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ..  doctest::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(0, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(2, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:
            
            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(-2, 2),
                ...     timespantools.Timespan(10, 20),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()
                >>> show(timespan_inventory, range_=(-2, 20), scale=0.5) # doctest: +SKIP

            ..  doctest::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(2, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(4, 8),
                ...     timespantools.Timespan(2, 6),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()
                >>> show(timespan_inventory, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(2, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(8, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Computes logical XOR:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(0, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.compute_logical_xor()

            ::

                >>> timespan_inventory
                TimespanInventory([])

        Operates in place and returns timespan inventory.
        '''
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
        r'''Computes overlap factor of timespans.

        ..  container:: example

            Example inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 15),
                ...     timespantools.Timespan(20, 25),
                ...     timespantools.Timespan(20, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Computes overlap factor across the entire inventory:

            ::

                >>> timespan_inventory.compute_overlap_factor()
                Multiplier(7, 6)

        ..  container:: example

            Computes overlap factor within a specific timespan:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-15, 0))
                Multiplier(0, 1)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-10, 5))
                Multiplier(1, 3)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(-5, 10))
                Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(0, 15))
                Multiplier(4, 3)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(5, 20))
                Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(10, 25))
                Multiplier(1, 1)

        ..  container:: example

            Computes overlap factor:

            ::

                >>> timespan_inventory.compute_overlap_factor(
                ...     timespan=timespantools.Timespan(15, 30))
                Multiplier(1, 1)

        Returns multiplier.
        '''
        from abjad.tools import timespantools
        if timespan is None:
            timespan = self.timespan
        time_relation = timespantools.timespan_2_intersects_timespan_1(
            timespan_1=timespan)
        timespan_inventory = self.get_timespans_that_satisfy_time_relation(
            time_relation)
        total_overlap = durationtools.Duration(sum(
            x.get_overlap_with_timespan(timespan) for x in timespan_inventory))
        overlap_factor = total_overlap / timespan.duration
        return overlap_factor

    def compute_overlap_factor_mapping(self):
        r'''Computes overlap factor for each consecutive offset pair in
        timespans.

        ..  container:: example

            Computes overlap factor mapping:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 10),
                ...     timespantools.Timespan(5, 15),
                ...     timespantools.Timespan(20, 25),
                ...     timespantools.Timespan(20, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> mapping = timespan_inventory.compute_overlap_factor_mapping()
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
        '''
        from abjad.tools import timespantools
        mapping = collections.OrderedDict()
        for start_offset, stop_offset in \
            sequencetools.iterate_sequence_nwise(sorted(
                self.count_offsets())):
            timespan = timespantools.Timespan(start_offset, stop_offset)
            overlap_factor = self.compute_overlap_factor(timespan=timespan)
            mapping[timespan] = overlap_factor
        return mapping

    def count_offsets(self):
        r'''Counts offsets.

        ..  container:: example

            Counts offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

            ::

                >>> offset_counter = timespan_inventory.count_offsets()
                >>> show(offset_counter, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> for offset, count in sorted(
                ...     timespan_inventory.count_offsets().items()):
                ...     offset, count
                ...
                (Offset(0, 1), 1)
                (Offset(3, 1), 2)
                (Offset(6, 1), 2)
                (Offset(10, 1), 1)

        ..  container:: example

            Counts offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(16, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(8, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(24, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

            ::

                >>> offset_counter = timespan_inventory.count_offsets()
                >>> show(offset_counter, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> for offset, count in sorted(
                ...     timespan_inventory.count_offsets().items()):
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

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(0, 6),
                ...     timespantools.Timespan(0, 9),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> offset_counter = timespan_inventory.count_offsets()
                >>> show(offset_counter, range_=(0, 9), scale=0.5) # doctest: +SKIP

            ::

                >>> for offset, count in sorted(
                ...     timespan_inventory.count_offsets().items()):
                ...     offset, count
                ...
                (Offset(0, 1), 3)
                (Offset(3, 1), 1)
                (Offset(6, 1), 1)
                (Offset(9, 1), 1)

        Returns counter.
        '''
        from abjad.tools import metertools
        return metertools.OffsetCounter(self)

    def explode(self, inventory_count=None):
        r'''Explodes timespans into inventories, avoiding overlap, and
        distributing density as evenly as possible.

        ..  container:: example

            Example inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(5, 13),
                ...     timespantools.Timespan(6, 10),
                ...     timespantools.Timespan(8, 9),
                ...     timespantools.Timespan(15, 23),
                ...     timespantools.Timespan(16, 21),
                ...     timespantools.Timespan(17, 19),
                ...     timespantools.Timespan(19, 20),
                ...     timespantools.Timespan(25, 30),
                ...     timespantools.Timespan(26, 29),
                ...     timespantools.Timespan(32, 34),
                ...     timespantools.Timespan(34, 37),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

        ..  container:: example

            Explodes timespans into the optimal number of non-overlapping
            inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode():
                ...     f(exploded_inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(13, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(17, 1),
                            stop_offset=durationtools.Offset(19, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(19, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(34, 1),
                            stop_offset=durationtools.Offset(37, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(16, 1),
                            stop_offset=durationtools.Offset(21, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(25, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(8, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(23, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(26, 1),
                            stop_offset=durationtools.Offset(29, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(32, 1),
                            stop_offset=durationtools.Offset(34, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Explodes timespans into a less-than-optimal number of overlapping
            inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode(
                ...     inventory_count=2):
                ...     f(exploded_inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(13, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(23, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(25, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(34, 1),
                            stop_offset=durationtools.Offset(37, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(8, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(16, 1),
                            stop_offset=durationtools.Offset(21, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(17, 1),
                            stop_offset=durationtools.Offset(19, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(19, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(26, 1),
                            stop_offset=durationtools.Offset(29, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(32, 1),
                            stop_offset=durationtools.Offset(34, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Explodes timespans into a greater-than-optimal number of
            non-overlapping inventories:

            ::

                >>> for exploded_inventory in timespan_inventory.explode(
                ...     inventory_count=6):
                ...     f(exploded_inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(16, 1),
                            stop_offset=durationtools.Offset(21, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(34, 1),
                            stop_offset=durationtools.Offset(37, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(23, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(8, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(17, 1),
                            stop_offset=durationtools.Offset(19, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(19, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(26, 1),
                            stop_offset=durationtools.Offset(29, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(32, 1),
                            stop_offset=durationtools.Offset(34, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(13, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(25, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

        Returns inventories.
        '''
        assert isinstance(inventory_count, (type(None), int))
        if isinstance(inventory_count, int):
            assert 0 < inventory_count
        bounding_timespan = self.timespan
        global_overlap_factors = []
        empty_inventory_pairs = []
        result_inventories = []
        if inventory_count is not None:
            for i in range(inventory_count):
                global_overlap_factors.append(0)
                result_inventory = type(self)([])
                empty_inventory_pairs.append((i, result_inventory))
                result_inventories.append(result_inventory)
        for current_timespan in self:
            current_overlap_factor = \
                current_timespan.duration / bounding_timespan.duration
            if empty_inventory_pairs:
                i, empty_inventory = empty_inventory_pairs.pop()
                empty_inventory.append(current_timespan)
                global_overlap_factors[i] = current_overlap_factor
                continue
            nonoverlapping_inventories = []
            overlapping_inventories = []
            for i, result_inventory in enumerate(result_inventories):
                local_overlap_factor = result_inventory.compute_overlap_factor(
                    current_timespan)
                global_overlap_factor = global_overlap_factors[i]
                if not local_overlap_factor:
                    nonoverlapping_inventories.append(
                        (i, global_overlap_factor))
                else:
                    overlapping_inventories.append(
                        (i, local_overlap_factor, global_overlap_factor))
            nonoverlapping_inventories.sort(key=lambda x: x[1])
            overlapping_inventories.sort(key=lambda x: (x[1], x[2]))
            if not nonoverlapping_inventories and inventory_count is None:
                result_inventory = type(self)([current_timespan])
                global_overlap_factors.append(current_overlap_factor)
                result_inventories.append(result_inventory)
                continue
            if nonoverlapping_inventories:
                i = nonoverlapping_inventories[0][0]
            else:
                i = overlapping_inventories[0][0]
            result_inventory = result_inventories[i]
            result_inventory.append(current_timespan)
            global_overlap_factors[i] += current_overlap_factor
        return tuple(result_inventories)

    def get_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Gets timespan that satisifies `time_relation`.

        ..  container:: example

            Gets timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan = timespantools.Timespan(2, 5)
                >>> time_relation = \
                ...     timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan)

            ::

                >>> timespan = timespan_inventory.get_timespan_that_satisfies_time_relation(
                ...     time_relation)
                >>> show(timespan, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> timespan
                Timespan(start_offset=Offset(3, 1), stop_offset=Offset(6, 1))

        Returns timespan when timespan inventory contains exactly one
        timespan that satisfies `time_relation`.

        Raises exception when timespan inventory contains no timespan
        that satisfies `time_relation`.

        Raises exception when timespan inventory contains more than one
        timespan that satisfies `time_relation`.
        '''
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
        r'''Gets timespans that satisfy `time_relation`.

        ..  container:: example

            Gets timespans:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan = timespantools.Timespan(2, 8)
                >>> time_relation = timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan)
                >>> result = timespan_inventory.get_timespans_that_satisfy_time_relation(
                ...     time_relation)
                >>> show(result, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(result)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Returns new timespan inventory.
        '''
        from abjad.tools import timespantools
        result = []
        for timespan in self:
            if isinstance(
                time_relation,
                timespantools.TimespanTimespanTimeRelation):
                if time_relation(timespan_2=timespan):
                    result.append(timespan)
            elif isinstance(
                time_relation,
                timespantools.OffsetTimespanTimeRelation):
                if time_relation(timespan=timespan):
                    result.append(timespan)
            else:
                raise ValueError
        return type(self)(result)

    def has_timespan_that_satisfies_time_relation(self, time_relation):
        r'''Is true when timespan inventory has timespan that satisfies
        `time_relation`.

        ..  container:: example

            Is true when inventory has matching timespan:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> timespan = timespantools.Timespan(2, 8)
                >>> time_relation = \
                ...     timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan)
                >>> timespan_inventory.has_timespan_that_satisfies_time_relation(
                ...     time_relation)
                True

        ..  container:: example

            Is false when inventory does not have matching timespan:

            ::

                >>> timespan = timespantools.Timespan(10, 20)
                >>> time_relation = \
                ...     timespantools.timespan_2_starts_during_timespan_1(
                ...     timespan_1=timespan)

            ::

                >>> timespan_inventory.has_timespan_that_satisfies_time_relation(
                ...     time_relation)
                False

        Returns true or false.
        '''
        return bool(
            self.get_timespans_that_satisfy_time_relation(time_relation))

    def partition(self, include_tangent_timespans=False):
        r'''Partitions timespans into inventories.

        ..  container:: example

            Partitions timespans:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

            ::

                >>> for inventory in timespan_inventory.partition():
                ...     f(inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Partitions timespans:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     timespantools.Timespan(15, 20),
                ...     timespantools.Timespan(24, 30),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(16, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(8, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(24, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

            ::

                >>> for inventory in timespan_inventory.partition():
                ...     f(inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(8, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(16, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(24, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Treats tangent timespans as part of the same group when
            `include_tangent_timespans` is true:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> for inventory in timespan_inventory.partition(
                ...     include_tangent_timespans=True):
                ...     f(inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Returns zero or more inventories.
        '''
        if not self:
            return []
        inventories = []
        timespans = sorted(self[:])
        current_inventory = type(self)([timespans[0]])
        latest_stop_offset = current_inventory[0].stop_offset
        for current_timespan in timespans[1:]:
            if current_timespan.start_offset < latest_stop_offset:
                current_inventory.append(current_timespan)
            elif (include_tangent_timespans and
                current_timespan.start_offset == latest_stop_offset):
                current_inventory.append(current_timespan)
            else:
                inventories.append(current_inventory)
                current_inventory = type(self)([current_timespan])
            if latest_stop_offset < current_timespan.stop_offset:
                latest_stop_offset = current_timespan.stop_offset
        if current_inventory:
            inventories.append(current_inventory)
        return tuple(inventories)

    def reflect(self, axis=None):
        r'''Reflects timespans.

        ..  container:: example

            Reflects timespans about timespan inventory axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.reflect()
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(4, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(4, 1),
                            stop_offset=durationtools.Offset(7, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(7, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Reflects timespans about arbitrary axis:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.reflect(axis=Offset(15))
                >>> show(timespan_inventory, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(20, 1),
                            stop_offset=durationtools.Offset(24, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(24, 1),
                            stop_offset=durationtools.Offset(27, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(27, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
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
        r'''Removes degenerate timespans.

        ..  container:: example

            Removes degenerate timespans:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(5, 5),
                ...     timespantools.Timespan(5, 10),
                ...     timespantools.Timespan(5, 25),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.remove_degenerate_timespans()
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(25, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        timespans = [x for x in self if x.is_well_formed]
        self[:] = timespans
        return self

    def repeat_to_stop_offset(self, stop_offset):
        r'''Repeats timespans to `stop_offset`.

        ..  container:: example

            Repeats timespans to stop offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 15), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.repeat_to_stop_offset(15)
                >>> show(timespan_inventory, range_=(0, 15), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(10, 1),
                            stop_offset=durationtools.Offset(13, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(13, 1),
                            stop_offset=durationtools.Offset(15, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        assert self.is_sorted
        stop_offset = durationtools.Offset(stop_offset)
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
        r'''Rotates by `count` contiguous timespans.

        ..  container:: example

            Rotates by one timespan to the left:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 4),
                ...     timespantools.Timespan(4, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.rotate(-1)
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(1, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(1, 1),
                            stop_offset=durationtools.Offset(7, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(7, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Rotates by one timespan to the right:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 4),
                ...     timespantools.Timespan(4, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.rotate(1)
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(9, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
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

    def round_offsets(self, multiplier, anchor=Left, must_be_well_formed=True):
        '''Rounds offsets of timespans in inventory to multiples of
        `multiplier`.

        ..  container:: example

            Rounds offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(3)
                >>> show(rounded_inventory, range_=(0, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(rounded_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Rounds offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(5)
                >>> show(rounded_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(rounded_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Rounds offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(
                ...     5,
                ...     anchor=Right,
                ...     )
                >>> show(rounded_inventory, range_=(-5, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(rounded_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-5, 1),
                            stop_offset=durationtools.Offset(0, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Rounds offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 2),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> rounded_inventory = timespan_inventory.round_offsets(
                ...     5,
                ...     anchor=Right,
                ...     must_be_well_formed=False,
                ...     )

            ::

                >>> f(rounded_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(0, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(5, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(5, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
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

    def scale(self, multiplier, anchor=Left):
        r'''Scales timespan by `multiplier` relative to `anchor`.

        ..  container:: example

            Scales timespans relative to timespan inventory start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 14), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.scale(2)
                >>> show(timespan_inventory, range_=(0, 14), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(9, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(14, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Scales timespans relative to timespan inventory stop offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.scale(2, anchor=Right)
                >>> show(timespan_inventory, range_=(-3, 10), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-3, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(2, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.scale(multiplier, anchor=anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def split_at_offset(self, offset):
        '''Splits timespans at `offset`.

        ..  container:: example

            Splits at offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> left, right = timespan_inventory.split_at_offset(4)

            ::

                >>> show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
                >>> f(left)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(4, 1),
                            ),
                        ]
                    )

            ::

                >>> show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
                >>> f(right)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(4, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Splits at offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> left, right = timespan_inventory.split_at_offset(6)

            ::

                >>> show(left, range_=(0, 10), scale=0.5) # doctest: +SKIP
                >>> f(left)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        ]
                    )

            ::

                >>> show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
                >>> f(right)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Splits at offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> left, right = timespan_inventory.split_at_offset(-1)

            ::

                >>> left
                TimespanInventory([])

            ::

                >>> show(right, range_=(0, 10), scale=0.5) # doctest: +SKIP
                >>> f(right)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )

        Returns inventories.
        '''
        offset = durationtools.Offset(offset)
        before_inventory = type(self)()
        during_inventory = type(self)()
        after_inventory = type(self)()
        for timespan in self:
            if timespan.stop_offset <= offset:
                before_inventory.append(timespan)
            elif offset <= timespan.start_offset:
                after_inventory.append(timespan)
            else:
                during_inventory.append(timespan)
        for timespan in during_inventory:
            before_timespan, after_timespan = timespan.split_at_offset(offset)
            before_inventory.append(before_timespan)
            after_inventory.append(after_timespan)
        before_inventory.sort()
        after_inventory.sort()
        return before_inventory, after_inventory

    def split_at_offsets(self, offsets):
        '''Splits timespans at `offsets`.

        ..  container:: example

            Splits at offsets:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(4, 10),
                ...     timespantools.Timespan(15, 20),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 20), scale=0.5) # doctest: +SKIP

            ::

                >>> offsets = [-1, 3, 6, 12, 13]
                >>> for inventory in timespan_inventory.split_at_offsets(
                ...     offsets):
                ...     show(inventory, range_=(0, 20), scale=0.5) # doctest: +SKIP
                ...     f(inventory)
                ...
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(3, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(4, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(10, 1),
                            ),
                        ]
                    )
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(15, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Splits empty inventory:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([])
                >>> timespan_inventory.split_at_offsets(offsets)
                [TimespanInventory([])]

        Returns one or more inventories.
        '''
        inventories = [self]
        if not self:
            return inventories
        offsets = sorted(set(durationtools.Offset(x) for x in offsets))
        offsets = [x for x in offsets
            if self.start_offset < x < self.stop_offset]
        for offset in offsets:
            shards = [x for x in inventories[-1].split_at_offset(offset)
                if x]
            if shards:
                inventories[-1:] = shards
        return inventories

    def stretch(self, multiplier, anchor=None):
        r'''Stretches timespans by `multiplier` relative to `anchor`.

        ..  container:: example

            Stretches timespans relative to timespan inventory start offset:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 20), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.stretch(2)
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(6, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(12, 1),
                            stop_offset=durationtools.Offset(20, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Stretches timespans relative to arbitrary anchor:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(-8, 12), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.stretch(2, anchor=Offset(8))
                >>> show(timespan_inventory, scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-8, 1),
                            stop_offset=durationtools.Offset(-2, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(-2, 1),
                            stop_offset=durationtools.Offset(4, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(4, 1),
                            stop_offset=durationtools.Offset(12, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        if anchor is None:
            anchor = self.start_offset
        for timespan in self:
            timespan = timespan.stretch(multiplier, anchor)
            timespans.append(timespan)
        self[:] = timespans
        return self

    def translate(self, translation=None):
        r'''Translates timespans by `translation`.

        ..  container:: example

            Translates timespan by offset ``50``:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 60), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.translate(50)
                >>> show(timespan_inventory, range_=(0, 60), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(50, 1),
                            stop_offset=durationtools.Offset(53, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(53, 1),
                            stop_offset=durationtools.Offset(56, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(56, 1),
                            stop_offset=durationtools.Offset(60, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        return self.translate_offsets(translation, translation)

    def translate_offsets(
        self,
        start_offset_translation=None,
        stop_offset_translation=None,
        ):
        r'''Translates timespans by `start_offset_translation`
        and `stop_offset_translation`.

        ..  container:: example

            Translates timespan start- and stop-offsets equally:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 60), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.translate_offsets(50, 50)
                >>> show(timespan_inventory, range_=(0, 60), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(50, 1),
                            stop_offset=durationtools.Offset(53, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(53, 1),
                            stop_offset=durationtools.Offset(56, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(56, 1),
                            stop_offset=durationtools.Offset(60, 1),
                            ),
                        ]
                    )

        ..  container:: example

            Translates timespan stop-offsets only:

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 3),
                ...     timespantools.Timespan(3, 6),
                ...     timespantools.Timespan(6, 10),
                ...     ])
                >>> show(timespan_inventory, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> _ = timespan_inventory.translate_offsets(
                ...     stop_offset_translation=20)
                >>> show(timespan_inventory, range_=(0, 30), scale=0.5) # doctest: +SKIP

            ::

                >>> f(timespan_inventory)
                timespantools.TimespanInventory(
                    [
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(0, 1),
                            stop_offset=durationtools.Offset(23, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(3, 1),
                            stop_offset=durationtools.Offset(26, 1),
                            ),
                        timespantools.Timespan(
                            start_offset=durationtools.Offset(6, 1),
                            stop_offset=durationtools.Offset(30, 1),
                            ),
                        ]
                    )

        Operates in place and returns timespan inventory.
        '''
        timespans = []
        for timespan in self:
            timespan = timespan.translate_offsets(
                start_offset_translation,
                stop_offset_translation,
                )
            timespans.append(timespan)
        self[:] = timespans
        return self
