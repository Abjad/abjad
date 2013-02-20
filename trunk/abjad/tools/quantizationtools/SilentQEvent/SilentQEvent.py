from abjad.tools.quantizationtools.QEvent import QEvent


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

    def __eq__(self, expr):
        if type(self) == type(expr) and \
            self._offset == expr._offset and \
            self._attachments == expr._attachments and \
            self._index == expr._index:
            return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attachments(self):
        return self._attachments
