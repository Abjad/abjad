from abjad.tools.pitchtools.IntervalObjectClass import IntervalObjectClass
import numbers


class InversionEquivalentChromaticIntervalClass(IntervalObjectClass):
    '''.. versionadded:: 2.0

    Abjad model of inversion-equivalent chromatic interval-class::

        >>> pitchtools.InversionEquivalentChromaticIntervalClass(1)
        InversionEquivalentChromaticIntervalClass(1)

    Inversion-equivalent chromatic interval-classes are immutable.
    '''

    __slots__ = ('_number', )

    def __init__(self, interval_class_token):
        if isinstance(interval_class_token, type(self)):
            _number = interval_class_token.number
        elif isinstance(interval_class_token, numbers.Number):
            if not 0 <= interval_class_token <= 6:
                raise ValueError('must be between 0 and 6, inclusive.')
            _number = interval_class_token
        else:
            raise TypeError('must be interval-class instance or number.')
        object.__setattr__(self, '_number', _number)

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

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '%s' % self.number

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return self.number

    ### PUBLIC PROPERTIES ###

    @property
    #def number(self):
    def inversion_equivalent_chromatic_interval_number(self):
        return self._number
