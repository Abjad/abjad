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

    def __init__(self, divisions, voice_name, start_offset=None, stop_offset=None):
        VoiceDivisionList.__init__(self, divisions, voice_name)
        self._start_offset = start_offset
        self._stop_offset = stop_offset    

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r}, {!r}, start_offset={!r}, stop_offset={!r})'.format(
            self._class_name, self._contents_string, self.voice_name, 
            self.start_offset, self.stop_offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def stop_offset(self):
        return self._stop_offset
