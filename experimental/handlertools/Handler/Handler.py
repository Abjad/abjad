import abc
from abjad.tools import abctools


class Handler(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self._mandatory_argument_values == other._mandatory_argument_values:
                if self._keyword_argument_values == other._keyword_argument_values:
                    return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _tools_package_name(self):
        pass
