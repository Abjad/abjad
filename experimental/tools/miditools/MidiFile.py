# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class MidiFile(AbjadValueObject):
    r'''MIDI file.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_tracks',
        )

    ### INITIALIZER ###

    def __init__(self, midi_tracks=None):
        from experimental.tools import miditools
        prototype = miditools.MidiTrack
        if midi_tracks is not None:
            assert all(isinstance(_, prototype) for _ in midi_tracks)
            midi_tracks = tuple(midi_tracks)
        self._midi_tracks = midi_tracks

    ### PUBLIC PROPERTIES ###

    @property
    def midi_tracks(self):
        r'''Gets MIDI tracks in MIDI file.
        '''
        return self._midi_tracks