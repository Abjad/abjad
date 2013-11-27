# -*- encoding: utf-8 -*-
import abc
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


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
        return type(self)(abs(self._number))

    def __add__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number + arg.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), arg)
        raise TypeError(message)

    def __copy__(self):
        return type(self)(self.number)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __float__(self):
        return float(self._number)

    def __ge__(self, arg):
        if not isinstance(arg, type(self)):
            message = 'must be numbered interval: {!r}.'.format(arg)
            raise TypeError(message)
        if not self.direction_number == arg.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) >= abs(arg.number)

    def __gt__(self, arg):
        if not isinstance(arg, type(self)):
            message = 'must be numbered interval: {!r}.'.format(arg)
            raise TypeError(message)
        if not self.direction_number == arg.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) > abs(arg.number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return int(self._number)

    def __le__(self, arg):
        if not isinstance(arg, type(self)):
            message = 'must be numbered interval: {!r}.'.format(arg)
            raise TypeError(message)
        if not self.direction_number == arg.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) <= abs(arg.number)

    def __lt__(self, arg):
        if not isinstance(arg, type(self)):
            message = 'must be numbered interval: {!r}.'.format(arg)
            raise TypeError(message)
        if not self.direction_number == arg.direction_number:
            message = 'can only compare intervals of same direction.'
            raise ValueError(message)
        return abs(self.number) < abs(arg.number)

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        return type(self)(-self._number)

    def __str__(self):
        return self._format_string

    def __sub__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number - arg.number
            return type(self)(number)
        message = 'must be {}: {!r}.'
        message = message.format(type(self), arg)
        raise TypeError(message)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self._direction_symbol, abs(self.number))

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
        '''Calculate numbered interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

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
        r'''Numeric sign:

        ::

            >>> pitchtools.NumberedInterval(-14).direction_number
            -1

        Returns integer.
        '''
        return mathtools.sign(self.number)

    @property
    def number(self):
        return self._number

    @property
    def numbered_interval_number(self):
        r'''Interval number:

        ::

            >>> pitchtools.NumberedInterval(-14).numbered_interval_number
            -14

        Returns integer or float.
        '''
        return self._number

    @property
    def semitones(self):
        return self.number
