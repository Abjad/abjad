from experimental.divisiontools.VoiceDivisionList import VoiceDivisionList


class DivisionRegionDivisionList(VoiceDivisionList):
    r'''.. versionadded:: 1.0

    A region is an uninterrupted block of time to which a command applies.

    A division region is a region to which exactly one division-maker applies.

    A division region division list is the division list output by
    exactly one division-maker applied to exactly one division region.

    Composers do not create division region division lists because
    all division lists arise as byproducts of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, voice_name, start_timepoint=None, stop_timepoint=None):
        VoiceDivisionList.__init__(self, divisions, voice_name)
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
