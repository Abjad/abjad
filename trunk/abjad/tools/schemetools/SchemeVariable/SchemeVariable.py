from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeVariable(_StrictComparator, _Immutable):
    '''Abjad model of Scheme variable::

        abjad> schemetools.SchemeVariable('grace')
        SchemeVariable('grace')

    Scheme variables are immutable.
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

    def __str__(self):
        return self.format

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme variable::

            abjad> scheme_variable = schemetools.SchemeVariable('UP')
            abjad> scheme_variable.format
            '#UP'

        Return string.
        '''
        return '#%s' % self._string
