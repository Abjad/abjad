import abc
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    '''Expression base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _evaluate(self):
        pass
