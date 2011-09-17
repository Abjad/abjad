from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock


class MIDIBlock(_AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file midi block.
    '''

    def __init__(self):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\midi'
        self.is_formatted_when_empty = True
