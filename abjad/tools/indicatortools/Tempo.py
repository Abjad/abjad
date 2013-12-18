# -*- encoding: utf-8 -*-
import fractions
import functools
import math
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools.abctools.AbjadObject import AbjadObject


@functools.total_ordering
class Tempo(AbjadObject):
    r'''A tempo indication.

    ::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> tempo = Tempo(Duration(1, 8), 52)
        >>> attach(tempo, staff[0])
        >>> show(score) # doctest: +SKIP

    ..  doctest::

        >>> print format(score)
        \new Score <<
            \new Staff {
                \tempo 8=52
                c'8
                d'8
                e'8
                f'8
            }
        >>

    Tempo indications are scoped to the **score context** by default.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        (1, 8),
        68,
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score
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
        elif len(args) == 1 and isinstance(args[0], tuple) and \
            len(args[0]) == 2:
            textual_indication = None
            duration, units_per_minute = args[0]
        elif len(args) == 1 and isinstance(args[0], tuple) and \
            len(args[0]) == 3:
            textual_indication, duration, units_per_minute = args[0]
        elif len(args) in [2, 3]:
            if len(args) == 3:
                textual_indication, duration, units_per_minute = args
            else:
                textual_indication = None
                duration, units_per_minute = args
        else:
            message = 'can not initialize tempo indication.'
            raise ValueError(message)
        assert isinstance(textual_indication, (str, type(None)))
        if duration:
            try:
                duration = durationtools.Duration(duration)
            except TypeError:
                duration = durationtools.Duration(*duration)
        assert isinstance(units_per_minute, (int, long, float, 
            durationtools.Duration, list, tuple, type(None)))
        if isinstance(units_per_minute, (list, tuple)):
            assert len(units_per_minute) == 2
            assert all(
                isinstance(x, (int, long, float, durationtools.Duration)) 
                for x in units_per_minute)
            units_per_minute = tuple(sorted(units_per_minute))
        self._duration = duration
        self._textual_indication = textual_indication
        self._units_per_minute = units_per_minute

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds tempo to `expr`.

        Returns new tempo.
        '''
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = \
                self.quarters_per_minute + expr.quarters_per_minute
            minimum_denominator = \
                min((self.duration.denominator, expr.duration.denominator))
            nonreduced_fraction = \
                mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = \
                nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_duration_denominator = \
                nonreduced_fraction.pair
            new_duration = \
                durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = \
                type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    def __copy__(self, *args):
        r'''Copies tempo.

        Returns new tempo.
        '''
        return type(self)(
            self.textual_indication, 
            self.duration, 
            self.units_per_minute,
            )

    def __div__(self, expr):
        r'''Divides tempo by `expr`.

        Returns new tempo.
        '''
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            result = self.quarters_per_minute / expr.quarters_per_minute
            return durationtools.Multiplier(result)
        message = 'must be tempo indication.'
        raise TypeError(message)

    def __eq__(self, expr):
        r'''True when `expr` is a tempo with duration, textual indication
        and units-per-minute all equal to this tempo. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.duration == expr.duration:
                if self.textual_indication == expr.textual_indication:
                    if self.units_per_minute == expr.units_per_minute:
                        return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats tempo.

        Set `format_specification` to `''`', `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> tempo = Tempo('Allegro', (1, 4), 84)
            >>> print format(tempo)
            indicatortools.Tempo(
                'Allegro',
                durationtools.Duration(1, 4),
                84
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __lt__(self, arg):
        r'''True when `arg` is a tempo with quarters per minute greater than
        that of this tempo. Otherwise false.

        Returns boolean.
        '''
        assert isinstance(arg, type(self)), repr(arg)
        return self.quarters_per_minute < arg.quarters_per_minute

    def __mul__(self, multiplier):
        r'''Multiplies tempo by `multiplier`.

        ::

            >>> tempo = Tempo(Duration(1, 4), 84)
            >>> tempo * 2
            Tempo(Duration(1, 4), 168)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_duration = durationtools.Duration(self.duration)
        new_tempo = type(self)(new_duration, new_units_per_minute)
        return new_tempo

    def __rmul__(self, multiplier):
        r'''Multiplies `multiplier` by tempo.

        ::

            >>> tempo = Tempo(Duration(1, 4), 84)
            >>> 2 * tempo
            Tempo(Duration(1, 4), 168)

        Returns new tempo.
        '''
        if not isinstance(multiplier, (int, float, durationtools.Duration)):
            return
        if self.is_imprecise:
            raise ImpreciseTempoError
        new_units_per_minute = multiplier * self.units_per_minute
        new_duration = durationtools.Duration(self.duration)
        new_tempo = type(self)(new_duration, new_units_per_minute)
        return new_tempo

    def __str__(self):
        r'''String representation of tempo.

        ::

            >>> str(tempo)
            '4=84'

        Returns string.
        '''
        return self._equation or self.textual_indication

    def __sub__(self, expr):
        r'''Subtracts `expr` from tempo.

        ::

            >>> tempo - 20

        Returns new tempo.
        '''
        if isinstance(expr, type(self)):
            if self.is_imprecise or expr.is_imprecise:
                raise ImpreciseTempoError
            new_quarters_per_minute = \
                self.quarters_per_minute - expr.quarters_per_minute
            minimum_denominator = \
                min((self.duration.denominator, expr.duration.denominator))
            nonreduced_fraction = \
                mathtools.NonreducedFraction(new_quarters_per_minute / 4)
            nonreduced_fraction = \
                nonreduced_fraction.with_denominator(minimum_denominator)
            new_units_per_minute, new_duration_denominator = \
                nonreduced_fraction.pair
            new_duration = \
                durationtools.Duration(1, new_duration_denominator)
            new_tempo_indication = \
                type(self)(new_duration, new_units_per_minute)
            return new_tempo_indication

    ### PRIVATE PROPERTIES ###

    @property
    def _dotted(self):
        return self.duration.lilypond_duration_string

    @property
    def _equation(self):
        if self.duration is None:
            return
        if isinstance(self.units_per_minute, tuple):
            return '{}={}-{}'.format(
                self._dotted, 
                self.units_per_minute[0], 
                self.units_per_minute[1],
                )
        return '{}={}'.format(self._dotted, self.units_per_minute)

    @property
    def _lilypond_format(self):
        text, equation = None, None
        if self.textual_indication is not None:
            text = schemetools.Scheme.format_scheme_value(
                self.textual_indication)
        if self.duration is not None and self.units_per_minute is not None:
            equation = self._equation
        if text and equation:
            return r'\tempo {} {}'.format(text, equation)
        elif equation:
            return r'\tempo {}'.format(equation)
        elif text:
            return r'\tempo {}'.format(text)
        else:
            return r'\tempo \default'

    @property
    def _one_line_menuing_summary(self):
        return self._lilypond_format.lstrip(r'\tempo ')

    @property
    def _repr_specification(self):
        return self._storage_format_specification.__makenew__(
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        if self.textual_indication:
            positional_argument_values.append(self.textual_indication)
        if self.duration:
            positional_argument_values.append(self.duration)
        if self.units_per_minute:
            positional_argument_values.append(self.units_per_minute)
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###


    @property
    def duration(self):
        r'''Duration of tempo.

        ::

            >>> tempo.duration
            Duration(1, 4)

        Returns duration.
        '''
        return self._duration

    @property
    def is_imprecise(self):
        r'''True if tempo is entirely textual or if tempo's
        units_per_minute is a range.

        ::

            >>> Tempo(Duration(1, 4), 60).is_imprecise
            False
            >>> Tempo('Langsam', 4, 60).is_imprecise
            False
            >>> Tempo('Langsam').is_imprecise
            True
            >>> Tempo('Langsam', 4, (35, 50)).is_imprecise
            True
            >>> Tempo(Duration(1, 4), (35, 50)).is_imprecise
            True

        Otherwise false:

        ::

            >>> Tempo(Duration(1, 4), 60).is_imprecise
            False

        Returns boolean.
        '''
        if self.duration is not None:
            if self.units_per_minute is not None:
                if not isinstance(self.units_per_minute, tuple):
                    return False
        return True

    @property
    def quarters_per_minute(self):
        r'''Quarters per minute of tempo.

        ::

            >>> tempo = Tempo(Duration(1, 8), 52)
            >>> tempo.quarters_per_minute
            Fraction(104, 1)

        Returns tuple when tempo `units_per_minute` is a range.

        Returns none when tempo is imprecise.

        Returns fraction otherwise.
        '''
        if self.is_imprecise:
            return None
        if isinstance(self.units_per_minute, tuple):
            low = durationtools.Duration(1, 4) / self.duration * \
                self.units_per_minute[0]
            high = durationtools.Duration(1, 4) / self.duration * \
                self.units_per_minute[1]
            return (low, high)
        result = durationtools.Duration(1, 4) / self.duration * \
            self.units_per_minute
        return fractions.Fraction(result)

    @property
    def textual_indication(self):
        r'''Optional textual indication of tempo.

        ::

            >>> tempo.textual_indication is None
            True

        Returns string or none.
        '''
        return self._textual_indication

    @property
    def units_per_minute(self):
        r'''Units per minute of tempo.

        ::

            >>> tempo.units_per_minute
            52

        Returns number.
        '''
        return self._units_per_minute

    ### PUBLIC METHODS ###

    def duration_to_milliseconds(self, duration):
        r'''Millisecond value of `duration` under a given tempo.

        ::

            >>> duration = (1, 4)
            >>> tempo = Tempo((1, 4), 60)
            >>> tempo.duration_to_milliseconds(duration)
            Duration(1000, 1)

        Returns duration.
        '''
        duration = durationtools.Duration(duration)
        whole_note_duration = 1000 \
            * durationtools.Multiplier(
                self.duration.denominator, 
                self.duration.numerator,
                ) \
            * durationtools.Multiplier(
                60, 
                self.units_per_minute,
                )
        return durationtools.Duration(duration * whole_note_duration)

    def is_tempo_token(self, expr):
        r'''True when `expr` can initialize tempo.

        ::

            >>> tempo = Tempo(Duration(1, 4), 72)
            >>> tempo.is_tempo_token((Duration(1, 4), 84))
            True

        Otherwise false:

        ::

            >>> tempo.is_tempo_token(84)
            False

        Returns boolean.
        '''
        try:
            tempo = type(self)(expr)
            return isinstance(tempo, type(self))
        except:
            return False

    def list_related_tempos(
        self, 
        maximum_numerator=None, 
        maximum_denominator=None,
        ):
        r'''Lists tempos related to this tempo.

        Returns list of tempo / ratio pairs.

        Each new tempo equals not less than half of this tempo
        and not more than twice this tempo.

        ..  container:: example

            Rewrites tempo ``58`` MM by ratios of the form ``n:d`` such that 
            ``1 <= n <= 8`` and ``1 <= d <= 8``:
            ...

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=8, 
                ...     maximum_denominator=8,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print string
                4=29    1:2
                4=58    1:1
                4=87    3:2
                4=116   2:1

        ..  container:: example

            Rewrites tempo ``58`` MM by ratios of the form ``n:d`` such that
            ``1 <= n <= 30`` and ``1 <= d <= 30``:

            ::

                >>> tempo = Tempo(Duration(1, 4), 58)
                >>> pairs = tempo.list_related_tempos(
                ...     maximum_numerator=30, 
                ...     maximum_denominator=30,
                ...     )

            ::

                >>> for tempo, ratio in pairs:
                ...     string = '{!s}\t{!s}'.format(tempo, ratio)
                ...     print string
                ...
                4=30    15:29
                4=32    16:29
                4=34    17:29
                4=36    18:29
                4=38    19:29
                4=40    20:29
                4=42    21:29
                4=44    22:29
                4=46    23:29
                4=48    24:29
                4=50    25:29
                4=52    26:29
                4=54    27:29
                4=56    28:29
                4=58    1:1
                4=60    30:29

        Returns list.
        '''
        # assert integer tempo
        assert isinstance(self.units_per_minute, int), repr(self)
        # find divisors
        divisors = mathtools.divisors(self.units_per_minute)
        if maximum_denominator is not None:
            divisors = [x for x in divisors if x <= maximum_denominator]
        # make pairs
        pairs = []
        for divisor in divisors:
            start = int(math.ceil(divisor / 2.0))
            stop = 2 * divisor
            numerators = range(start, stop + 1)
            if maximum_numerator is not None:
                    numerators = [
                        x for x in numerators 
                        if x <= maximum_numerator
                        ]
        for numerator in numerators:
                ratio = mathtools.Ratio(numerator, divisor)
                multiplier = durationtools.Multiplier(*ratio)
                new_units_per_minute = multiplier * self.units_per_minute
                assert mathtools.is_integer_equivalent_expr(
                    new_units_per_minute)
                new_units_per_minute = int(new_units_per_minute)
                new_tempo = type(self)(self.duration, new_units_per_minute)
                pair = (new_tempo, ratio)
                if pair not in pairs:
                    pairs.append(pair)
        # sort pairs
        pairs.sort()
        # return pairs
        return pairs

    def rewrite_duration(self, duration, new_tempo):
        r'''Rewrite `duration` under `new_tempo`.

        Given `duration` governed by this tempo
        return new duration governed by `new_tempo`.

        Ensure that `duration` and new duration
        consume the same amount of time in seconds.

        ..  container:: example

            Consider the two tempo indications below. 
            
            ::

                >>> tempo = Tempo(Duration(1, 4), 60)
                >>> new_tempo = Tempo(Duration(1, 4), 90)

            `tempo` specifies quarter equal to ``60 MM``.

            `new_tempo` indication specifies quarter equal to ``90 MM``.

            `new_tempo` is ``3/2`` times as fast as `tempo`:

            ::

                >>> new_tempo / tempo
                Multiplier(3, 2)

            Note that a triplet eighth note under `tempo` equals a regular 
            eighth note under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 12), new_tempo)
                Duration(1, 8)

            And note that a regular eighth note under `tempo` equals a dotted
            sixteenth under `new_tempo`:

            ::

                >>> tempo.rewrite_duration(Duration(1, 8), new_tempo)
                Duration(3, 16)

        Returns duration.
        '''
        tempo_ratio = new_tempo / self
        new_duration = tempo_ratio * duration
        return new_duration
