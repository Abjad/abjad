# -*- encoding: utf-8 -*-
import abc
from abjad.tools.miditools.Message import Message


class MidiMessage(Message):
    '''
    MIDI midi message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_channel_number',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        channel_number=0,
        ):
        channel_number = int(channel_number)
        assert 0 <= channel_number < 16
        self._channel_number = channel_number

    ### PUBLIC PROPERTIES ###

    @property
    def channel_number(self):
        '''Gets midi message channel number.
        '''
        return self._channel_number
