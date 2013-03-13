import fractions
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools.contexttools.ContextMark import ContextMark


class TempoMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a tempo indication::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)

    ::

        >>> contexttools.TempoMark(Duration(1, 8), 52)(staff[0])
        TempoMark(Duration(1, 8), 52)(c'8)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                \tempo 8=52
                c'8
                d'8
                e'8
                f'8
            }
        >>

    ::

        >>> show(score) # doctest: +SKIP

    Tempo marks target **score** context by default.

    Initialization allows many different types of input argument structure.
    '''

    ### CLASS ATTRIBUTES ###

    _format_slot = 'opening'

    _default_positional_input_arguments = (
        (1, 8),
        68,
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools.scoretools.Score import Score
        ContextMark.__init__(self, **kwargs)

        if self.target_context is None:
            self._target_context = Score

        if len(args) == 1 and isinstance(args[0], type(self)):
            tempo_indication = args[0]
            duration = durationtools.Duration(tempo_indication.duration)
            textual_indication = tempo_indication.textual_indication
            units_per_minute = tempo_indication.units_per_minute

        elif len(args) == 1 and isinstance(args[0], str):
            duration = None
            textual_indication = args[0]
            units_per_minute = None
            assert isinstance(textual_indication, (str, type(None)))

        elif len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2:
            textual_indication = None
            duration, units_per_minute = args[0]

        elif len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 3:
            textual_indication, duration, units_per_minute = args[0]

        elif len(args) in [2, 3]:
            if len(args) == 3:
                textual_indication, duration, units_per_minute = args
            else:
                textual_indication = None
                duration, units_per_minute = args

        else:
            raise ValueError('can not initialize tempo indication.')

        assert isinstance(textual_indication, (str, type(None)))

        if duration:
            try:
                duration = durationtools.Duration(duration)
            except TypeError:
                duration = durationtools.Duration(*duration)

        assert isinstance(units_per_minute, (int, long, float, durationtools.Duration, list, tuple, type(None)))
        if isinstance(units_per_minute, (list, tuple)):
            assert len(units_per_minute) == 2
            assert all([isinstance(x, (int, long, float, durationtools.Duration)) for x in units_per_minute])
            units_per_minute = tuple(sorted(units_per_minute))

        object.__setattr__(self, '_duration', duration)
        object.__setattr__(self, '_textual_indication', textual_indication)
        object.__setattr__(self, '_units_per_minute', units_per_minute)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = self.quarters_per_minute + expr.quarters_per_minute
            minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
            nonreduced_fraction = mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_duration_denominator = nonreduced_fraction.pair
            new_duration = durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    def __copy__(self, *args):
        return type(self)(
            self.textual_indication, self.duration, self.units_per_minute,
            target_context=self.target_context)

    def __div__(self, expr):
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            result = self.quarters_per_minute / expr.quarters_per_minute
            return durationtools.Multiplier(result)
        raise TypeError('must be tempo indication.')

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.duration == expr.duration:
                if self.textual_indication == expr.textual_indication:
                    if self.units_per_minute == expr.units_per_minute:
                        return True
        return False

    def __mul__(self, multiplier):
        if isinstance(multiplier, (int, float, durationtools.Duration)):
            if self.is_imprecise:
                raise ImpreciseTempoError
            new_units_per_minute = multiplier * self.units_per_minute
            new_duration = durationtools.Duration(self.duration)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    def __sub__(self, expr):
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = self.quarters_per_minute - expr.quarters_per_minute
            minimum_denominator = min((self.duration.denominator, expr.duration.denominator))
            nonreduced_fraction = mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_duration_denominator = nonreduced_fraction.pair
            new_duration = durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    ### PRIVATE METHODS ###

    def _bind_correct_effective_context(self, correct_effective_context):
        ContextMark._bind_correct_effective_context(self, correct_effective_context)
        correct_effective_context._mark_entire_score_tree_for_later_update('seconds')

    def _bind_start_component(self, start_component):
        ContextMark._bind_start_component(self, start_component)
        self._start_component._mark_entire_score_tree_for_later_update('seconds')

    ### PRIVATE PROPERTIES ###

    @property
    def _dotted(self):
        '''Dotted numeral representation of duration.
        '''
        return self.duration.lilypond_duration_string

    @property
    def _equation(self):
        '''Dotted numeral and units per minute together around equal sign.
        '''
        if isinstance(self.units_per_minute, tuple):
            return '%s=%s~%s' % (self._dotted, self.units_per_minute[0], self.units_per_minute[1])
        return '%s=%s' % (self._dotted, self.units_per_minute)

    @property
    def _one_line_menuing_summary(self):
        return self.lilypond_format.lstrip(r'\tempo ')

    @property
    def _positional_argument_values(self):
        result = []
        if self.textual_indication:
            result.append(self.textual_indication)
        if self.duration:
            result.append(self.duration)
        if self.units_per_minute:
            result.append(self.units_per_minute)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @apply
    def duration():
        def fget(self):
            '''Get duration of tempo mark::

                >>> tempo = contexttools.TempoMark(Duration(1, 8), 52)
                >>> tempo.duration
                Duration(1, 8)

            Set duration of tempo mark::

                >>> tempo.duration = Duration(1, 4)
                >>> tempo.duration
                Duration(1, 4)

            Return duration, or None if tempo mark is imprecise.
            '''
            return self._duration
        def fset(self, duration):
            if duration is not None:
                try:
                    duration = durationtools.Duration(duration)
                except TypeError:
                    duration = durationtools.Duration(*duration)
            self._duration = duration
        return property(**locals())

    @property
    def is_imprecise(self):
        r'''True if tempo mark is entirely textual, or if tempo mark's
        units_per_minute is a range:

        ::

            >>> contexttools.TempoMark(Duration(1, 4), 60).is_imprecise
            False
            >>> contexttools.TempoMark('Langsam', 4, 60).is_imprecise
            False
            >>> contexttools.TempoMark('Langsam').is_imprecise
            True
            >>> contexttools.TempoMark('Langsam', 4, (35, 50)).is_imprecise
            True
            >>> contexttools.TempoMark(Duration(1, 4), (35, 50)).is_imprecise
            True

        Return boolean.
        '''
        if self.duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def lilypond_format(self):
        r'''Read-only LilyPond format of tempo mark:

        ::

            >>> tempo = contexttools.TempoMark(Duration(1, 8), 52)
            >>> tempo.lilypond_format
            '\\tempo 8=52'

        ::

            >>> tempo.textual_indication = 'Gingerly'
            >>> tempo.lilypond_format
            '\\tempo Gingerly 8=52'

        ::

            >>> tempo.units_per_minute = (52, 56)
            >>> tempo.lilypond_format
            '\\tempo Gingerly 8=52~56'

        Return string.
        '''
        text, equation = None, None

        if self.textual_indication is not None:
            text = schemetools.format_scheme_value(self.textual_indication)

        if self.duration is not None and self.units_per_minute is not None:
            equation = self._equation

        if text and equation:
            return r'\tempo %s %s' % (text, equation)
        elif equation:
            return r'\tempo %s' % equation
        elif text:
            return r'\tempo %s' % text
        else:
            return r'\tempo \default'

    @property
    def quarters_per_minute(self):
        r'''Read-only quarters per minute of tempo mark::

            >>> tempo = contexttools.TempoMark(Duration(1, 8), 52)
            >>> tempo.quarters_per_minute
            Fraction(104, 1)

        Return fraction.

        Or tuple if tempo mark `units_per_minute` is a range.

        Or none if tempo mark is imprecise.
        '''
        if self.is_imprecise:
            return None

        if isinstance(self.units_per_minute, tuple):
            low = durationtools.Duration(1, 4) / self.duration * self.units_per_minute[0]
            high = durationtools.Duration(1, 4) / self.duration * self.units_per_minute[1]
            return (low, high)
        result = durationtools.Duration(1, 4) / self.duration * self.units_per_minute
        return fractions.Fraction(result)

    @apply
    def textual_indication():
        def fget(self):
            r'''Get textual indication of tempo mark::

                >>> tempo = contexttools.TempoMark('Langsam', Duration(1, 8), 52)
                >>> tempo.textual_indication
                'Langsam'

            Return string or None.
            '''
            return self._textual_indication
        def fset(self, textual_indication):
            assert isinstance(textual_indication, (str, type(None)))
            self._textual_indication = textual_indication
        return property(**locals())

    @apply
    def units_per_minute():
        def fget(self):
            r'''Get units per minute of tempo mark::

                >>> tempo = contexttools.TempoMark(Duration(1, 8), 52)
                >>> tempo.units_per_minute
                52

            Set units per minute of tempo mark::

                >>> tempo.units_per_minute = 56
                >>> tempo.units_per_minute
                56

            Return number.
            '''
            return self._units_per_minute
        def fset(self, units_per_minute):
            assert isinstance(units_per_minute, (numbers.Number, list, tuple, type(None)))
            if isinstance(units_per_minute, (list, tuple)):
                assert len(units_per_minute) == 2
                assert all([isinstance(x, numbers.Number) for x in units_per_minute])
                units_per_minute = tuple(sorted(units_per_minute))
            self._units_per_minute = units_per_minute
        return property(**locals())

    ### PUBLIC METHODS ###

    def is_tempo_mark_token(self, expr):
        '''True when `expr` has the form of a tempo mark initializer::

            >>> tempo_mark = contexttools.TempoMark(Duration(1, 4), 72)
            >>> tempo_mark.is_tempo_mark_token((Duration(1, 4), 84))
            True

        Otherwise false::

            >>> tempo_mark.is_tempo_mark_token(84)
            False

        Return boolean.
        '''
        try:
            tempo_mark = type(self)(expr)
            return isinstance(tempo_mark, type(self))
        except:
            return False
