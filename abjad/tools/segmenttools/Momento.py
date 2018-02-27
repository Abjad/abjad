import typing
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.systemtools.Tag import Tag


class Momento(AbjadObject):
    r'''Momento.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_absent',
        '_context',
        '_edition',
        '_prototype',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        absent: bool = None,
        context: str = None,
        edition: typing.Union[str, Tag] = None,
        prototype: str = None,
        #value: Union[int, str] = None,
        value: typing.Any = None,
        ) -> None:
        if absent is not None:
            absent = bool(absent)
        self._absent: bool = absent
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context: str = context
        edition_ = None
        if edition is not None:
            edition_ = Tag(edition)
        self._edition: Tag = edition_
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
        self._prototype: str = prototype
        if value is not None:
            if not isinstance(value, (int, str)):
                assert type(value).__name__ == 'PersistentOverride'
        #self._value: Union[int, str] = value
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def absent(self) -> typing.Optional[bool]:
        r'''Is true when context is absent in this segment.
        '''
        return self._absent

    @property
    def context(self) -> str:
        r'''Gets (name of local) context.
        '''
        return self._context

    @property
    def edition(self) -> typing.Optional[Tag]:
        r'''Gets edition.
        '''
        return self._edition

    @property
    def prototype(self) -> str:
        r'''Gets prototype.
        '''
        return self._prototype

    @property
    def value(self) -> typing.Union[int, str]:
        r'''Gets value.
        '''
        return self._value
