from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeNumber(_Immutable):
    '''Abjad model of Scheme number::

        abjad> schemetools.SchemeNumber(1.1)
        SchemeNumber(1.1...)

    Scheme numbers are immutable.
    '''

    __slots__ = ('number',)

    def __new__(klass, number):
        assert type(number) in (float, int)
        self = object.__new__(klass)
        object.__setattr__(self, 'number', number)
        return self

    def __getnewargs__(self):
        return (self.number, )

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, SchemeNumber):
            return self.number == arg.number
        return False

    def __float__(self):
        return float(self.number)

    def __int__(self):
        return int(self.number)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.number)

    def __str__(self):
        return self.format

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme number::

            abjad> scheme_number = schemetools.SchemeNumber(1.1)
            abjad> scheme_number.format
            '#1.1'

        Return string.
        '''
        return '#%s' % self.number
