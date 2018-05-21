import pathlib
from .SegmentMaker import SegmentMaker


class PianoStaffSegmentMaker(SegmentMaker):
    """
    Piano staff segment-maker.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_divisions',
        '_include_layout_ly',
        '_lh_pitch_range',
        '_lh_rhythm_maker',
        '_rh_pitch_range',
        '_rh_rhythm_maker',
        '_score',
        '_time_signatures',
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
        time_signatures=None,
        divisions=None,
        rh_rhythm_maker=None,
        lh_rhythm_maker=None,
        rh_pitch_range=None,
        lh_pitch_range=None,
        include_layout_ly=None,
        ):
        import abjad
        from abjad import rhythmos
        SegmentMaker.__init__(self)
        time_signatures = time_signatures or []
        time_signatures = [abjad.TimeSignature(_) for _ in time_signatures]
        self._time_signatures = time_signatures
        self._divisions = divisions
        if rh_rhythm_maker is None:
            rh_rhythm_maker = rhythmos.NoteRhythmMaker()
        assert isinstance(rh_rhythm_maker, rhythmos.RhythmMaker)
        self._rh_rhythm_maker = rh_rhythm_maker
        if lh_rhythm_maker is None:
            lh_rhythm_maker = rhythmos.NoteRhythmMaker()
        assert isinstance(lh_rhythm_maker, rhythmos.RhythmMaker)
        self._lh_rhythm_maker = lh_rhythm_maker
        rh_pitch_range = rh_pitch_range or '[C4, C6]'
        rh_pitch_range = abjad.PitchRange(rh_pitch_range)
        self._rh_pitch_range = rh_pitch_range
        lh_pitch_range = lh_pitch_range or '[C2, C4)'
        lh_pitch_range = abjad.PitchRange(lh_pitch_range)
        self._lh_pitch_range = lh_pitch_range
        if include_layout_ly is not None:
            include_layout_ly = bool(include_layout_ly)
        self._include_layout_ly = include_layout_ly

    ### PRIVATE METHODS ###

    def _make_lilypond_file(self, midi=None):
        import abjad
        template = abjad.TwoStaffPianoScoreTemplate()
        score = template()
        self._score = score
        rh_voice = score['RHVoice']
        lh_voice = score['LHVoice']
        self._populate_rhythms(rh_voice, self.rh_rhythm_maker)
        self._populate_rhythms(lh_voice, self.lh_rhythm_maker)
        self._populate_pitches(rh_voice, self.rh_pitch_range)
        self._populate_pitches(lh_voice, self.lh_pitch_range)
        template.attach_defaults(score)
        stylesheet_path = pathlib.Path(
            '..',
            '..',
            'stylesheets',
            'stylesheet.ily',
            )
        lilypond_file = abjad.LilyPondFile.new(
            music=score,
            includes=[stylesheet_path],
            use_relative_includes=True,
            )
        if midi:
            for block in lilypond_file.items[:]:
                if block.name in ('layout', 'paper'):
                    lilypond_file.items.remove(block)
            block = abjad.Block(name='midi')
            lilypond_file.items.append(block)
        if self.include_layout_ly:
            score_block = lilypond_file.score_block
            score = score_block.items[0]
            assert isinstance(score, abjad.Score)
            include = abjad.Container()
            string = r'\include "layout.ly"'
            literal = abjad.LilyPondLiteral(string, 'opening')
            abjad.attach(literal, include)
            container = abjad.Container(
                [include, score],
                is_simultaneous=True,
                )
            score_block.items[:] = [container]
        return lilypond_file

    def _populate_pitches(self, voice, pitch_range):
        import abjad
        assert isinstance(pitch_range, abjad.PitchRange)
        pitch_numbers = [
            _ for _ in self._test_pitch_numbers
            if _ in pitch_range
            ]
        pitch_numbers = abjad.sequence(pitch_numbers).remove_repeats()
        pitch_numbers = abjad.CyclicTuple(pitch_numbers)
        logical_ties = abjad.iterate(voice).logical_ties(pitched=True)
        for i, logical_tie in enumerate(logical_ties):
            pitch_number = pitch_numbers[i]
            for note in logical_tie:
                note.written_pitch = pitch_number

    def _populate_rhythms(self, voice, rhythm_maker):
        import abjad
        assert isinstance(voice, abjad.Voice)
        divisions = self.divisions
        if isinstance(divisions, dict):
            divisions = divisions[voice.name]
        assert isinstance(divisions, (list, tuple))
        selections = rhythm_maker(divisions)
        for selection in selections:
            voice.extend(selection)

    ### PUBLIC PROPERTIES ###

    @property
    def divisions(self):
        """
        Gets divisions of segment-maker.

        Returns list.
        """
        return self._divisions

    @property
    def include_layout_ly(self):
        """
        Is true when segment-maker includes layout.ly.

        Returns true, false or none.
        """
        return self._include_layout_ly

    @property
    def lh_pitch_range(self):
        """
        Gets LH pitch range.

        Defaults to ``[C2, C4)``.
        """
        return self._lh_pitch_range

    @property
    def lh_rhythm_maker(self):
        """
        Gets LH rhythm-maker.

        Defaults to note rhythm-maker.
        """
        return self._lh_rhythm_maker

    @property
    def rh_pitch_range(self):
        """
        Gets RH pitch range.

        Defaults to ``[C4, C6]``.
        """
        return self._rh_pitch_range

    @property
    def rh_rhythm_maker(self):
        """
        Gets RH rhythm-maker.

        Defaults to note rhythm-maker.
        """
        return self._rh_rhythm_maker

    @property
    def time_signatures(self):
        """
        Gets time signatures of segment-maker.

        Returns list or none.
        """
        return self._time_signatures
