import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimeObjectInequality(AbjadObject):
    r'''.. versionadded:: 1.0

    Time-object inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, template):
        self._template = template
