# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MidiMessage import MidiMessage


class ProgramChangeMessage(MidiMessage):
    '''
    MIDI program change message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_program_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        program_number,
        channel_number=0,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            )
        self._program_number = int(program_number)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        stride = 2
        status, program_number = data[index:index + stride]
        message_type = status >> 4
        channel_number = status & 0x0F
        assert message_type == 0xC
        message = cls(
            channel_number=channel_number,
            program_number=program_number,
            )
        return message, index + stride

    ### PUBLIC PROPERTIES ###

    @property
    def program_number(self):
        '''
        Gets program number.
        '''
        return self._program_number
