# -*- encoding: utf-8 -*-
import struct
from abjad.tools.miditools.MetaMessage import MetaMessage


class TempoMessage(MetaMessage):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_microseconds',
        )

    _meta_type_char = 0x51

    ### INITIALIZER ###

    def __init__(
        self,
        microseconds,
        ):
        self._microseconds = int(microseconds)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        assert data[index] == cls._meta_type_char
        index += 1
        assert data[index] == 0x03
        index += 1
        microseconds = struct.unpack('>I', b'\x00' + data[index:index + 3])[0]
        index += 3
        message = cls(microseconds)
        return message, index

    ### PUBLIC PROPERTIES ###

    @property
    def microseconds(self):
        return self._microseconds
