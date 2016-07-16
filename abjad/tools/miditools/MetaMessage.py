# -*- encoding: utf-8 -*-
from abjad.tools.miditools.Message import Message


class MetaMessage(Message):
    '''
    MIDI meta message.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        from abjad.tools import miditools
        _message_types = {
            0x02: miditools.CopyrightMessage,
            0x07: miditools.CuePointMessage,
            0x2F: miditools.EndOfTrackMessage,
            0x04: miditools.InstrumentNameMessage,
            0x59: miditools.KeySignatureMessage,
            0x05: miditools.LyricMessage,
            0x06: miditools.MarkerMessage,
            0x20: miditools.MidiChannelPrefixMessage,
            0x7F: miditools.SequencerSpecificMessage,
            0x00: miditools.SequenceNumberMessage,
            0x03: miditools.SequenceOrTrackNameMessage,
            0x54: miditools.SmpteOffsetMessage,
            0x51: miditools.TempoMessage,
            0x01: miditools.TextMessage,
            0x58: miditools.TimeSignatureMessage,
            }
        assert data[index] == 0xFF
        index += 1
        message_type = _message_types[data[index]]
        message, index = message_type._from_bytes(data, index=index)
        return message, index
