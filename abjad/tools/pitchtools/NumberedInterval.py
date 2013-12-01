# -*- encoding: utf-8 -*-
import abc
import functools
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


@functools.total_ordering
class NumberedInterval(Interval):
    '''A numbered interval.

    ::

        >>> numbered_interval = pitchtools.NumberedInterval(-14)
        >>> numbered_interval
        NumberedInterval(-14)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg=None):
        from abjad.tools import pitchtools
        if isinstance(arg, (int, float, long)):
            number = arg
        elif isinstance(arg, pitchtools.Interval):
            number = arg.semitones
        elif arg is None:
            number = 0
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, arg)
            raise TypeError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of numbered interval.

        Returns new numbered interval.
        '''
        return type(self)(abs(self._number))

    def __add__(self, arg):
        r'''Adds `arg` to numbered interval.

        Returns new numbered interval.
        '''
        if isinstance(arg, type(self)):
            number = self.number + arg.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), arg)
        raise TypeError(message)

    def __copy__(self):
        r'''Copies numbered interval.

        Returns new numbered interval.
        '''
        return type(self)(self.number)

    def __eq__(self, arg):
        r'''True when `arg` is a numbered interval with number equal to that of
        this numbered interval. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __float__(self):
        r'''Changes numbered interval to float.

        Returns float.
        '''
        return float(self._number)

    def __hash__(self):
        r'''Hashes numbered interval.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Changes numbered interval to integer.

        Returns integer.
        '''
        return int(self._number)

    def __lt__(self, arg):
        r'''True when `arg` is a numbered interval with same direction number
        as this numbered interval and with number greater than that of this
        numbered interval. Otherwise false.

        Returns boolean.
        '''
        if not isinstance(arg, type(self)):
            message = 'must be numbered interval: {!r}.'.format(arg)
            raise TypeError(message)
        if not self.direction_number == arg.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) < abs(arg.number)

    def __neg__(self):
        r'''Negates numbered interval.

        Returns new numbered interval.
        '''
        return type(self)(-self._number)

    def __str__(self):
        r'''String representation of numbered interval.

        Returns string.
        '''
        return self._format_string

    def __sub__(self, arg):
        r'''Subtracts `arg` from numbered interval.

        Returns new numbered interval.
        '''
        if isinstance(arg, type(self)):
            number = self.number - arg.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), arg)
        raise TypeError(message)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '{}{}'.format(self._direction_symbol, abs(self.number))

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            self.number,
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Makes numbered interval from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ::

            >>> pitchtools.NumberedInterval.from_pitch_carriers(
            ...     NamedPitch(-2), 
            ...     NamedPitch(12),
            ...     )
            NumberedInterval(14)

        Returns numbered interval.
        '''
        from abjad.tools import pitchtools
        # get pitches
        pitch_1 = pitchtools.get_named_pitch_from_pitch_carrier(
            pitch_carrier_1)
        pitch_2 = pitchtools.get_named_pitch_from_pitch_carrier(
            pitch_carrier_2)
        # get difference in semitones
        number = abs(pitchtools.NumberedPitch(pitch_2)) - \
            abs(pitchtools.NumberedPitch(pitch_1))
        # change 1.0, 2.0, ... into 1, 2, ...
        number = mathtools.integer_equivalent_number_to_integer(number)
        # return numbered interval
        return cls(number)

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Direction sign of numbered interval.

        ::

            >>> pitchtools.NumberedInterval(-14).direction_number
            -1

        Returns integer.
        '''
        return mathtools.sign(self.number)

    @property
    def number(self):
        r'''Number of numbered interval.

        Returns number.
        '''
        return self._number

    @property
    def numbered_interval_number(self):
        r'''Number of numbered interval.

        ::

            >>> pitchtools.NumberedInterval(-14).numbered_interval_number
            -14

        Returns integer or float.
        '''
        return self._number

    @property
    def semitones(self):
        r'''Semitones corresponding to numbered interval.

        Returns nonnegative number.
        '''
        return self.number
