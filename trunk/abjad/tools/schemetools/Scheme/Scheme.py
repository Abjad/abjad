from abjad.core import _Immutable
from abjad.core import _StrictComparator


class Scheme(_Immutable, _StrictComparator):
    '''Abjad model of Scheme code::

        abjad> from abjad.tools.schemetools import Scheme
        abjad> s = Scheme(True)
        abjad> s.format
        '##t'

    schemetools.Scheme can represent nested structures ::

        abjad> s = Scheme(('left', (1, 2, False)), ('right', (1, 2, 3.3)))
        abjad> s.format
        '#((left (1 2 #f)) (right (1 2 3.3)))'

    schemetools.Scheme wraps variable-length arguments into a tuple ::

        abjad> s = Scheme(1, 2, 3)
        abjad> q = Scheme((1, 2, 3))
        abjad> s.format == q.format
        True

    schemetools.Scheme also takes an optional `quoting` keyword, by which Scheme's
    various quote, unquote, unquote-splicing characters can be prepended to the
    formatted result ::

        abjad> s = Scheme((1, 2, 3), quoting="'#")
        abjad> s.format
        "#'#(1 2 3)"

    Scheme is immutable.
    '''

    __slots__ = ('_quoting', '_value',)

    def __new__(klass, *args, **kwargs):
        self = object.__new__(klass)
        if 1 == len(args):
            if isinstance(args[0], klass):
                args = args[0]._value
            else:
                args = args[0]
        quoting = kwargs.get('quoting')
        assert isinstance(quoting, (str, type(None)))
        if quoting is not None:
            assert all([x in ("'", ',', '@', '`', '#') for x in quoting])
        object.__setattr__(self, '_quoting', quoting)
        object.__setattr__(self, '_value', args)
        return self

    ### OVERLOADS ###

    def __eq__(self, other):
        if type(self) == type(other):
            if self._value == other._value:
                return True
        return False

    def __getnewargs__(self):
        return (self._value,)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self._value)

    def __str__(self):
        if self._quoting is not None:
            return self._quoting + self._formatted_value
        return self._formatted_value

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_value(self):
        return Scheme._format_value(self._value)

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''Hash-mark-prepended format of Scheme::

            abjad> from abjad.tools.schemetools import Scheme
            abjad> Scheme(True).format
            '##t'

        Returns string.
        '''
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#%s' % self._formatted_value

    ### PRIVATE METHODS ###

    @staticmethod
    def _format_value(value):
        if isinstance(value, str):
            if -1 == value.find(' '):
                return value
            value = repr(value)
            if value.startswith("'") and value.endswith("'"):
                value = value.replace('"', '\"')
                value = '"' + value[1:]
                value = value[:-1] + '"'
            return value
        elif isinstance(value, bool):
            if value:
                return '#t'
            return '#f'
        elif isinstance(value, (list, tuple)):
            return '(%s)' % ' '.join([Scheme._format_value(x) for x in value])
        elif isinstance(value, Scheme):
            return str(value)
        elif isinstance(value, type(None)):
            return '#f'
        return str(value)
