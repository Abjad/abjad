import abc
import operator

from abjad.system.StorageFormatManager import StorageFormatManager


class Inequality(object):
    """
    Inequality.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Inequalities"

    __slots__ = ("_operator_string", "_operator_function")

    _operator_strings = ("!=", "<", "<=", "==", ">", ">=")

    ### INITIALIZER ###

    def __init__(self, operator_string="<"):
        assert operator_string in self._operator_strings
        self._operator_string = operator_string
        self._operator_function = {
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            ">": operator.gt,
            ">=": operator.ge,
        }[self._operator_string]

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument):
        """
        Calls inequality on ``argument``.

        Returns true or false.
        """
        raise NotImplementedError

    def __eq__(self, argument) -> bool:
        """
        Is true equal to ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats inequality.
        """
        if format_specification in ("", "storage"):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self) -> int:
        """
        Hashes object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self) -> str:
        """
        Gets operator string.

        Returns string.
        """
        return self._operator_string
