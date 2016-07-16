# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MidiMessage import MidiMessage


class NoteOffMessage(MidiMessage):
    '''
    MIDI NoteOff message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch',
        '_velocity',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pitch,
        velocity,
        channel_number=0,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            )
        self._pitch = int(pitch)
        self._velocity = int(velocity)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        stride = 3
        status, pitch, velocity = data[index:index + stride]
        message_type = status >> 4
        channel_number = status & 0x0F
        assert message_type == 0x8
        message = cls(
            channel_number=channel_number,
            pitch=pitch,
            velocity=velocity,
            )
        return message, index + stride

    ### PUBLIC PROPERTIES ###

    @property
    def pitch(self):
        '''
        Gets pitch.
        '''
        return self._pitch

    @property
    def velocity(self):
        '''
        Gets velocity.
        '''
        return self._velocity
