# -*- coding: utf-8 -*-
from abjad.tools.quantizationtools.QEvent import QEvent


class SilentQEvent(QEvent):
    r'''Silent q-event.

    ::

        >>> import abjad
        >>> from abjad.tools import quantizationtools

    ..  container:: example

        ::

            >>> q_event = quantizationtools.SilentQEvent(1000)
            >>> q_event
            SilentQEvent(offset=Offset(1000, 1))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_attachments',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, offset=0, attachments=None, index=None):
        QEvent.__init__(self, offset=offset, index=index)
        if attachments is None:
            attachments = ()
        else:
            attachments = tuple(attachments)
        self._attachments = attachments

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a silent q-event with offset,
        attachments and index equal to those of this silent q-event.
        Otherwise false.

        Returns true or false.
        '''
        if (type(self) == type(argument) and
            self._offset == argument._offset and
            self._attachments == argument._attachments and
            self._index == argument._index):
            return True
        return False

    def __hash__(self):
        r'''Hashes silent q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(SilentQEvent, self).__hash__()

    ### PUBLIC PROPERTIES ###

    @property
    def attachments(self):
        r'''Gets attachments of silent q-event.
        '''
        return self._attachments
