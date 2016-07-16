# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MidiMessage import MidiMessage


class ChannelPressureMessage(MidiMessage):
    '''
    MIDI channel pressure message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_velocity',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        velocity,
        channel_number=0,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            )
        velocity = int(velocity)
        assert 0 <= velocity < 128
        self._velocity = velocity

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        stride = 2
        status, velocity = data[index:index + stride]
        message_type = status >> 4
        channel_number = status & 0x0F
        assert message_type == 0xD
        message = cls(
            channel_number=channel_number,
            velocity=velocity,
            )
        return message, index + stride

    ### PUBLIC PROPERTIES ###

    @property
    def velocity(self):
        '''
        Gets velocity.
        '''
        return self._velocity
