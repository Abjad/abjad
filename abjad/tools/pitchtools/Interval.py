import abc
import functools
import re
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class Interval(AbjadValueObject):
    '''Abstract interval.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _named_interval_quality_abbreviation_regex_body = '''
        (M|         # major
        m|          # minor
        P|          # perfect
        aug|        # augmented
        dim)        # dimished
        '''

    _named_interval_quality_abbreviation_regex = re.compile(
        '^{}$'.format(_named_interval_quality_abbreviation_regex_body),
        re.VERBOSE,
        )

    _interval_name_abbreviation_regex_body = '''
        ([+,-]?)    # one plus, one minus, or neither
        {}          # exactly one quality abbreviation
        (\d+)       # followed by one or more digits
        '''.format(
        _named_interval_quality_abbreviation_regex_body,
        )

    _interval_name_abbreviation_regex = re.compile(
        '^{}$'.format(_interval_name_abbreviation_regex_body),
        re.VERBOSE,
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of interval.

        Returns new interval.
        '''
        return type(self)(abs(self.number))

    def __float__(self):
        r'''Coerce to float.

        Returns float.
        '''
        return float(self.number)

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

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        r'''Gets cents of interval.

        Returns nonnegative number.
        '''
        return 100 * self.semitones

    ### PUBLIC METHODS ###

    @staticmethod
    def is_named_interval_abbreviation(argument):
        '''Is true when `argument` is a named interval abbreviation.
        Otherwise false.

        ..  container:: example

            >>> abjad.Interval.is_named_interval_abbreviation('+M9')
            True

        The regex ``^([+,-]?)(M|m|P|aug|dim)(\d+)$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Interval._interval_name_abbreviation_regex.match(argument))

    @staticmethod
    def is_named_interval_quality_abbreviation(argument):
        '''Is true when `argument` is a named-interval quality abbreviation.
        Otherwise false.

        ..  container:: example

            >>> abjad.Interval.is_named_interval_quality_abbreviation('aug')
            True

        The regex ``^M|m|P|aug|dim$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(argument, str):
            return False
        return bool(Interval._named_interval_quality_abbreviation_regex.match(
            argument))

    @abc.abstractmethod
    def transpose(self, pitch_carrier):
        r'''Transposes `pitch_carrier` by interval.

        Returns new pitch carrier.
        '''
        raise NotImplementedError
