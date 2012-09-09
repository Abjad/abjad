from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class TimespanInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    Timespan inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ObjectInventory.__init__(self, *args, **kwargs)

    ### PUBLIC METHODS ###

    def get_timespan_that_satisfies_inequality(self, timespan_inequality):
        timespans = self.get_timespan_that_satisfy_inequality(timespan_inequality)
        if len(timespans) == 1:
            return timespans[0]
        elif 1 < len(timespans):
            raise Exception('extra timespan error.')
        else:
            raise Exception('missing timespan error.')

    def get_timespans_that_satisfy_inequality(self, timespan_inequality):
        result = []
        for timespan in self:
            if timespan_inequality(timespan_1=timespan):
                result.append(timespan)
        return result

    def has_timespan_that_satisifies_inequality(self, timespan_inequality):
        return bool(self.get_timespans_that_satisfy_inequality(timespan_inequality))
