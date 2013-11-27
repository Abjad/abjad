# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    '''A numbered inversion-equivalent interval-class.

    ::

        >>> pitchtools.NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(1)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, interval_class_token=None):
        from abjad.tools import pitchtools
        if isinstance(interval_class_token, type(self)):
            number = interval_class_token.number
        elif isinstance(interval_class_token, numbers.Number):
            if not 0 <= interval_class_token <= 6:
                message = 'must be between 0 and 6, inclusive.'
                raise ValueError(message)
            number = interval_class_token
        elif hasattr(interval_class_token, 'semitones'):
            number = interval_class_token.semitones
            number %= 12
            if 6 < number:
                number = 12 - number
        elif interval_class_token is None:
            number = 0
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, interval_class_token)
            raise TypeError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self.number))

    def __copy__(self):
        return type(self)(self.number)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, arg):
        return not self == arg

    def __neg__(self):
        return type(self)(self.number)

    def __str__(self):
        return '%s' % self.number

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            self.number,
            )
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )
