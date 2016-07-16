# -*- encoding: utf-8 -*-
from abjad.tools.miditools.MetaMessage import MetaMessage


class EndOfTrackMessage(MetaMessage):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _meta_type_char = 0x2F

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        assert data[index] == cls._meta_type_char
        index += 2
        return cls(), index
