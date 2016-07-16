# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import Enumeration
from abjad.tools.miditools.MetaMessage import MetaMessage


class KeySignatureMessage(MetaMessage):

    ### CLASS VARIABLES ###

    class Mode(Enumeration):
        MINOR = 0
        MAJOR = 1

    __slots__ = (
        '_alteration',
        '_mode',
        )

    _meta_type_char = 0x59

    ### INITIALIZER ###

    def __initializer__(
        self,
        alteration,
        mode,
        ):
        alteration = int(alteration)
        assert -7 <= alteration <= 7
        self._alteration = alteration
        self._mode = self.Mode.from_expr(mode)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        assert data[index] == cls._meta_type_char
        index += 1
        assert data[index] == 0x02
        index += 1
        alteration, mode = data[index:index + 2]
        index += 2
        message = cls(alteration, mode)
        return message, index

    ### PUBLIC PROPERTIES ###

    def alteration(self):
        return self._alteration

    def mode(self):
        return self._mode
