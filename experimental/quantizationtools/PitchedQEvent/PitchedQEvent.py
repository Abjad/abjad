from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental.quantizationtools.QEvent import QEvent


class PitchedQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    _fields = ('_attachments', '_offset', '_pitches')

    ### INITIALIZER ###

    def __new__(cls, offset, pitches, attachments=None):
        offset = durationtools.Offset(offset)
        pitches = tuple([pitchtools.NamedChromaticPitch(x) for x in pitches])
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        return tuple.__new__(cls, (offset, pitches, attachments))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attachments(self):
        return self[2]

    @property
    def pitches(self):
        return self[1]
