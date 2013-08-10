# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.mathtools.BoundedObject import BoundedObject
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction, BoundedObject):
    r'''Division.

    Offset-positioned, bounded, nonreduced fraction.

    Example 1. Initialize from string:

    ::

        >>> musicexpressiontools.Division('[5, 8)')
        Division('[5, 8)')

    Example 2. Initialize from pair and optional open / closed keywords:

    ::

        >>> musicexpressiontools.Division((5, 8), 
        ...     is_right_open=True, start_offset=Offset(1, 8))
        Division('[5, 8)', start_offset=Offset(1, 8))

    Example 3. Initialize from other division:

        >>> musicexpressiontools.Division(_)
        Division('[5, 8)', start_offset=Offset(1, 8))

    Divisions may model beats. Divisions may model complete measures.
    Divisions may model time objects other than beats or measures.

    Divisions generally may be used to model any block of time that is
    to be understood as divisible into parts.
    '''

    ### CLASS VARIABLES ###

    # slots definition does nothing here because multiple inheritance
    # breaks with multiple slots base classes
    __slots__ = (
        '_is_left_closed', 
        '_is_left_open', 
        '_is_right_closed', 
        '_is_right_open',
        '_start_offset',
        )

    ### CONSTRUCTOR ###

    def __new__(cls, arg,
        is_left_open=None, is_right_open=None, start_offset=None):
        if isinstance(arg, str):
            triple = mathtools.interval_string_to_pair_and_indicators(arg)
            pair, is_left_open, is_right_open = triple
        elif isinstance(arg, cls):
            pair = arg
        elif hasattr(arg, 'duration'):
            pair = (arg.duration.numerator, arg.duration.denominator)
        else:
            pair = arg
        self = NonreducedFraction.__new__(cls, pair)
        if is_left_open is None:
            is_left_open = getattr(pair, 'is_left_open', False)
        if is_right_open is None:
            is_right_open = getattr(pair, 'is_right_open', False)
        self.is_left_open = is_left_open
        self.is_right_open = is_right_open
        if start_offset is None:
            start_offset = getattr(pair, 'start_offset', None)
        self._start_offset = start_offset
        return self

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return self.__class__(
            self.pair,
            is_left_open=self.is_left_open, is_right_open=self.is_right_open,
            start_offset=self.start_offset)

    # TODO: remove?
    __deepcopy__ = __copy__

    def __repr__(self):
        if self.start_offset is not None:
            return '{}({!r}, start_offset={!r})'.format(
                self._class_name, str(self), self.start_offset)
        else:
            return '{}({!r})'.format(self._class_name, str(self))

    def __str__(self):
        if self.is_left_open:
            left_symbol = '('
        else:
            left_symbol = '['
        if self.is_right_open:
            right_symbol = ')'
        else:
            right_symbol = ']'
        return '{}{}, {}{}'.format(
            left_symbol, self.numerator, self.denominator, right_symbol)

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        string = '{}({!r})'.format(
            self._tools_package_qualified_class_name, str(self))
        return [string]

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Division duration.

        Return duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    # TODO: remove in favor of self.timespan
    @property
    def start_offset(self):
        r'''Division start offset specified at initialization.

        .. note:: remove in favor of ``self.timespan``.

        Return offset or none.
        '''
        return self._start_offset

    # TODO: remove in favor of self.timespan
    @property
    def stop_offset(self):
        r'''Division stop offset defined equal to start offset plus duration
        when start offset is not none.

        .. note:: remove in favor of ``self.timespan``.

        Defined equal to none when start offset is none.

        Return offset or none.
        '''
        if self.start_offset is not None:
            return self.start_offset + self.duration

    # TODO: remove in favor of self.get_timespan()
    @property
    def timespan(self):
        r'''Division timespan.

        Return timespan.

        .. note:: Deprecated. Use get_timespan() instead.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    # TODO: maybe keep only _get_timespan?
    def _get_timespan(self):
        '''Get timespan of division.

        Return timespan.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    def get_timespan(self):
        '''Get timespan of division.

        Return timespan.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = \
                positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(
            *positional_argument_values, **keyword_argument_dictionary)
        return result
