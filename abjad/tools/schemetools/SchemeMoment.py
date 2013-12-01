# -*- encoding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools.schemetools.Scheme import Scheme


@functools.total_ordering
class SchemeMoment(Scheme):
    r'''A LilyPond scheme moment.

    Initializes with two integers:

    ::

        >>> moment = schemetools.SchemeMoment(1, 68)
        >>> moment
        SchemeMoment(1, 68)

    Scheme moments are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and durationtools.Duration.is_token(args[0]):
            args = durationtools.Duration(args[0])
        elif len(args) == 1 and isinstance(args[0], type(self)):
            args = args[0].duration
        elif len(args) == 2 and \
            isinstance(args[0], int) and isinstance(args[1], int):
            args = durationtools.Duration(args)
        elif len(args) == 0:
            args = durationtools.Duration((1, 4))
        else:
            message = 'can not intialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise TypeError(message)
        Scheme.__init__(self, args, **kwargs)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''True when `arg` is a scheme moment with the same value as that of
        this scheme moment.

        ::

            >>> moment == schemetools.SchemeMoment(1, 68)
            True

        Otherwise false.

            >>> moment == schemetools.SchemeMoment(1, 54)
            False

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self._value == arg._value:
                return True
        return False

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self._value,)

    def __lt__(self, arg):
        r'''True when `arg` is a scheme moment with value greater than that of
        this scheme moment.

        ::

            >>> moment < schemetools.SchemeMoment(1, 32)
            True

        Otherwise false:

        ::

            >>> moment < schemetools.SchemeMoment(1, 78)
            False

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self._value < arg._value:
                return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        numerator, denominator = self._value.numerator, self._value.denominator
        return '(ly:make-moment {} {})'.format(numerator, denominator)

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self._value.numerator,
                self._value.denominator,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Duration of scheme moment.

        ::

            >>> scheme_moment = schemetools.SchemeMoment(1, 68)
            >>> scheme_moment.duration
            Duration(1, 68)

        Returns duration.
        '''
        return self._value
