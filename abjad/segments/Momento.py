import typing
from abjad.system.AbjadObject import AbjadObject
from abjad.system.Tag import Tag


class Momento(AbjadObject):
    """
    Momento.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_edition',
        '_manifest',
        '_prototype',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        context: str = None,
        edition: typing.Union[str, Tag] = None,
        manifest: str = None,
        prototype: str = None,
        value: typing.Any = None,
        ) -> None:
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        edition_ = None
        if edition is not None:
            edition_ = Tag(edition)
        self._edition = edition_
        if manifest is not None:
            assert isinstance(manifest, str), repr(manifest)
            assert prototype is None
        self._manifest = manifest
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
            assert manifest is None
        self._prototype = prototype
        if value is not None:
            if not isinstance(value, (int, str, dict)):
                assert type(value).__name__ == 'PersistentOverride', repr(value)
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets (name of local) context.
        """
        return self._context

    @property
    def edition(self) -> typing.Optional[Tag]:
        """
        Gets edition.
        """
        return self._edition

    @property
    def manifest(self) -> typing.Optional[str]:
        """
        Gets manifest.
        """
        return self._manifest

    @property
    def prototype(self) -> typing.Optional[str]:
        """
        Gets prototype.
        """
        return self._prototype

    @property
    def value(self) -> typing.Union[int, str]:
        """
        Gets value.
        """
        return self._value
