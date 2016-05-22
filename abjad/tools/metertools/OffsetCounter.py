# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools.datastructuretools.TypedCounter import TypedCounter


class OffsetCounter(TypedCounter):
    r'''An offset counter.

    ..  container:: example

        ::

            >>> timespan_inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 16),
            ...     timespantools.Timespan(5, 12),
            ...     timespantools.Timespan(-2, 8),
            ...     ])
            >>> timespan_operand = timespantools.Timespan(6, 10)
            >>> timespan_inventory = timespan_inventory - timespan_operand
            >>> offset_counter = metertools.OffsetCounter(timespan_inventory)
            >>> print(format(offset_counter))
            metertools.OffsetCounter(
                {
                    durationtools.Offset(-2, 1): 1,
                    durationtools.Offset(0, 1): 1,
                    durationtools.Offset(5, 1): 1,
                    durationtools.Offset(6, 1): 3,
                    durationtools.Offset(10, 1): 2,
                    durationtools.Offset(12, 1): 1,
                    durationtools.Offset(16, 1): 1,
                    }
                )

        ::

            >>> show(offset_counter, scale=0.5) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None):
        TypedCounter.__init__(self, item_class=durationtools.Offset)
        if items:
            for item in items:
                if hasattr(item, 'start_offset') and \
                    hasattr(item, 'stop_offset'):
                    self[item.start_offset] += 1
                    self[item.stop_offset] += 1
                elif hasattr(item, '_get_timespan'):
                    self[item._get_timespan().start_offset] += 1
                    self[item._get_timespan().stop_offset] += 1
                else:
                    offset = durationtools.Offset(item)
                    self[offset] += 1

    ### SPECIAL METHODS ###

    def __illustrate__(self, range_=None, scale=None):
        r'''Illustrates offset counter.

        ..  container:: example

            ::

                >>> timespan_inventory = timespantools.TimespanInventory([
                ...     timespantools.Timespan(0, 16),
                ...     timespantools.Timespan(5, 12),
                ...     timespantools.Timespan(-2, 8),
                ...     ])
                >>> timespan_operand = timespantools.Timespan(6, 10)
                >>> timespan_inventory = timespan_inventory - timespan_operand
                >>> offset_counter = metertools.OffsetCounter(
                ...     timespan_inventory,
                ...     )
                >>> show(offset_counter, scale=0.5) # doctest: +SKIP

            ..  doctest::

                >>> illustration = offset_counter.__illustrate__()

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
            minimum, maximum = min(self), max(self)
        minimum = float(durationtools.Offset(minimum))
        maximum = float(durationtools.Offset(maximum))
        if scale is None:
            scale = 1.
        assert 0 < scale
        postscript_scale = 150. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        ps = markuptools.Postscript()
        ps = ps.setlinewidth(0.2)
        ps = ps.setdash([2, 1])
        for offset, count in sorted(self.items()):
            offset = (float(offset) * postscript_scale)
            offset -= postscript_x_offset
            ps = ps.moveto(offset, -1)
            ps = ps.rlineto(0, (float(count) * -3) + 1)
            ps = ps.stroke()
        markup = markuptools.Markup.postscript(ps)
        pieces = [markup]
        for offset in sorted(self):
            offset = durationtools.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = markuptools.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            pieces.append(fraction)
        markup = markuptools.Markup.overlay(pieces)
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import durationtools
        return durationtools.Offset
