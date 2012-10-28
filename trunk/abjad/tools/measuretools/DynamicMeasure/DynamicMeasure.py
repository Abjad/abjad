from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.measuretools.Measure.Measure import Measure


class DynamicMeasure(Measure):
    r'''.. versionadded:: 1.1

    Measure sets time signature dynamically to exactly equal contents duration::

        >>> measure = measuretools.DynamicMeasure("c'8 d'8 e'8")

    ::

        >>> measure
        DynamicMeasure(3/8, [c'8, d'8, e'8])

    ::

        >>> f(measure)
        {
            \time 3/8
            c'8
            d'8
            e'8
        }

    Return dynamic measure.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_denominator', '_time_signature_is_current', '_suppress_time_signature', )

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        Measure.__init__(self, time_signature=(99, 99), music=music, **kwargs)
        self._denominator = None
        self._time_signature_is_current = False
        self._suppress_time_signature = False
        self._update_time_signature()

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        return ()

    ### PRIVATE METHODS ###

    def _update_time_signature(self):
        if self.denominator:
            time_signature_pair = mathtools.NonreducedFraction(self.contents_duration)
            time_signature_pair = time_signature_pair.with_denominator(self.denominator)
        else:
            time_signature_pair = (self.contents_duration.numerator, self.contents_duration.denominator)
        time_signature = contexttools.TimeSignatureMark(time_signature_pair)
        time_signature.suppress = self.suppress_time_signature
        contexttools.detach_time_signature_marks_attached_to_component(self)
        time_signature.attach(self)
        self._time_signature_is_current = True

    ### PUBLIC PROPERTIES ###

    @apply
    def denominator():
        def fget(self):
            r'''Get explicit denominator of dynamic measure::

                >>> measure = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")

            ::

                >>> measure.denominator is None
                True

            Set explicit denominator of dynamic measure::

                >>> measure.denominator = 8

            ::

                >>> f(measure)
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
    def suppress_time_signature():
        def fget(self):
            r'''Get time signature suppression indicator::

            >>> measure = measuretools.DynamicMeasure("c'8 d'8 e'8 f'8")

        ::

            >>> f(measure)
            {
                \time 1/2
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> measure.suppress_time_signature
            False

        Set time signature suppression indicator::

            >>> measure.suppress_time_signature = True

        ::

            >>> measure.suppress_time_signature
            True

        ::

            >>> f(measure)
            {
                c'8
                d'8
                e'8
                f'8
            }

        Set boolean.
        '''
            return self._suppress_time_signature
        def fset(self, arg):
            assert isinstance(arg, (bool, type(None)))
            self._suppress_time_signature = arg
            self._update_time_signature()
        return property(**locals())

    ### PUBLIC METHODS ###

    def extend(self, expr):
        r'''Extend dynamic measure::

            >>> measure = measuretools.DynamicMeasure("c'8 d'8 e'8")

        ::

            >>> f(measure)
            {
                \time 3/8
                c'8
                d'8
                e'8
            }

        ::

            >>> measure.extend([Note("f'8"), Note("g'8")])

        ::

            >>> f(measure)
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
