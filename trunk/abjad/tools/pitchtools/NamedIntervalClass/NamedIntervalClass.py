# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NamedIntervalClass(IntervalClass):
    '''Abjad model of named interval-class:

    ::

        >>> pitchtools.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')

    Return named interval-class.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if len(args) == 1 and\
            isinstance(args[0], (pitchtools.NamedInterval,
                pitchtools.NamedIntervalClass)):
            quality_string = args[0]._quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = pitchtools.Interval._interval_name_abbreviation_regex.match(
                args[0])
            if match is None:
                raise ValueError(
                    '{!r} does not have the form of an abbreviation.'.format(
                    args[0]))
            direction_string, quality_abbreviation, number_string = \
                match.groups()
            quality_string = \
                NamedIntervalClass._quality_abbreviation_to_quality_string[
                    quality_abbreviation]
            number = int(direction_string + number_string)
        elif len(args) == 1 and sequencetools.is_pair(args[0]):
            quality_string, number = args[0]
        elif len(args) == 2:
            quality_string, number = args
        else:
            raise TypeError('what type of instance is this?, {!r}'.format(
                args))
        if quality_string not in \
            NamedIntervalClass._acceptable_quality_strings:
            raise ValueError('not acceptable quality string.')
        if not isinstance(number, int):
            raise TypeError('must be integer.')
        if number == 0:
            raise ValueError('must be nonzero.')
        sign = mathtools.sign(number)
        abs_number = abs(number)
        if abs_number % 7 == 1 and 8 <= abs_number:
            number = 8
        else:
            number = abs_number % 7
            if number == 0:
                number = 7
        if not number == 1:
            number *= sign
        self._number = number
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.direction_number == arg.direction_number:
                if self._quality_string == arg._quality_string:
                    if self.number == arg.number:
                        return True
        return False

    def __float__(self):
        return float(self._number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return self._number

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, str(self))

    def __str__(self):
        return '{}{}{}'.format(
            self.direction_symbol,
            self._quality_abbreviation, 
            abs(self.number),
            )

    ### PRIVATE PROPERTIES ###

    _acceptable_quality_strings = (
        'perfect', 
        'major', 
        'minor', 
        'diminished', 
        'augmented',
        )

    @property
    def _format_string(self):
        return '{}{}'.format(
            self.direction_symbol, 
            abs(self.number),
            )

    @property
    def _full_name(self):
        strings = []
        if self.direction_word:
            strings.append(self.direction_word)
        strings.extend([self._quality_string, self._interval_string])
        return ' '.join(strings)

    _interval_number_to_interval_string = {
        1: 'unison', 
        2: 'second',
        3: 'third', 
        4: 'fourth', 
        5: 'fifth', 
        6: 'sixth',
        7: 'seventh', 
        8: 'octave',
        }

    _quality_abbreviation_to_quality_string = {
        'M': 'major', 
        'm': 'minor', 
        'P': 'perfect', 
        'aug': 'augmented', 
        'dim': 'diminished',
        }

    _quality_string_to_quality_abbreviation = {
        'major': 'M', 
        'minor': 'm', 
        'perfect': 'P', 
        'augmented': 'aug', 
        'diminished': 'dim',
        }

    @property
    def _interval_string(self):
        return self._interval_number_to_interval_string[abs(self.number)]

    @property
    def _quality_abbreviation(self):
        return self._quality_string_to_quality_abbreviation[
            self._quality_string]

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate named interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2),
            ...     pitchtools.NamedPitch(12),
            ...     )
            NamedIntervalClass('+M2')

        Return named interval-class.
        '''
        from abjad.tools import pitchtools
        named_interval = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        return cls(named_interval)

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        if self.number < 1:
            return '-'
        elif self.number == 1:
            return ''
        else:
            return '+'

    @property
    def direction_word(self):
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'

    @property
    def quality_string(self):
        return self._quality_string
