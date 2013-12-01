# -*- encoding: utf-8 -*-
import abc
import re
from abjad.tools.abctools.AbjadObject import AbjadObject


class Interval(AbjadObject):
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
        {}          # exactly one diatonic quality abbreviation
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

    def __eq__(self, arg):
        r'''True when `arg` is an interval with number and direction direction
        equal to those of this interval. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if arg.number == self.number:
                if arg.direction_number == self.direction_number:
                    return True
        return False

    def __float__(self):
        r'''Change interval to float.

        Returns float.
        '''
        message = 'float needs to be implemented on {}.'.format(type(self))
        raise NotImplementedError(message)

    def __hash__(self):
        r'''Hashes interval.

        Returns integer.
        '''
        return hash(repr(self))

    def __int__(self):
        r'''Change interval to integer.

        Returns integer.
        '''
        message = 'int needs to be implemented on {}.'.format(type(self))
        raise NotImplementedError(message)

    def __ne__(self, arg):
        r'''True when interval does not equal `arg`.

        Returns boolean.
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

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.number,
                ),
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def is_named_interval_abbreviation(expr):
        '''True when `expr` is a named interval abbreviation.
        Otherwise false:

        ::

            >>> pitchtools.Interval.is_named_interval_abbreviation('+M9')
            True

        The regex ``^([+,-]?)(M|m|P|aug|dim)(\d+)$`` underlies this predicate.

        Returns boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Interval._interval_name_abbreviation_regex.match(expr))

    @staticmethod
    def is_named_interval_quality_abbreviation(expr):
        '''True when `expr` is a named-interval quality abbreviation. Otherwise
        false:

        ::

            >>> pitchtools.Interval.is_named_interval_quality_abbreviation('aug')
            True

        The regex ``^M|m|P|aug|dim$`` underlies this predicate.

        Returns boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(Interval._named_interval_quality_abbreviation_regex.match(
            expr))

    ### PUBLIC PROPERTIES ###

    @property
    def cents(self):
        r'''Cents of interval.

        Returns nonnegative number.
        '''
        return 100 * self.semitones

    @property
    def direction_number(self):
        r'''Direction number of interval.

        Returns -1, 0 or 1.
        '''
        return self._direction_number

    @property
    def direction_string(self):
        r'''Direction string of interval.

        Returns string.
        '''
        return self._direction_string

    # TODO: remove
    @property
    def interval_class(self):
        r'''Interval class of interval.
        '''
        pass

    # TODO: remove
    @property
    def number(self):
        r'''Number of interval.
        '''
        return self._number

    @property
    def semitones(self):
        r'''Semitones equating to interval.

        Return nonnegative number.
        '''
        pass
