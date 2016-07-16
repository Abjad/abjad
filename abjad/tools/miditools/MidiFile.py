# -*- encoding: utf-8 -*-
import struct
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class MidiFile(AbjadValueObject):
    '''
    MIDI file.
    '''
    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_tracks',
        '_midi_format',
        '_division',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        midi_tracks=None,
        midi_format=0,
        division=96,
        ):
        if midi_tracks is None:
            midi_tracks = []
        self._midi_tracks = tuple(midi_tracks)
        self._midi_format = midi_format
        self._division = int(division)

    ### PRIVATE METHODS ###

    @staticmethod
    def _variable_length_integer_from_bytes(data, index=0):
        character = data[index]
        total = character & 0x7f
        while data[index] >> 7:  # if the continuation bit is set
            index += 1
            character = data[index]
            total = (total << 7) + (character & 0x7f)
        index += 1
        return total, index

    @staticmethod
    def _bytes_from_variable_length_integer(integer):
        result = bytearray()
        while integer or not len(result):
            integer, masked = integer >> 7, integer & 0x7F
            if len(result):
                masked |= 0x80
            result.append(masked)
        result.reverse()
        return bytes(result)

    ### PUBLIC METHODS ###

    @classmethod
    def from_bytes(cls, data):
        from abjad.tools import miditools
        assert data.startswith(b'MThd\x00\x00\x00\x06')
        midi_format, track_count, division = struct.unpack_from(
            '>HHH', data, 8)
        midi_tracks, index = [], 14
        for _ in range(track_count):
            midi_track, index = miditools.MidiTrack._from_bytes(data, index)
            midi_tracks.append(midi_track)
        midi_file = MidiFile(
            division=division,
            midi_format=midi_format,
            midi_tracks=midi_tracks,
            )
        return midi_file

    ### PUBLIC PROPERTIES ###

    @property
    def division(self):
        '''
        Gets division.
        '''
        return self._division

    @property
    def midi_format(self):
        '''
        Gets MIDI format.
        '''
        return self._midi_format

    @property
    def midi_tracks(self):
        '''
        Gets MIDI tracks.
        '''
        return self._midi_tracks
