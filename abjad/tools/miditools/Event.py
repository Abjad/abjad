# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Event(AbjadValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_offset',
        '_message',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        offset,
        message,
        ):
        from abjad.tools import miditools
        self._offset = int(offset)
        assert isinstance(message, miditools.Message)
        self._message = message

    ### PUBLIC PROPERTIES ###

    @property
    def message(self):
        return self._message

    @property
    def offset(self):
        return self._offset
