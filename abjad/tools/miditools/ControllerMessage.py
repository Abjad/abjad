# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MidiMessage import MidiMessage


class ControllerMessage(MidiMessage):
    '''
    MIDI control change message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controller_number',
        '_controller_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        controller_number,
        controller_value,
        channel_number=0,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            )
        self._controller_number = int(controller_number)
        self._controller_value = int(controller_value)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        stride = 3
        status, controller_number, controller_value = data[index:index + stride]
        message_type = status >> 4
        channel_number = status & 0x0F
        assert message_type == 0xB
        message = cls(
            channel_number=channel_number,
            controller_number=controller_number,
            controller_value=controller_value,
            )
        return message, index + stride

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        '''
        Gets controller_number.
        '''
        return self._controller_number

    @property
    def controller_value(self):
        '''
        Gets controller_value.
        '''
        return self._controller_value
