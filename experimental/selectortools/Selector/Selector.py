from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import containertools
from abjad.tools import leaftools
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

    # TODO: rename to _interpets_as_sliceable_selector
    def _is_counttime_selector_reference(self, expr):
        '''True if `expr` can serve as reference container for counttime selector.
        '''
        from experimental import selectortools
        # voices are sliceable
        if isinstance(expr, (voicetools.Voice, str)):
            return True
        # selectors are sliceable if they a container
        elif isinstance(expr, Selector) and issubclass(expr.klass, containertools.Container):
            return True
        # selectors are also sliceable if they pick out a slice
        # TODO: need an explicit SliceSelector abstract base class; can inherit from Selector
        elif isinstance(expr, selectortools.Selector) and 'Slice' in expr._class_name:
            return True
        else:
            return False

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
