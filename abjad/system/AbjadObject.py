import abc
from .FormatSpecification import FormatSpecification
from .StorageFormatManager import StorageFormatManager


class AbjadObject(object):
    """
    Abstract base class from which many custom classes inherit.
    """

    __slots__ = ()

    def __format__(self, format_specification='') -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def _get_format_specification(self):
        return FormatSpecification(client=self)
