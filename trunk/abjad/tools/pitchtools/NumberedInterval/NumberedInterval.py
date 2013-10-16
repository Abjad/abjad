# -*- encoding: utf-8 -*-
import abc
from abjad.tools import mathtools
from abjad.tools.pitchtools.Interval import Interval


class NumberedInterval(Interval):
    '''Abjad model of a numbered interval:

    ::

        >>> numbered_interval = pitchtools.NumberedInterval(-14)
        >>> numbered_interval
        NumberedInterval(-14)

    Return numbered interval.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        from abjad.tools import pitchtools
        if isinstance(arg, (int, float, long)):
            number = arg
        elif isinstance(arg, pitchtools.Interval):
            number = arg.semitones
        else:
            raise TypeError('%s must be number or interval.' % arg)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __add__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number + arg.number
            return type(self)(number)
        raise TypeError('must be %s.'% type(self))

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
            raise TypeError('%s must be melodic chromatic interval.' % arg)
        if not self.direction_number == arg.direction_number:
            raise ValueError(
                'can only compare melodic intervals of same direction.')
        return abs(self.number) >= abs(arg.number)

    def __gt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic chromatic interval.' % arg)
        if not self.direction_number == arg.direction_number:
            raise ValueError(
                'can only compare melodic intervals of same direction.')
        return abs(self.number) > abs(arg.number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return int(self._number)

    def __le__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic chromatic interval.' % arg)
        if not self.direction_number == arg.direction_number:
            raise ValueError(
                'can only compare melodic intervals of same direction.')
        return abs(self.number) <= abs(arg.number)

    def __lt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError('%s must be melodic chromatic interval.' % arg)
        if not self.direction_number == arg.direction_number:
            raise ValueError(
                'can only compare melodic intervals of same direction.')
        return abs(self.number) < abs(arg.number)

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        return type(self)(-self._number)

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return self._format_string

    def __sub__(self, arg):
        if isinstance(arg, type(self)):
            number = self.number - arg.number
            return type(self)(number)
        raise TypeError('must be %s' % type(self))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self._direction_symbol, abs(self.number))

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic chromatic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NumberedInterval.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            NumberedInterval(+14)

        Return melodic chromatic interval.
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
        # return melodic chromatic interval
        return cls(number)

    ### PUBLIC PROPERTIES ###

    @property
    def numbered_interval_number(self):
        r'''Chromatic interval number:

        ::

            >>> pitchtools.NumberedInterval(-14).numbered_interval_number
            -14

        Return integer or float.
        '''
        return self._number

    @property
    def direction_number(self):
        r'''Numeric sign:

        ::

            >>> pitchtools.NumberedInterval(-14).direction_number
            -1

        Return integer.
        '''
        return mathtools.sign(self.number)

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        return self.number
