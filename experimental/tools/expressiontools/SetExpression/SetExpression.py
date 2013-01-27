import abc
import copy
from experimental.tools.expressiontools.AnchoredExpression import AnchoredExpression


class SetExpression(AnchoredExpression):
    '''Base set expression.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, source=None, target_timespan=None):
        assert isinstance(target_timespan, (str, type(None), AnchoredExpression)), repr(target_timespan)
        AnchoredExpression.__init__(self, anchor=target_timespan)
        self._source = source
        self._target_timespan = target_timespan

    ### PRIVATE METHODS ###

    def _set_start_segment_identifier(self, segment_identifier):
        assert isinstance(segment_identifier, str)
        if isinstance(self.target_timespan, str):
            self._target_timespan = segment_identifier
            self._anchor = segment_identifier
        else:
            target_timespan = copy.deepcopy(self.target_timespan)
            target_timespan._set_start_segment_identifier(segment_identifier)
            self._target_timespan = target_timespan
            self._anchor = target_timespan

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def target_timespan(self):
        return self._target_timespan
