# -*- encoding: utf-8 -*-
from abjad.tools.miditools.Message import Message


class SystemExclusiveMessage(Message):
    '''
    MIDI SysEx message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_data_bytes',
        '_is_continuation',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        data_bytes,
        is_continuation=False,
        ):
        self._data_bytes = bytes(data_bytes)
        self._is_continuation = bool(is_continuation)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        return cls()

    ### PUBLIC PROPERTIES ###

    def data_bytes(self):
        '''
        Gets data message bytes.
        '''
        return self._data_bytes

    def is_continuation(self):
        '''
        SysEx continuation flag.
        '''
        return self._is_continuation
