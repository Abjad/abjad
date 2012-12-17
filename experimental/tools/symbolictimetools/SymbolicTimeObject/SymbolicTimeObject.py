import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimeObject(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which symbolic time objects inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Read-only reference to score specification against which symbolic time object is defined.

        Return score specification or none.
        '''
        return self._score_specification
