from experimental.divisiontools.DivisionList import DivisionList


class DivisionRegionDivisionList(DivisionList):
    r'''.. versionadded:: 1.0

    What is a region?
    A region is an uninterrupted block of time to which a command applies.
    (A region is a special type of timespan.)

    What is a division region?
    A division region is a region to which exactly one division-maker applies.

    What is a division region division list?
    A division region division list is a special type of division list.
    A division region division list is the division list created by
    exactly one division-maker applied to exactly one division region.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, start_timepoint=None, stop_timepoint=None):
        DivisionList.__init__(self, divisions)
        self._start_timepoint = start_timepoint
        self._stop_timepoint = stop_timepoint    

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r}, start_timepoint={!r}, stop_timepoint={!r})'.format(
            self._class_name, self._contents_string, self.start_timepoint, self.stop_timepoint)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_timepoint(self):
        return self._start_timepoint

    @property
    def stop_timepoint(self):
        return self._stop_timepoint
