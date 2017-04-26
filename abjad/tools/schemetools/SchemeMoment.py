# -*- coding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools import systemtools
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

    def __init__(self, *arguments, **keywords):
        if len(arguments) == 1 and durationtools.Duration.is_token(arguments[0]):
            arguments = durationtools.Duration(arguments[0])
        elif len(arguments) == 1 and isinstance(arguments[0], type(self)):
            arguments = arguments[0].duration
        elif len(arguments) == 2 and \
            isinstance(arguments[0], int) and isinstance(arguments[1], int):
            arguments = durationtools.Duration(arguments)
        elif len(arguments) == 0:
            arguments = durationtools.Duration((1, 4))
        else:
            message = 'can not intialize {}: {!r}.'
            message = message.format(type(self).__name__, arguments)
            raise TypeError(message)
        Scheme.__init__(self, arguments, **keywords)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a scheme moment with the same value as that of
        this scheme moment.

        ::

            >>> moment == schemetools.SchemeMoment(1, 68)
            True

        Otherwise false.

            >>> moment == schemetools.SchemeMoment(1, 54)
            False

        Returns true or false.
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

    def __hash__(self):
        r'''Hashes scheme moment.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(SchemeMoment, self).__hash__()

    def __lt__(self, arg):
        r'''Is true when `arg` is a scheme moment with value greater than that of
        this scheme moment.

        ::

            >>> moment < schemetools.SchemeMoment(1, 32)
            True

        Otherwise false:

        ::

            >>> moment < schemetools.SchemeMoment(1, 78)
            False

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self._value < arg._value:
                return True
        return False

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=[
                self._value.numerator,
                self._value.denominator,
                ],
            storage_format_kwargs_names=[],
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        numerator, denominator = self._value.numerator, self._value.denominator
        return '(ly:make-moment {} {})'.format(numerator, denominator)

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
