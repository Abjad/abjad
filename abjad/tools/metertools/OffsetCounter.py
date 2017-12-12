from abjad.tools import markuptools
from abjad.tools.datastructuretools.TypedCounter import TypedCounter


class OffsetCounter(TypedCounter):
    r'''Offset counter.

    ..  container:: example

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 16),
        ...     abjad.Timespan(5, 12),
        ...     abjad.Timespan(-2, 8),
        ...     ])
        >>> timespan_operand = abjad.Timespan(6, 10)
        >>> timespans = timespans - timespan_operand
        >>> offset_counter = abjad.OffsetCounter(timespans)

        >>> abjad.f(offset_counter)
        abjad.OffsetCounter(
            {
                abjad.Offset(-2, 1): 1,
                abjad.Offset(0, 1): 1,
                abjad.Offset(5, 1): 1,
                abjad.Offset(6, 1): 3,
                abjad.Offset(10, 1): 2,
                abjad.Offset(12, 1): 1,
                abjad.Offset(16, 1): 1,
                }
            )

        >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None):
        import abjad
        TypedCounter.__init__(self, item_class=abjad.Offset)
        if items:
            for item in items:
                try:
                    self[item.start_offset] += 1
                    self[item.stop_offset] += 1
                except:
                    if hasattr(item, '_get_timespan'):
                        self[abjad.inspect(item).get_timespan().start_offset] += 1
                        self[abjad.inspect(item).get_timespan().stop_offset] += 1
                    else:
                        offset = abjad.Offset(item)
                        self[offset] += 1

    ### SPECIAL METHODS ###

    def __illustrate__(self, range_=None, scale=None):
        r'''Illustrates offset counter.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> timespan_operand = abjad.Timespan(6, 10)
            >>> timespans = timespans - timespan_operand
            >>> offset_counter = abjad.OffsetCounter(timespans)
            >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

        Returns LilyPond file.
        '''
        import abjad
        if not self:
            return markuptools.Markup.null().__illustrate__()
        if isinstance(range_, abjad.Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = min(self), max(self)
        minimum = float(abjad.Offset(minimum))
        maximum = float(abjad.Offset(maximum))
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
            offset = abjad.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = abjad.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            pieces.append(fraction)
        markup = abjad.Markup.overlay(pieces)
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        import abjad
        return abjad.Offset
