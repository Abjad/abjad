import abc
import functools
import numbers
from abjad import mathtools
from abjad.abctools.AbjadValueObject import AbjadValueObject
from . import constants


@functools.total_ordering
class Interval(AbjadValueObject):
    '''Abstract interval.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, argument):
        import abjad
        if isinstance(argument, str):
            match = constants._interval_name_abbreviation_regex.match(argument)
            if match is None:
                try:
                    argument = float(argument)
                    self._from_number(argument)
                    return
                except ValueError:
                    message = 'can not initialize {} from {!r}.'
                    message = message.format(type(self).__name__, argument)
                    raise ValueError(message)
                message = 'can not initialize {} from {!r}.'
                message = message.format(type(self).__name__, argument)
                raise ValueError(message)
            group_dict = match.groupdict()
            direction = group_dict['direction']
            if direction == '-':
                direction = -1
            else:
                direction = 1
            quality = group_dict['quality']
            if quality == 'aug':
                quality = 'A'
            elif quality == 'dim':
                quality = 'd'
            diatonic_number = int(group_dict['number'])
            self._validate_quality_and_diatonic_number(quality, diatonic_number)
            self._from_direction_quality_and_diatonic_number(
                direction,
                quality,
                diatonic_number,
                )
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = mathtools.sign(number)
            diatonic_number = abs(number)
            self._validate_quality_and_diatonic_number(quality, diatonic_number)
            self._from_direction_quality_and_diatonic_number(
                direction,
                quality,
                diatonic_number,
                )
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (abjad.Interval, abjad.IntervalClass)):
            self._from_interval_or_interval_class(argument)
        else:
            message = 'can not initialize {} from {!r}.'
            message = message.format(type(self).__name__, argument)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of interval.

        Returns new interval.
        '''
        return type(self)(abs(self.number))

    def __float__(self):
        r'''Coerce to semitones as float.

        Returns float.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def __lt__(self, argument):
        r'''Is true when interval is less than `argument`.

        Returns true or false.
        '''
        raise NotImplementedError

    def __neg__(self):
        r'''Negates interval.

        Returns interval.
        '''
        pass

    def __str__(self):
        r'''Gets string representation of interval.

        Returns string.
        '''
        return str(self.number)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _from_direction_quality_and_diatonic_number(
        self,
        direction,
        quality,
        diatonic_number,
        ):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_number(self, argument):
        raise NotImplementedError

    @abc.abstractmethod
    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    def _get_direction_symbol(self):
        if self.direction_number == -1:
            return '-'
        elif self.direction_number == 0:
            return ''
        elif self.direction_number == 1:
            return '+'
        else:
            message = 'invalid direction number: {!r}.'
            message = message.format(self.direction_number)
            raise ValueError(message)

    @classmethod
    def _named_to_numbered(cls, direction, quality, diatonic_number):
        octave_number = 0
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number >= 8:
            diatonic_pc_number -= 7
            octave_number += 1
        base_quality = quality
        if len(quality) > 1:
            base_quality = quality[0]
        semitones = constants._diatonic_number_and_quality_to_semitones[diatonic_pc_number][base_quality]
        if base_quality == 'd':
            semitones -= (len(quality) - 1)
        elif base_quality == 'A':
            semitones += (len(quality) - 1)
        semitones += (octave_number * 12)
        semitones *= direction
        return mathtools.integer_equivalent_number_to_integer(semitones)

    @classmethod
    def _numbered_to_named(cls, number):
        number = cls._to_nearest_quarter_tone(float(number))
        direction = mathtools.sign(number)
        octaves, semitones = divmod(abs(number), 12)
        quality, diatonic_number = constants._semitones_to_quality_and_diatonic_number[semitones]
        diatonic_number += octaves * 7
        return direction, quality, diatonic_number

    @staticmethod
    def _to_nearest_quarter_tone(number):
        number = round(float(number) * 4) / 4
        div, mod = divmod(number, 1)
        if mod == 0.75:
            div += 1
        elif mod == 0.5:
            div += 0.5
        return mathtools.integer_equivalent_number_to_integer(div)

    @classmethod
    def _validate_quality_and_diatonic_number(cls, quality, diatonic_number):
        diatonic_pc_number = diatonic_number
        while diatonic_pc_number > 7:
            diatonic_pc_number -= 7
        if constants._diatonic_number_and_quality_to_semitones.get(
            diatonic_pc_number, {}).get(quality[0]) is None:
            message = 'can not initialize {} from {!r} and {!r}.'
            message = message.format(cls.__name__, quality, diatonic_number)
            raise ValueError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        '''
        Gets cents of interval.

        Returns nonnegative number.
        '''
        return 100 * self.semitones

    @abc.abstractproperty
    def direction_number(self):
        '''
        Gets direction number of interval

        Returns integer.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def direction_string(self):
        '''
        Gets direction string of interval.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def interval_class(self):
        '''
        Gets interval-class of interval.

        Returns interval-class.
        '''
        raise NotImplementedError

#    @abc.abstractproperty
#    def name(self):
#        '''
#        Gets name of interval.
#
#        Returns string.
#        '''
#        raise NotImplementedError

    @abc.abstractproperty
    def number(self):
        '''
        Gets number of interval.

        Returns integer.
        '''
        raise NotImplementedError

    @property
    def octaves(self):
        r'''Gets octaves interval.

        Returns nonnegative number.
        '''
        return self.semitones // 12

#    @abc.abstractproperty
#    def quality_string(self):
#        '''
#        Gets quality name of interval.
#
#        Returns string.
#        '''
#        raise NotImplementedError

    @abc.abstractproperty
    def semitones(self):
        '''
        Gets semitones of interval.

        Returns integer or float.
        '''
        raise NotImplementedError

#    @abc.abstractproperty
#    def staff_spaces(self):
#        '''
#        Gets staff spaces of interval.
#
#        Returns integer.
#        '''
#        raise NotImplementedError

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def transpose(self, pitch_carrier):
        r'''Transposes `pitch_carrier` by interval.

        Returns new pitch carrier.
        '''
        raise NotImplementedError
