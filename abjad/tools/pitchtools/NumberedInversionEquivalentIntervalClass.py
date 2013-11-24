# -*- encoding: utf-8 -*-
import numbers
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    '''A numbered inversion-equivalent interval-class.

    ::

        >>> pitchtools.NumberedInversionEquivalentIntervalClass(1)
        NumberedInversionEquivalentIntervalClass(1)

    Returns numbered inversion-equivalent interval-class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, interval_class_token):
        from abjad.tools import pitchtools
        if isinstance(interval_class_token, type(self)):
            _number = interval_class_token.number
        elif isinstance(interval_class_token, numbers.Number):
            if not 0 <= interval_class_token <= 6:
                message = 'must be between 0 and 6, inclusive.'
                raise ValueError(message)
            _number = interval_class_token
        elif hasattr(interval_class_token, 'semitones'):
            _number = interval_class_token.semitones
            _number %= 12
            if 6 < _number:
                _number = 12 - _number
        else:
            message = 'must be interval-class or number.'
            raise TypeError(message)
        self._number = _number

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
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.number,
                )
            )
