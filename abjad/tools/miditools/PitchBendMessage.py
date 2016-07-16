# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MidiMessage import MidiMessage


class PitchBendMessage(MidiMessage):
    '''
    MIDI pitch bend message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pitch_bend',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pitch_bend,
        channel_number=0,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            )
        self._pitch_bend = int(pitch_bend)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        stride = 3
        status, low_bits, high_bits = data[index:index + stride]
        message_type = status >> 4
        channel_number = status & 0x0F
        assert message_type == 0xE
        pitch_bend = (high_bits << 7) | low_bits
        message = cls(
            channel_number=channel_number,
            pitch_bend=pitch_bend,
            )
        return message, index + stride

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_bend(self):
        '''
        Gets pitch bend.
        '''
        return self._pitch_bend
