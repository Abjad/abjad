from typing import Optional
from typing import Union as U
from abjad.tools.abctools.AbjadObject import AbjadObject


class Momento(AbjadObject):
    r'''Momento.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_absent',
        '_context',
        '_document',
        '_prototype',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        absent: bool = None,
        context: str = None,
        document: str = None,
        prototype: str = None,
        value: U[int, str] = None,
        ) -> None:
        if absent is not None:
            absent = bool(absent)
        self._absent = absent
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if document is not None:
            assert isinstance(document, str), repr(document)
        self._document = document
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
        self._prototype = prototype
        if value is not None:
            assert isinstance(value, (int, str)), repr(value)
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def absent(self) -> Optional[bool]:
        r'''Is true when context is absent in this segment.
        '''
        return self._absent

    @property
    def context(self) -> str:
        r'''Gets (name of local) context.
        '''
        return self._context

    @property
    def document(self) -> Optional[str]:
        r'''Gets document.
        '''
        return self._document

    @property
    def prototype(self) -> str:
        r'''Gets prototype.
        '''
        return self._prototype

    @property
    def value(self) -> U[int, str]:
        r'''Gets value.
        '''
        return self._value
