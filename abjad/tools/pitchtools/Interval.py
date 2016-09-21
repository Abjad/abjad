# -*- coding: utf-8 -*-
import abc
import re
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Interval(AbjadValueObject):
    '''Interval base class.
    '''

    ### CLASS VARIABLES ###

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

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of interval.

        Returns new interval.
        '''
        return type(self)(abs(self.number))

    def __float__(self):
        r'''Change interval to float.

        Returns float.
        '''
        message = 'float needs to be implemented on {}.'
        message = message.format(type(self))
        raise NotImplementedError(message)

    def __int__(self):
        r'''Change interval to integer.

        Returns integer.
        '''
        message = 'int needs to be implemented on {}.'
        message = message.format(type(self))
        raise NotImplementedError(message)

    def __ne__(self, arg):
        r'''Is true when interval does not equal `arg`.

        Returns true or false.
        '''
        return not self == arg

    def __neg__(self):
        r'''Negates interval.

        Returns interval.
        '''
        pass

    def __str__(self):
        r'''String representation of interval.

        Returns string.
        '''
        return str(self.number)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        if type(self).__name__.startswith('Named'):
            values = [str(self)]
        else:
            values = [
                mathtools.integer_equivalent_number_to_integer(float(self))
                ]
        return systemtools.FormatSpecification(
            client=self,
            coerce_for_equality=True,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            template_names=['direction_number', 'interval_number'],
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def is_named_interval_abbreviation(expr):
        '''Is true when `expr` is a named interval abbreviation.
        Otherwise false:

        ::

            >>> pitchtools.Interval.is_named_interval_abbreviation('+M9')
            True

        The regex ``^([+,-]?)(M|m|P|aug|dim)(\d+)$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Interval._interval_name_abbreviation_regex.match(expr))

    @staticmethod
    def is_named_interval_quality_abbreviation(expr):
        '''Is true when `expr` is a named-interval quality abbreviation. Otherwise
        false:

        ::

            >>> pitchtools.Interval.is_named_interval_quality_abbreviation('aug')
            True

        The regex ``^M|m|P|aug|dim$`` underlies this predicate.

        Returns true or false.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Interval._named_interval_quality_abbreviation_regex.match(
            expr))

    ### PRIVATE PROPERTIES ###

    @property
    def _direction_symbol(self):
        if self.direction_number == -1:
            return '-'
        elif self.direction_number == 0:
            return ''
        elif self.direction_number == 1:
            return '+'
        else:
            raise ValueError

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        r'''Cents of interval.

        Returns nonnegative number.
        '''
        return 100 * self.semitones
