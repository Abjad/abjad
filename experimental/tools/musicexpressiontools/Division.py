# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import timespantools
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction


class Division(NonreducedFraction):
    r'''Division.

    A division is a nonreduced fraction that is optionally
    offset-positioned.

    ..  container:: example::
    
        Example 1. Initializes from pair:

        ::

            >>> musicexpressiontools.Division(5, 8)
            Division(5, 8)

    ..  container:: example::

        Example 2. Initializes from other division:

        ::

            >>> division = musicexpressiontools.Division(
            ...     (5, 8),
            ...     start_offset=Offset(1, 8),
            ...     )
            >>> new_division = musicexpressiontools.Division(division)
            >>> new_division
            Division(5, 8)
            >>> new_division.start_offset
            Offset(1, 8)

    Divisions model any block of time that is divisible into parts: beats,
    complete measures, etc.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_offset',
        )

    ### CONSTRUCTOR ###

    def __new__(
        cls,
        *args,
        **kwargs
        ):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                raise Exception(str)
            elif isinstance(arg, cls):
                pair = arg
            elif hasattr(arg, 'duration'):
                pair = (arg.duration.numerator, arg.duration.denominator)
            else:
                pair = arg
        elif len(args) == 2:
            pair = args
        else:
            raise ValueError(args)
        self = NonreducedFraction.__new__(cls, pair)
        start_offset = kwargs.get('start_offset')
        if start_offset is None:
            start_offset = getattr(pair, 'start_offset', None)
        self._start_offset = start_offset
        return self

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self.pair,
            start_offset=self.start_offset,
            )

    # TODO: remove?
    __deepcopy__ = __copy__

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        keyword_argument_names = []
        if self.start_offset is not None:
            keyword_argument_names.append('start_offset')
        positional_argument_values = (
            self.pair,
            )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    # TODO: maybe keep only _get_timespan?
    def _get_timespan(self):
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Division duration.

        Returns duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    # TODO: remove in favor of self.timespan
    @property
    def start_offset(self):
        r'''Division start offset specified at initialization.

        .. note:: remove in favor of ``self.timespan``.

        Returns offset or none.
        '''
        return self._start_offset

    # TODO: remove in favor of self.timespan
    @property
    def stop_offset(self):
        r'''Division stop offset defined equal to start offset plus duration
        when start offset is not none.

        .. note:: remove in favor of ``self.timespan``.

        Defined equal to none when start offset is none.

        Returns offset or none.
        '''
        if self.start_offset is not None:
            return self.start_offset + self.duration

    # TODO: remove in favor of self.get_timespan()
    @property
    def timespan(self):
        r'''Division timespan.

        Returns timespan.

        .. note:: Deprecated. Use get_timespan() instead.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)

    ### PUBLIC METHODS ###

    def get_timespan(self):
        '''Get timespan of division.

        Returns timespan.
        '''
        return timespantools.Timespan(self.start_offset, self.stop_offset)