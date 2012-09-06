from abjad.tools.abctools import AbjadObject


class Scheme(AbjadObject):
    '''Abjad model of Scheme code::

        >>> from abjad.tools.schemetools import Scheme
        >>> s = Scheme(True)
        >>> s.lilypond_format
        '##t'

    schemetools.Scheme can represent nested structures ::

        >>> s = Scheme(('left', (1, 2, False)), ('right', (1, 2, 3.3)))
        >>> s.lilypond_format
        '#((left (1 2 #f)) (right (1 2 3.3)))'

    schemetools.Scheme wraps variable-length arguments into a tuple ::

        >>> s = Scheme(1, 2, 3)
        >>> q = Scheme((1, 2, 3))
        >>> s.lilypond_format == q.lilypond_format
        True

    schemetools.Scheme also takes an optional `quoting` keyword, by which Scheme's
    various quote, unquote, unquote-splicing characters can be prepended to the
    formatted result ::

        >>> s = Scheme((1, 2, 3), quoting="'#")
        >>> s.lilypond_format
        "#'#(1 2 3)"

    Scheme is immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_quoting', '_value',)

    ### INITIALIZER ###

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
        from abjad.tools import schemetools
        return schemetools.format_scheme_value(self._value)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        '''Hash-mark-prepended format of Scheme::

            >>> from abjad.tools.schemetools import Scheme
            >>> Scheme(True).lilypond_format
            '##t'

        Returns string.
        '''
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#%s' % self._formatted_value

