from abjad.core import _Immutable
from abjad.core import _StrictComparator


class SchemeBoolean(_Immutable):
    '''Abjad model of Scheme boolean::

        abjad> schemetools.SchemeBoolean(True)
        SchemeBoolean(True)

    Scheme variables are immutable.
    '''

    __slots__ = ('arg',)

    def __new__(klass, arg):
        self = object.__new__(klass)
        object.__setattr__(self, 'arg', bool(arg))
        return self

    def __getnewargs__(self):
        return (self.arg, )

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, SchemeBoolean):
            return arg.arg == self.arg
        return False

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.arg)

    def __str__(self):
        return self.format

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme boolean::

            abjad> scheme_boolean = schemetools.SchemeBoolean(True)
            abjad> scheme_boolean.format
            '##t'

        Return string.
        '''
        if self.arg:
            return '##t'
        return '##f'
