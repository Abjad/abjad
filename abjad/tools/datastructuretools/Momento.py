from abjad.tools.abctools.AbjadObject import AbjadObject


class Momento(AbjadObject):
    r'''Momento.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_absent',
        '_context',
        '_prototype',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        absent=None,
        context=None,
        prototype=None,
        value=None,
        ):
        if absent is not None:
            absent = bool(absent)
        self._absent = absent
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
        self._prototype = prototype
        if value is not None:
            assert isinstance(value, (int, str)), repr(value)
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def absent(self):
        r'''Is true when context is absent in this segment.

        Returns true, false or none.
        '''
        return self._absent

    @property
    def context(self):
        r'''Gets (name of local) context.

        Returns string.
        '''
        return self._context

    @property
    def prototype(self):
        r'''Gets prototype.

        Returns string.
        '''
        return self._prototype

    @property
    def value(self):
        r'''Gets value.

        Returns string.
        '''
        return self._value
