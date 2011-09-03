from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeString(_StrictComparator, _Immutable):
    '''Abjad model of Scheme string::

        abjad> schemetools.SchemeString('grace')
        SchemeString('grace')

    Scheme strings are immutable.
    '''

    #def __init__(self, string):
    #    self._string = string
    def __new__(klass, string):
        self = object.__new__(klass)
        object.__setattr__(self, '_string', string)
        return self

    def __getnewargs__(self):
        return (self._string, )

    ### OVERLOADS ###

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self._string)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme string::

            abjad> scheme_string = schemetools.SchemeString('grace')
            abjad> scheme_string.format
            '#"grace"'

        Return string.
        '''
        return '#"%s"' % self._string
