from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.measuretools.Measure.Measure import Measure


class DynamicMeasure(Measure):
    r'''.. versionadded:: 1.1

    Measure sets meter dynamically to exactly equal contents duration::

        abjad> measure = measuretools.DynamicMeasure("c'8 d'8 e'8")

    ::

        abjad> measure
        DynamicMeasure(3/8, [c'8, d'8, e'8])

    ::

        abjad> f(measure)
        {
            \time 3/8
            c'8
            d'8
            e'8
        }

    Return dynamic measure.
    '''

    __slots__ = ('_denominator', '_time_signature_is_current', '_suppress_meter', )

    def __init__(self, music = None, **kwargs):
        Measure.__init__(self, meter = (99, 99), music = music, **kwargs)
        self._denominator = None
        self._time_signature_is_current = False
        self._suppress_meter = False
        self._update_time_signature()

    ### OVERLOADS ###

    def __getnewargs__(self):
        return ()

    ### PRIVATE METHODS ###

    def _update_time_signature(self):
        if self.denominator:
            meter_pair = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                self.contents_duration, self.denominator)
        else:
            meter_pair = (self.contents_duration.numerator, self.contents_duration.denominator)
        meter = contexttools.TimeSignatureMark(meter_pair)
        meter.suppress = self.suppress_meter
        contexttools.detach_time_signature_marks_attached_to_component(self)
        meter.attach(self)
        self._time_signature_is_current = True

    ### PUBLIC ATTRIBUTES ###

    @apply
    def denominator():
        def fget(self):
            r'''Get explicit denominator of dynamic measure::

                abjad> measure = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")

            ::

                abjad> measure.denominator is None
                True

            Set explicit denominator of dynamic measure::

                abjad> measure.denominator = 8

            ::

                abjad> f(measure)
                {
                    \time 4/8
                    c'8
                    d'8
                    e'8
                    f'8
                }

            Set positive integer or none.
            '''
            return self._denominator
        def fset(self, arg):
            assert isinstance(arg, (int, long, type(None)))
            self._denominator = arg
            self._update_time_signature()
        return property(**locals())

    @property
    def preprolated_duration(self):
        return self.contents_duration

    @apply
    def suppress_meter():
        def fget(self):
            r'''Get meter suppression indicator::

            abjad> measure = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")

        ::

            abjad> f(measure)
            {
                \time 1/2
                c'8
                d'8
                e'8
                f'8
            }

        ::

            abjad> measure.suppress_meter
            False

        Set meter suppression indicator::

            abjad> measure.suppress_meter = True

        ::

            abjad> measure.suppress_meter
            True

        ::

            abjad> f(measure)
            {
                c'8
                d'8
                e'8
                f'8
            }

        Set boolean.
        '''
            return self._suppress_meter
        def fset(self, arg):
            assert isinstance(arg, (bool, type(None)))
            self._suppress_meter = arg
            self._update_time_signature()
        return property(**locals())

    ### PUBLIC METHODS ###

    def extend(self, expr):
        r'''Extend dynamic measure::

            abjad> measure = measuretools.DynamicMeasure("c'8 d'8 e'8")

        ::

            abjad> f(measure)
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

        ::

            abjad> measure.extend([Note("f'8"), Note("g'8")])

        ::

            abjad> f(measure)
            {
                \time 5/8
                c'8
                d'8
                e'8
                f'8
                g'8
            }

        Return none.
        '''
        Measure.extend(self, expr)
        self._update_time_signature()
