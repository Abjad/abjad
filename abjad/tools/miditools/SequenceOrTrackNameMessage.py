# -*- encoding: utf-8 -*-
from abjad.tools.miditools.TextMessage import TextMessage


class SequenceOrTrackNameMessage(TextMessage):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _meta_type_char = 0x03
