from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    Timespan inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ObjectInventory.__init__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def get_timespan_active_at_offset(self, offset):
        timespans = self.get_timespans_active_at_offset(offset)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception('extra timespan error.')
        else:
            raise Exception('missing timespan error.')

    def get_timespans_active_at_offset(self, offset):
        from experimental import timespantools
        result = []
        for timespan in self:
            if timespantools.expr_happens_during_timespan(timespan, offset):
                result.append(timespan)
        return result

    def has_timespan_active_at_offset(self, offset):
        return bool(self.get_timespans_active_at_offset(offset))
