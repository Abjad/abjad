from experimental.quantizationtools.QEvent import QEvent


class SilentQEvent(QEvent):
    '''A ``QEvent`` which indicates the onset of a period of silence
    in a ``QEventSequence``:

        >>> q_event = quantizationtools.SilentQEvent(1000)
        >>> q_event
        quantizationtools.SilentQEvent(
            durationtools.Offset(1000, 1),
            attachments=()
            )

    Return ``SilentQEvent`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_attachments', '_offset',)

    ### INITIALIZER ###

    def __init__(self, offset, attachments=None, index=None):
        QEvent.__init__(self, offset, index=index)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if type(self) == type(other) and \
            self._offset == other._offset and \
            self._attachments == other._attachments and \
            self._index == other._index:
            return True
        return False

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def attachments(self):
        return self._attachments
