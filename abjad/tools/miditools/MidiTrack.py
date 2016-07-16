# -*- encoding: utf-8 -*-
import struct
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MidiTrack(AbjadValueObject):
    '''
    MIDI track.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_events',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        events,
        ):
        if events is None:
            events = []
        self._events = tuple(events)

    ### PRIVATE METHODS ###

    @classmethod
    def _from_bytes(cls, data, index=0):
        from abjad.tools import miditools
        assert data[index:index + 4] == b'MTrk'
        index += 4
        length = struct.unpack_from('>I', data, index)[0]
        index += 4
        stop_index = index + length - 1
        events = []
        offset = 0
        while index < stop_index:
            delta_time, index = \
                miditools.MidiFile._variable_length_integer_from_bytes(
                    data, index=index)
            offset += delta_time
            message_type = cls._parse_message_type(data, index=index)
            message, index = message_type._from_bytes(data, index=index)
            event = miditools.Event(offset, message)
            events.append(event)
        midi_track = cls(events)
        return midi_track, index

    @staticmethod
    def _parse_message_type(data, index=0):
        from abjad.tools import miditools
        _message_types = {
            0x8: miditools.NoteOffMessage,
            0x9: miditools.NoteOnMessage,
            0xA: miditools.PolyphonicPressureMessage,
            0xB: miditools.ControllerMessage,
            0xC: miditools.ProgramChangeMessage,
            0xD: miditools.ChannelPressureMessage,
            0xE: miditools.PitchBendMessage,
            }
        upper_nibble = data[index] >> 4
        lower_nibble = data[index] & 0xF
        if upper_nibble in _message_types:
            return _message_types[upper_nibble]
        if lower_nibble == 0xF:
            return miditools.MetaMessage
        return miditools.SystemExclusiveMessage

    ### PUBLIC PROPERTIES ###

    @property
    def events(self):
        '''
        Gets MIDI events.
        '''
        return self._events
