from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.timespantools.Timespan import Timespan


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, timespan=None):
        assert isinstance(timespan, (Timespan, type(None)))
        self.value = value
        self.timespan = timespan 
