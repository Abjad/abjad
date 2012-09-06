from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental import helpertools


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    Timespan inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ObjectInventory.__init__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def get_timespan_active_at_offset(self, offset):
        pass

    def get_timespans_active_at_offset(self, offset):
        pass

    def has_timespan_active_at_offset(self, offset):
        pass
