# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import rhythmmakertools
from abjad.tools import scoretools
from abjad.tools import templatetools
from experimental.tools.segmentmakertools.SegmentMaker import SegmentMaker


class PianoStaffSegmentMaker(SegmentMaker):
    r'''Piano staff segment-maker.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lh_pitch_range',
        '_lh_rhythm_maker',
        '_rh_pitch_range',
        '_rh_rhythm_maker',
        '_score',
        )

    _test_pitch_numbers = (
        43, 19, 36, 22, 29, -34, -37, 31, 40, 35, 14, -6, 28, 14, 43,
        -22, -32, -22, -3, 32, 7, 1, 27, -34, -17, -35, 42, 36, 38, 
        -11, -11, -31, 8, 9, 16, 31, 22, -27, -3, -28, -13, -14, 0, 
        34, 37, -33, -12, -26, -20, -2, 41, -37, -16, -2, -6, 6, 43, 
        -19, 10, 34, -2, -16, 34, -2, 21, -17, 22, 17, 4, -15, 42, -33, 
        -37, -32, -21, -2, 23, -2, 10, 31, -20, -39, -32, 22, 31, 0, 
        43, -19, 45, 35, -26, -35, -38, 7, 41, 38, 27, 5, -35, 15, 15, 
        -20, -19, 41, -20, 27, -4, 14, -26, -17, 17, -19, 9, -8, -31, 
        -14, 30, -28, 43, -34, -7, 14, 25, -26, 46, 36, -33, -17, 3, 
        -4, -12, 16, 4, 28, -20, 13, -34, -37, -38, -32, -10, -22, 9, 
        -25, 48, 32, 21, -27, 28, 14, 10, 7, 33, 39, 20, -3, 41, -36, 
        18, -20, 9, 28, 6, 39, 43, 39, 13, -35, -30, -36, -10, -11, 17, 
        -13, -36, -28, -13, -3, -20, -10, 42, 38, 23, 46, -17, 27, -10, 
        45, -28, 36, 29, 12, -1, 37, -10, 15, 45, 20, 32, -17
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rh_rhythm_maker=None,
        lh_rhythm_maker=None,
        rh_pitch_range=None,
        lh_pitch_range=None,
        ):
        SegmentMaker.__init__(self)
        if rh_rhythm_maker is None:
            rh_rhythm_maker = rhythmmakertools.NoteRhythmMaker()
        assert isinstance(rh_rhythm_maker, rhythmmakertools.RhythmMaker)
        self._rh_rhythm_maker = rh_rhythm_maker
        if lh_rhythm_maker is None:
            lh_rhythm_maker = rhythmmakertools.NoteRhythmMaker()
        assert isinstance(lh_rhythm_maker, rhythmmakertools.RhythmMaker)
        self._lh_rhythm_maker = lh_rhythm_maker
        rh_pitch_range = rh_pitch_range or '[C2, C4)'
        rh_pitch_range = pitchtools.PitchRange(rh_pitch_range)
        self._rh_pitch_range = rh_pitch_range
        lh_pitch_range = lh_pitch_range or '[C4, C6]'
        lh_pitch_range = pitchtools.PitchRange(lh_pitch_range)
        self._lh_pitch_range = lh_pitch_range

    ### PRIVATE METHODS ###

    def _make_music(self, divisions=None):
        template = templatetools.TwoStaffPianoScoreTemplate()
        score = template()
        self._score = score
        rh_voice = score['RH Voice']
        lh_voice = score['LH Voice']
        self._populate_rhythms(rh_voice, self.rh_rhythm_maker, divisions)
        self._populate_rhythms(lh_voice, self.lh_rhythm_maker, divisions)
        self._populate_pitches(rh_voice, self.rh_pitch_range)
        self._populate_pitches(lh_voice, self.lh_pitch_range)
        return score

    def _populate_pitches(self, voice, pitch_range):
        assert isinstance(pitch_range, pitchtools.PitchRange)
        numbers = self._random_pitch_numbers
        for note in iterate(voice).by_class(scoretools.Note):
            pass

    def _populate_rhythms(self, voice, rhythm_maker, divisions):
        assert isinstance(voice, scoretools.Voice)
        assert isinstance(divisions, (list, tuple))
        selections = rhythm_maker(divisions)
        for selection in selections:
            voice.extend(selection)

    ### PUBLIC PROPERTIES ###

    @property
    def lh_rhythm_maker(self):
        r'''Gets LH rhythm-maker.

        Defaults to note rhythm-maker.
        '''
        return self._lh_rhythm_maker

    @property
    def lh_pitch_range(self):
        r'''Gets LH pitch range.

        Defaults to ``[C2, C4)``.
        '''
        return self._lh_pitch_range

    @property
    def rh_rhythm_maker(self):
        r'''Gets RH rhythm-maker.

        Defaults to note rhythm-maker.
        '''
        return self._rh_rhythm_maker

    @property
    def rh_pitch_range(self):
        r'''Gets RH pitch range.

        Defaults to ``[C4, C6]``.
        '''
        return self._rh_pitch_range
