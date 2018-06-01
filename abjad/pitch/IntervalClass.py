import abc
import functools
import numbers
from abjad import mathtools
from abjad.abctools.AbjadValueObject import AbjadValueObject
from . import constants


@functools.total_ordering
class IntervalClass(AbjadValueObject):
    '''Abstract interval-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, argument):
        import abjad
        if isinstance(argument, str):
            match = constants._interval_name_abbreviation_regex.match(argument)
            if match is None:
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
            number = int(group_dict['number'])
            self._from_direction_quality_and_diatonic_number(direction, quality, number)
        elif isinstance(argument, tuple) and len(argument) == 2:
            quality, number = argument
            direction = mathtools.sign(number)
            number = abs(number)
            self._from_direction_quality_and_diatonic_number(direction, quality, number)
        elif isinstance(argument, numbers.Number):
            self._from_number(argument)
        elif isinstance(argument, (abjad.Interval, abjad.IntervalClass)):
            self._from_interval_or_interval_class(argument)

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of interval-class.

        Returns new interval-class.
        '''
        return type(self)(abs(self._number))

    @abc.abstractmethod
    def __lt__(self, argument):
        r'''Is true when interval-class is less than `argument`.

        Returns true or false.
        '''
        raise NotImplementedError

    def __str__(self):
        r'''Gets string representation of interval-class.

        Returns string.
        '''
        return str(self.number)

    ### PRIVATE METHODS ###

    #@abc.abstractmethod
    def _from_direction_quality_and_diatonic_number(
        self,
        direction,
        quality,
        diatonic_number,
        ):
        raise NotImplementedError

    #@abc.abstractmethod
    def _from_number(self, argument):
        raise NotImplementedError

    #@abc.abstractmethod
    def _from_interval_or_interval_class(self, argument):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        r'''Gets number of interval-class.

        Returns number.
        '''
        return self._number
