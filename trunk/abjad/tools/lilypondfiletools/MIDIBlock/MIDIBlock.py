from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock


class MIDIBlock(_AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file MIDI block.
    '''

    def __init__(self):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\MIDI'
        self.is_formatted_when_empty = True
