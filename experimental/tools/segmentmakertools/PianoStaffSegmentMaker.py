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

    ### INITIALIZER ###

    def __init__(
        self,
        rh_rhythm_maker=None,
        lh_rhythm_maker=None,
        rh_pitch_range=None,
        lh_pitch_range=None,
        ):
        SegmentMaker.__init__(self)
        prototype = (rhythmmakertools.RhythmMaker, type(None))
        assert isinstance(rh_rhythm_maker, prototype)
        self._rh_rhythm_maker = rh_rhythm_maker
        assert isinstance(lh_rhythm_maker, prototype)
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
        pass

    def _populate_rhythms(self, voice, rhythm_maker, divisions):
        assert isinstance(voice, scoretools.Voice)
        assert isinstance(divisions, (list, tuple))
        selections = rhythm_maker(divisions)
        for selection in selections:
            pass


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
