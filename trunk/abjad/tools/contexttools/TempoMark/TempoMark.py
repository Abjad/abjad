from abjad.tools import durationtools
from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools import durationtools
import numbers


class TempoMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a tempo indication::

        abjad> score = Score([])
        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score.append(staff)

    ::

        abjad> contexttools.TempoMark(Duration(1, 8), 52)(staff[0])
        TempoMark(8, 52)(c'8)

    ::

        abjad> f(score)
        \new Score <<
            \tempo 8=52
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>

    Tempo marks target **score** context by default.
    '''

    _format_slot = 'opening'

    def __init__(self, *args, **kwargs):
        from abjad.tools.scoretools.Score import Score
        ContextMark.__init__(self, **kwargs)
        if self.target_context is None:
            self._target_context = Score
        if len(args) == 1 and isinstance(args[0], type(self)):
            tempo_indication = args[0]
            duration = durationtools.Duration(tempo_indication.duration)
            units_per_minute = tempo_indication.units_per_minute
        elif len(args) == 2:
            duration, units_per_minute = args
            #assert isinstance(duration, durationtools.Duration)
            try:
                duration = durationtools.Duration(duration)
            except TypeError:
                duration = durationtools.Duration(*duration)
            assert isinstance(units_per_minute, (int, long, float, durationtools.Duration))
            #duration = duration
            units_per_minute = units_per_minute
        else:
            raise ValueError('can not initialize tempo indication.')
        object.__setattr__(self, '_duration', duration)
        object.__setattr__(self, '_units_per_minute', units_per_minute)

    ### OVERLOADS ###

    def __add__(self, expr):
        if isinstance(expr, type(self)):
            new_quarters_per_minute = self.quarters_per_minute + expr.quarters_per_minute
            minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
            new_units_per_minute, new_duration_denominator = \
                durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                new_quarters_per_minute / 4, minimum_denominator)
            new_duration = durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    def __copy__(self, *args):
        return type(self)(self.duration, self.units_per_minute, target_context = self.target_context)

    def __div__(self, expr):
        if isinstance(expr, type(self)):
            return self.quarters_per_minute / expr.quarters_per_minute
        raise TypeError('must be tempo indication.')

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.duration == expr.duration:
                if self.units_per_minute == expr.units_per_minute:
                    return True
        return False

    def __mul__(self, multiplier):
        if isinstance(multiplier, (int, float, durationtools.Duration)):
            new_units_per_minute = multiplier * self.units_per_minute
            new_duration = durationtools.Duration(self.duration)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    def __sub__(self, expr):
        if isinstance(expr, type(self)):
            new_quarters_per_minute = self.quarters_per_minute - expr.quarters_per_minute
            minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
            new_units_per_minute, new_duration_denominator = \
                durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                new_quarters_per_minute / 4, minimum_denominator)
            new_duration = durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return '%s, %s' % (self._dotted, self.units_per_minute)

    @property
    def _dotted(self):
        '''Dotted numeral representation of duration.'''
        return durationtools.assignable_rational_to_lilypond_duration_string(self.duration)

    @property
    def _equation(self):
        '''Dotted numeral and units per minute together around equal sign.'''
        return '%s=%s' % (self._dotted, self.units_per_minute)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def duration():
        def fget(self):
            '''Get duration of tempo mark::

                abjad> tempo = contexttools.TempoMark(Duration(1, 8), 52)
                abjad> tempo.duration
                Duration(1, 8)

            Set duration of tempo mark::

                abjad> tempo.duration = Duration(1, 4)
                abjad> tempo.duration
                Duration(1, 4)

            Return duration.
            '''
            return self._duration
        def fset(self, duration):
            try:
                duration = durationtools.Duration(duration)
            except TypeError:
                duration = durationtools.Duration(*duration)
            self._duration = duration
        return property(**locals())

    @property
    def format(self):
        r'''Read-only LilyPond format of tempo mark:

        ::

            abjad> tempo = contexttools.TempoMark(Duration(1, 8), 52)
            abjad> tempo.format
            '\\tempo 8=52'

        Return string.
        '''
        return r'\tempo %s' % self._equation

    @property
    def quarters_per_minute(self):
        r'''Read-only quarters per minute of tempo mark::

            abjad> tempo = contexttools.TempoMark(Duration(1, 8), 52)
            abjad> tempo.quarters_per_minute
            Duration(104, 1)

        Return fraction.
        '''
        return durationtools.Duration(1, 4) / self.duration * self.units_per_minute

    @apply
    def units_per_minute():
        def fget(self):
            r'''Get units per minute of tempo mark::

                abjad> tempo = contexttools.TempoMark(Duration(1, 8), 52)
                abjad> tempo.units_per_minute
                52

            Set units per minute of tempo mark::

                abjad> tempo.units_per_minute = 56
                abjad> tempo.units_per_minute
                56

            Return number.
            '''
            return self._units_per_minute
        def fset(self, units_per_minute):
            assert isinstance(units_per_minute, numbers.Number)
            self._units_per_minute = units_per_minute
        return property(**locals())
