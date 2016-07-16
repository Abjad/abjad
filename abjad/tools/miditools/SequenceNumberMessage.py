# -*- encoding: utf-8 -*-
import struct
from abjad.tools.miditools.MetaMessage import MetaMessage


class SequenceNumberMessage(MetaMessage):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_sequence_number',
        )

    _meta_type_char = 0x00

    ### INITIALIZER ###

    def __init__(
        self,
        sequence_number,
        ):
        self._sequence_number = int(sequence_number)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        assert data[index] == cls._meta_type_char
        index += 1
        assert data[index] == 0x02
        index += 1
        sequence_number = struct.unpack_from('>H', data, index)[0]
        index += 2
        message = cls(sequence_number)
        return message, index

    ### PUBLIC PROPERTIES ###

    @property
    def sequence_number(self):
        '''
        Gets sequence number.
        '''
        return self._sequence_number
