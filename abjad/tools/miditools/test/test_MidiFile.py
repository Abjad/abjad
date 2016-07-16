# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import miditools
from abjad.tools import stringtools
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


class Test(unittest.TestCase):

    '''
    size 140
       0   4d 54 68 64  00 00 00 06  00 01 00 02  01 80 4d 54   |MThd..........MT|
      16   72 6b 00 00  00 46 00 ff  03 00 00 ff  01 09 63 72   |rk...F........cr|
      32   65 61 74 6f  72 3a 20 00  ff 01 1e 47  4e 55 20 4c   |eator: ....GNU L|
      48   69 6c 79 50  6f 6e 64 20  32 2e 31 39  2e 34 34 20   |ilyPond 2.19.44 |
      64   20 20 20 20  20 20 20 20  20 00 ff 58  04 04 02 12   |         ..X....|
      80   08 00 ff 51  03 0f 42 40  00 ff 2f 00  4d 54 72 6b   |...Q..B@../.MTrk|
      96   00 00 00 28  00 90 3c 5a  83 00 90 3c  00 00 90 3e   |...(..<Z...<...>|
     112   5a 83 00 90  3e 00 00 90  40 5a 83 00  90 40 00 00   |Z...>...@Z...@..|
     128   90 41 5a 83  00 90 41 00  00 ff 2f 00                |.AZ...A.../.|
    '''

    def test_01(self):
        path = pathlib.Path(__file__).parent.joinpath('test.midi')
        with open(str(path), 'rb') as file_pointer:
            data = file_pointer.read()
        midi_file = miditools.MidiFile.from_bytes(data)
        assert midi_file is not None
        assert format(midi_file) == stringtools.normalize(
            '''
            miditools.MidiFile(
                midi_tracks=(
                    miditools.MidiTrack(
                        (
                            miditools.Event(
                                0,
                                miditools.SequenceOrTrackNameMessage(
                                    ''
                                    )
                                ),
                            miditools.Event(
                                0,
                                miditools.TextMessage(
                                    'creator: '
                                    )
                                ),
                            miditools.Event(
                                0,
                                miditools.TextMessage(
                                    'GNU LilyPond 2.19.44          '
                                    )
                                ),
                            miditools.Event(
                                0,
                                miditools.TimeSignatureMessage(
                                    4,
                                    4,
                                    18,
                                    user_scaling=8,
                                    )
                                ),
                            miditools.Event(
                                0,
                                miditools.TempoMessage(
                                    1000000
                                    )
                                ),
                            miditools.Event(
                                0,
                                miditools.EndOfTrackMessage()
                                ),
                            )
                        ),
                    miditools.MidiTrack(
                        (
                            miditools.Event(
                                0,
                                miditools.NoteOnMessage(
                                    60,
                                    90,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                384,
                                miditools.NoteOnMessage(
                                    60,
                                    0,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                384,
                                miditools.NoteOnMessage(
                                    62,
                                    90,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                768,
                                miditools.NoteOnMessage(
                                    62,
                                    0,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                768,
                                miditools.NoteOnMessage(
                                    64,
                                    90,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                1152,
                                miditools.NoteOnMessage(
                                    64,
                                    0,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                1152,
                                miditools.NoteOnMessage(
                                    65,
                                    90,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                1536,
                                miditools.NoteOnMessage(
                                    65,
                                    0,
                                    channel_number=0,
                                    )
                                ),
                            miditools.Event(
                                1536,
                                miditools.EndOfTrackMessage()
                                ),
                            )
                        ),
                    ),
                midi_format=1,
                division=384,
                )
            '''
            )
