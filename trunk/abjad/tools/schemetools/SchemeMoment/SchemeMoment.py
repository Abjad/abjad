from abjad.tools import durationtools
from abjad.tools.schemetools.Scheme import Scheme


class SchemeMoment(Scheme):
    r'''Abjad model of LilyPond moment:

    ::

        >>> schemetools.SchemeMoment(1, 68)
        SchemeMoment((1, 68))

    Initialize scheme moments with a single fraction, 
    two integers or another scheme moment.

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
        else:
            message = 'can not intialize scheme moment from "{}".'
            raise TypeError(message.format(args))
        Scheme.__init__(self, args, **kwargs)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self._value == arg._value:
                return True
        return False

    def __ge__(self, arg):
        if isinstance(arg, type(self)):
            if self._value >= arg._value:
                return True
        return False

    def __getnewargs__(self):
        return (self._value,)

    def __gt__(self, arg):
        if isinstance(arg, type(self)):
            if self._value > arg._value:
                return True
        return False

    def __le__(self, arg):
        if isinstance(arg, type(self)):
            if self._value <= arg._value:
                return True
        return False

    def __lt__(self, arg):
        if isinstance(arg, type(self)):
            if self._value < arg._value:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}(({}, {}))'.format(
            self._class_name, 
            self._value.numerator, 
            self._value.denominator,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        numerator, denominator = self._value.numerator, self._value.denominator
        return '(ly:make-moment %s %s)' % (numerator, denominator)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Duration of scheme moment:

        ::

            >>> scheme_moment = schemetools.SchemeMoment(1, 68)
            >>> scheme_moment.duration
            Duration(1, 68)

        Return duration.
        '''
        return self._value
