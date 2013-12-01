# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class NamedIntervalClass(IntervalClass):
    '''A named interval-class.

    ::

        >>> pitchtools.NamedIntervalClass('-M9')
        NamedIntervalClass('-M2')

    '''

    ### CLASS VARIABLES ###

    _acceptable_quality_strings = (
        'perfect',
        'major',
        'minor',
        'diminished',
        'augmented',
        )

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

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if len(args) == 1 and \
            isinstance(args[0], (pitchtools.NamedInterval,
                pitchtools.NamedIntervalClass)):
            quality_string = args[0]._quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = \
                pitchtools.Interval._interval_name_abbreviation_regex.match(
                args[0])
            if match is None:
                message = '{!r} does not have the form of an abbreviation.'
                message = message.format(args[0])
                raise ValueError(message)
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
        elif len(args) == 0:
            quality_string = 'perfect'
            number = 1
        else:
            message = 'bad input: {!r}.'.format(args)
            raise TypeError(message)
        if quality_string not in \
            NamedIntervalClass._acceptable_quality_strings:
            message = 'not acceptable quality string: {!r}.'
            message = message.format(quality_string)
            raise ValueError(message)
        if not isinstance(number, int):
            message = 'must be integer: {!r}.'.format(number)
            raise TypeError(message)
        if number == 0:
            message = 'must be nonzero: {!r}.'.format(number)
            raise ValueError(number)
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
        r'''Absolute value of named interval-class.

        Returns new named interval-class.
        '''
        return type(self)(abs(self._number))

    def __eq__(self, arg):
        r'''True when `arg` is a named interval-class with direction number,
        quality string and number equal to those of this named interval-class.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.direction_number == arg.direction_number:
                if self._quality_string == arg._quality_string:
                    if self.number == arg.number:
                        return True
        return False

    def __float__(self):
        r'''Changes named interval-class to float.

        Returns float.
        '''
        return float(self._number)

    def __hash__(self):
        r'''Hashes named interval-class.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Changes named interval-class to integer.

        Returns integer.
        '''
        return self._number

    def __ne__(self, arg):
        r'''True when named interval-class does not equal `arg`. Otherwise
        false.

        Returns boolean.
        '''
        return not self == arg

    def __str__(self):
        r'''String representation of named interval-class.

        Returns string.
        '''
        return '{}{}{}'.format(
            self.direction_symbol,
            self._quality_abbreviation,
            abs(self.number),
            )

    ### PRIVATE PROPERTIES ###

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

    @property
    def _interval_string(self):
        return self._interval_number_to_interval_string[abs(self.number)]

    @property
    def _quality_abbreviation(self):
        return self._quality_string_to_quality_abbreviation[
            self._quality_string]

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                str(self),
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Makes named interval-class from `pitch_carrier_1` and
        `pitch_carrier_2`.

        ::

            >>> pitchtools.NamedIntervalClass.from_pitch_carriers(
            ...     NamedPitch(-2),
            ...     NamedPitch(12),
            ...     )
            NamedIntervalClass('+M2')

        Returns named interval-class.
        '''
        from abjad.tools import pitchtools
        named_interval = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        return cls(named_interval)

    ### PUBLIC PROPERTIES ###

    @property
    def direction_number(self):
        r'''Direction number of named interval-class.

        Returns -1, 0 or 1.
        '''
        if self.number < 1:
            return -1
        elif self.number == 1:
            return 0
        else:
            return 1

    @property
    def direction_symbol(self):
        r'''Direction symbol of named interval-class.

        Returns string.
        '''
        if self.number < 1:
            return '-'
        elif self.number == 1:
            return ''
        else:
            return '+'

    @property
    def direction_word(self):
        r'''Direction word of named interval-class.

        Returns string.
        '''
        if self.number < 1:
            return 'descending'
        elif self.number == 1:
            return ''
        else:
            return 'ascending'

    @property
    def quality_string(self):
        r'''Quality string of named interval-class.

        Returns string.
        '''
        return self._quality_string
