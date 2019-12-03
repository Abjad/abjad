import typing

from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag
from abjad.utilities.Offset import Offset


class Momento(object):
    """
    Momento.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_context",
        "_edition",
        "_manifest",
        "_prototype",
        "_synthetic_offset",
        "_value",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        context: str = None,
        edition: typing.Union[str, Tag] = None,
        manifest: str = None,
        prototype: str = None,
        synthetic_offset: Offset = None,
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
        if synthetic_offset is not None:
            assert isinstance(synthetic_offset, Offset), repr(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if value is not None:
            if not isinstance(value, (int, str, dict)):
                assert type(value).__name__ == "PersistentOverride", repr(value)
        self._value = value

    ### SPECIAL METHODS ###

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS###

    def _get_format_specification(self):
        return FormatSpecification(client=self)

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
    def synthetic_offset(self) -> typing.Optional[Offset]:
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    @property
    def value(self) -> typing.Union[int, str]:
        """
        Gets value.
        """
        return self._value
