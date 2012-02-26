from fractions import Fraction
from abjad.tools.schemetools.Scheme import Scheme


class SchemeMoment(Scheme):
    '''Abjad model of LilyPond moment::

        abjad> schemetools.SchemeMoment(1, 68)
        SchemeMoment(1, 68)

    Initialize scheme moments with a single fraction, two integers or another scheme moment.

    Scheme moments are immutable.
    '''

    def __new__(klass, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (Fraction, int, long)):
            args = Fraction(args[0])
        elif len(args) == 1 and isinstance(args[0], tuple):
            args = Fraction(*args[0])
        elif len(args) == 1 and isinstance(args[0], klass):
            args = args[0].duration
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            args = Fraction(*args)
        else:
            raise TypeError('can not intialize scheme moment from "%s".' % str(args))
        return Scheme.__new__(klass, args, **kwargs)

    ### OVERLOADS ###

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
        return '%s(%s, %s)' % (type(self).__name__, self._value.numerator, self._value.denominator)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_value(self):
        numerator, denominator = self._value.numerator, self._value.denominator
        return '(ly:make-moment %s %s)' % (numerator, denominator)

    ### PUBLIC ATTRIBUTES ###

    @property
    def duration(self):
        '''Duration of scheme moment::

            abjad> scheme_moment = schemetools.SchemeMoment(1, 68)
            abjad> scheme_moment.duration
            Fraction(1, 68)

        Return duration.
        '''
        return self._value
