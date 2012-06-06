from abjad.tools.abctools import AbjadObject


class Scheme(AbjadObject):
    '''Abjad model of Scheme code::

        >>> from abjad.tools.schemetools import Scheme
        >>> s = Scheme(True)
        >>> s.format
        '##t'

    schemetools.Scheme can represent nested structures ::

        >>> s = Scheme(('left', (1, 2, False)), ('right', (1, 2, 3.3)))
        >>> s.format
        '#((left (1 2 #f)) (right (1 2 3.3)))'

    schemetools.Scheme wraps variable-length arguments into a tuple ::

        >>> s = Scheme(1, 2, 3)
        >>> q = Scheme((1, 2, 3))
        >>> s.format == q.format
        True

    schemetools.Scheme also takes an optional `quoting` keyword, by which Scheme's
    various quote, unquote, unquote-splicing characters can be prepended to the
    formatted result ::

        >>> s = Scheme((1, 2, 3), quoting="'#")
        >>> s.format
        "#'#(1 2 3)"

    Scheme is immutable.
    '''

    __slots__ = ('_quoting', '_value',)

    def __init__(self, *args, **kwargs):
        if 1 == len(args):
            if isinstance(args[0], type(self)):
                args = args[0]._value
            else:
                args = args[0]
        quoting = kwargs.get('quoting')
        assert isinstance(quoting, (str, type(None)))
        if quoting is not None:
            assert all([x in ("'", ',', '@', '`', '#') for x in quoting])
        object.__setattr__(self, '_quoting', quoting)
        object.__setattr__(self, '_value', args)

    ### SPECIAL METHODS ###

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

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        return Scheme._format_value(self._value)

    ### PUBLIC PROPERTIES ###

    @property
    def format(self):
        '''Hash-mark-prepended format of Scheme::

            >>> from abjad.tools.schemetools import Scheme
            >>> Scheme(True).format
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
            if value.startswith('"') and value.endswith('"'):
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
