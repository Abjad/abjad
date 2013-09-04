# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.NamedIntervalClass import NamedIntervalClass


class NamedMelodicIntervalClass(NamedIntervalClass):
    '''Abjad model of melodic diatonic interval-class:

    ::

        >>> pitchtools.NamedMelodicIntervalClass('-M9')
        NamedMelodicIntervalClass('-M2')

    Melodic diatonic interval-classes are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        from abjad.tools.pitchtools.is_melodic_diatonic_interval_abbreviation \
            import melodic_diatonic_interval_abbreviation_regex
        if len(args) == 1 and\
            isinstance(args[0], pitchtools.NamedInterval):
            quality_string = args[0]._quality_string
            number = args[0].number
        elif len(args) == 1 and isinstance(args[0], str):
            match = melodic_diatonic_interval_abbreviation_regex.match(
                args[0])
            if match is None:
                raise ValueError(
                    '"%s" does not have the form of an abbreviation.' % 
                    args[0])
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
            raise TypeError('what type of instance is this?')
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

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.direction_number == arg.direction_number:
                if self._quality_string == arg._quality_string:
                    if self.number == arg.number:
                        return True
        return False

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, arg):
        return not self == arg

    def __str__(self):
        return '%s%s%s' % (self.direction_symbol,
            self._quality_abbreviation, abs(self.number))

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%s%s' % (self.direction_symbol, abs(self.number))

    @property
    def _full_name(self):
        strings = []
        if self.direction_word:
            strings.append(self.direction_word)
        strings.extend([self._quality_string, self._interval_string])
        return ' '.join(strings)

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate melodic diatonic interval-class from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedMelodicIntervalClass.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2),
            ...     pitchtools.NamedPitch(12),
            ...     )
            NamedMelodicIntervalClass('+M2')

        Return melodic diatonic interval-class.
        '''
        from abjad.tools import pitchtools
        # get melodic diatonic interval
        mdi = pitchtools.NamedInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return melodic diatonic interval-class
        return pitchtools.NamedMelodicIntervalClass(mdi)
        #return mdi.melodic_diatonic_interval_class

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
