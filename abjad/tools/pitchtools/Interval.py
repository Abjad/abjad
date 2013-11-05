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
        return type(self)(abs(self.number))

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if arg.number == self.number:
                if arg.direction_number == self.direction_number:
                    return True
        return False

    def __float__(self):
        raise NotImplementedError(
            'float needs to be implemented on %s.' % type(self))

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError(
            'int needs to be implemented on %s.' % type(self))

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        pass

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return str(self.number)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

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
        return 100 * self.semitones

    @property
    def direction_number(self):
        return self._direction_number

    @property
    def direction_string(self):
        return self._direction_string

    # TODO: remove
    @property
    def interval_class(self):
        pass

    # TODO: remove
    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        pass
