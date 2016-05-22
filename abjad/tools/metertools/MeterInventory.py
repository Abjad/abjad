# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import markuptools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.datastructuretools.TypedList import TypedList


class MeterInventory(TypedList):
    r'''An ordered list of meters.

    ..  container:: example

        ::

            >>> meter_inventory = metertools.MeterInventory([
            ...     (3, 4), (5, 16), (7, 8),
            ...     ])
            >>> print(format(meter_inventory))
            metertools.MeterInventory(
                [
                    metertools.Meter(
                        '(3/4 (1/4 1/4 1/4))'
                        ),
                    metertools.Meter(
                        '(5/16 ((3/16 (1/16 1/16 1/16)) (2/16 (1/16 1/16))))'
                        ),
                    metertools.Meter(
                        '(7/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8)) (2/8 (1/8 1/8))))'
                        ),
                    ]
                )

        ::

            >>> show(meter_inventory, scale=0.5) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __illustrate__(self, denominator=16, range_=None, scale=None):
        r'''Illustrates meter inventory.

        ..  container:: example

            ::

                >>> meter_inventory = metertools.MeterInventory([
                ...     (3, 4), (5, 16), (7, 8),
                ...     ])
                >>> show(meter_inventory, scale=0.5) # doctest: +SKIP

            ..  doctest

                >>> illustration = meter_inventory.__illustrate__()
                >>> print(format(illustration))
                % ...
                <BLANKLINE>
                \version "..."
                \language "english"
                <BLANKLINE>
                \header {
                    tagline = ##f
                }
                <BLANKLINE>
                \layout {}
                <BLANKLINE>
                \paper {}
                <BLANKLINE>
                \markup {
                    \column
                        {
                            \combine
                                \combine
                                    \translate
                                        #'(1.0 . 1)
                                        \sans
                                            \fontsize
                                                #-3
                                                \center-align
                                                    \fraction
                                                        3
                                                        4
                                    \translate
                                        #'(49.387... . 1)
                                        \sans
                                            \fontsize
                                                #-3
                                                \center-align
                                                    \fraction
                                                        5
                                                        16
                                \translate
                                    #'(69.548... . 1)
                                    \sans
                                        \fontsize
                                            #-3
                                            \center-align
                                                \fraction
                                                    7
                                                    8
                            \combine
                                \postscript
                                    #"
                                    0.2 setlinewidth
                                    1 0.5 moveto
                                    49.387... 0.5 lineto
                                    stroke
                                    1 1.25 moveto
                                    1 -0.25 lineto
                                    stroke
                                    49.387... 1.25 moveto
                                    49.387... -0.25 lineto
                                    stroke
                                    49.387... 0.5 moveto
                                    69.548... 0.5 lineto
                                    stroke
                                    49.387... 1.25 moveto
                                    49.387... -0.25 lineto
                                    stroke
                                    69.548... 1.25 moveto
                                    69.548... -0.25 lineto
                                    stroke
                                    69.548... 0.5 moveto
                                    126 0.5 lineto
                                    stroke
                                    69.548... 1.25 moveto
                                    69.548... -0.25 lineto
                                    stroke
                                    126 1.25 moveto
                                    126 -0.25 lineto
                                    stroke
                                    "
                                \postscript
                                    #"
                                    1 -2 moveto
                                    0 -6.153... rlineto
                                    stroke
                                    5.032... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    9.064... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    13.096... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    17.129... -2 moveto
                                    0 -4.615... rlineto
                                    stroke
                                    21.161... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    25.193... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    29.225... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    33.258... -2 moveto
                                    0 -4.615... rlineto
                                    stroke
                                    37.290... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    41.322... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    45.354... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    49.387... -2 moveto
                                    0 -6.153... rlineto
                                    stroke
                                    49.387... -2 moveto
                                    0 -10.909... rlineto
                                    stroke
                                    53.419... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    57.451... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    61.483... -2 moveto
                                    0 -7.272... rlineto
                                    stroke
                                    65.516... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    69.548... -2 moveto
                                    0 -10.909... rlineto
                                    stroke
                                    69.548... -2 moveto
                                    0 -5.517... rlineto
                                    stroke
                                    73.580... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    77.612... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    81.645... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    85.677... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    89.709... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    93.741... -2 moveto
                                    0 -4.137... rlineto
                                    stroke
                                    97.774... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    101.806... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    105.838... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    109.870... -2 moveto
                                    0 -4.137... rlineto
                                    stroke
                                    113.903... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    117.935... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    121.967... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    126 -2 moveto
                                    0 -5.517... rlineto
                                    stroke
                                    "
                        }
                    }


        Returns LilyPond file.
        '''
        from abjad.tools import metertools
        durations = [_.duration for _ in self]
        total_duration = sum(durations)
        offsets = mathtools.cumulative_sums(durations, start=0)
        timespan_inventory = timespantools.TimespanInventory()
        for one, two in sequencetools.iterate_sequence_nwise(offsets):
            timespan = timespantools.Timespan(
                start_offset=one,
                stop_offset=two,
                )
            timespan_inventory.append(timespan)

        if range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = 0, total_duration
        minimum = float(durationtools.Offset(minimum))
        maximum = float(durationtools.Offset(maximum))
        if scale is None:
            scale = 1.
        assert 0 < scale
        postscript_scale = 125. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        timespan_markup = timespan_inventory._make_timespan_inventory_markup(
            timespan_inventory,
            postscript_x_offset,
            postscript_scale,
            draw_offsets=False,
            )
        ps = markuptools.Postscript()
        rational_x_offset = durationtools.Offset(0)
        for meter in self:
            kernel_denominator = denominator or meter.denominator
            kernel = metertools.MetricAccentKernel.from_meter(
                meter, kernel_denominator)
            for offset, weight in sorted(kernel.kernel.items()):
                weight = float(weight) * -40
                ps_x_offset = float(rational_x_offset + offset)
                ps_x_offset *= postscript_scale
                ps_x_offset += 1
                ps = ps.moveto(ps_x_offset, -2)
                ps = ps.rlineto(0, weight)
                ps = ps.stroke()
            rational_x_offset += meter.duration
        ps = markuptools.Markup.postscript(ps)
        lines_markup = markuptools.Markup.combine(timespan_markup, ps)
        fraction_markups = []
        for meter, offset in zip(self, offsets):
            numerator, denominator = meter.numerator, meter.denominator
            fraction = markuptools.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            fraction_markups.append(fraction)
        fraction_markup = fraction_markups[0]
        for markup in fraction_markups[1:]:
            fraction_markup = markuptools.Markup.combine(
                fraction_markup, markup)
        markup = markuptools.Markup.column([fraction_markup, lines_markup])
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import metertools
        return metertools.Meter
