from abjad.tools import durationtools
from experimental.quantizationtools.QEvent import QEvent


class UnpitchedQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    _fields = ('_attachments', '_offset',)

    ### INITIALIZER ###

    def __new__(cls, offset, attachments=None):
        offset = durationtools.Offset(offset)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        return tuple.__new__(cls, (offset, attachments))

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attachments(self):
        return self[1]
