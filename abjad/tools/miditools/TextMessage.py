# -*- encoding: utf-8 -*-
import sys
from abjad.tools.miditools.MetaMessage import MetaMessage


class TextMessage(MetaMessage):
    '''
    Meta text message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_text',
        )

    _meta_type_char = 0x01

    ### INITIALIZER ###

    def __init__(
        self,
        text,
        ):
        self._text = str(text)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        from abjad.tools import miditools
        assert data[index] == cls._meta_type_char
        index += 1
        length, index = miditools.MidiFile._variable_length_integer_from_bytes(
            data, index)
        text = data[index:index + length]
        if sys.version_info[0] == 3:
            text = text.decode('utf-8')
        index += length
        message = cls(text=text)
        return message, index

    ### PUBLIC PROPERTIES ###

    @property
    def text(self):
        '''
        Gets text.
        '''
        return self._text
