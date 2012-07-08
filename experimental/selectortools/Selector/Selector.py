from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import voicetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Selector(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which all selectors inherit.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### PRIVATE METHODS ###

    def _is_counttime_selector_reference(self, expr):
        '''True if `expr` can serve as reference container for self.
        '''
        from experimental import selectortools
        return isinstance(expr, (voicetools.Voice, selectortools.CounttimeContainerSelector, str))

    def _reference_to_storable_form(self, reference):
        if isinstance(reference, voicetools.Voice):
            return reference.name
        else:
            return reference

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        '''Timespan of selector.

        Return timespan object.
        '''
        from experimental import timespantools
        return timespantools.Timespan(selector=self)
