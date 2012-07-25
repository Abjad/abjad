from abjad.tools import durationtools
from experimental.quantizationtools.QEvent import QEvent


class SilentQEvent(QEvent):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_attachments', '_offset',)

    ### INITIALIZER ###

    def __init__(self, offset, attachments=None):
        offset = durationtools.Offset(offset)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._offset = offset
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self._offset == other._offset and \
            self._attachments == other._attachments:
            return True
        return False

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attachments(self):
        return self._attachments
