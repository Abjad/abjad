from abjad.core import _Immutable
from abjad.core import _StrictComparator
from fractions import Fraction


class SchemeMoment(_StrictComparator, _Immutable):
    '''Abjad model of LilyPond moment::

        abjad> schemetools.SchemeMoment(1, 68)
        SchemeMoment(1, 68)

    Initialize scheme moments with a single fraction, two integers or another scheme moment.

    Scheme moments are immutable.
    '''

    __slots__ = ('_duration')

    def __new__(klass, *args):
        self = object.__new__(klass)
        if len(args) == 1 and isinstance(args[0], (Fraction, int, long)):
            object.__setattr__(self, '_duration', Fraction(args[0]))
        elif len(args) == 1 and isinstance(args[0], tuple):
            object.__setattr__(self, '_duration', Fraction(*args[0]))
        elif len(args) == 1 and isinstance(args[0], type(self)):
            object.__setattr__(self, '_duration', args[0].duration)
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            object.__setattr__(self, '_duration', Fraction(*args))
        else:
            raise TypeError('can not intialize scheme moment from "%s".' % str(args))
        return self

    def __getnewargs__(self):
        return (self.duration, )

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.duration == arg.duration:
                return True
        return False

    def __ge__(self, arg):
        if isinstance(arg, type(self)):
            if self.duration >= arg.duration:
                return True
        return False

    def __gt__(self, arg):
        if isinstance(arg, type(self)):
            if self.duration > arg.duration:
                return True
        return False

    def __le__(self, arg):
        if isinstance(arg, type(self)):
            if self.duration <= arg.duration:
                return True
        return False

    def __lt__(self, arg):
        if isinstance(arg, type(self)):
            if self.duration < arg.duration:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.duration.numerator, self.duration.denominator)

    ### PUBLIC ATTRIBUTES ###

    @property
    def duration(self):
        '''Duration of scheme moment::

            abjad> scheme_moment = schemetools.SchemeMoment(1, 68)
            abjad> scheme_moment.duration
            Fraction(1, 68)

        Return duration.
        '''
        return self._duration

    @property
    def format(self):
        '''LilyPond input format of scheme moment::

            abjad> scheme_moment = schemetools.SchemeMoment(1, 68)
            abjad> scheme_moment.format
            '#(ly:make-moment 1 68)'

        Return string.
        '''
        numerator, denominator = self.duration.numerator, self.duration.denominator
        return '#(ly:make-moment %s %s)' % (numerator, denominator)
