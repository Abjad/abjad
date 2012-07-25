from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental.quantizationtools.QEvent import QEvent


class PitchedQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_attachments', '_offset', '_pitches')

    ### INITIALIZER ###

    def __init__(self, offset, pitches, attachments=None):
        offset = durationtools.Offset(offset)
        pitches = tuple([pitchtools.NamedChromaticPitch(x) for x in pitches])
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._offset = offset
        self._pitches = pitches
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self.offset == other.offset and \
            self.pitches == other.pitches and \
            self.attachments == other.attachments:
            return True
        return False

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attachments(self):
        return self._attachments

    @property
    def pitches(self):
        return self._pitches
