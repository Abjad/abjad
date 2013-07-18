from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools.pitchtools import HarmonicDiatonicIntervalSegment
from abjad.tools.pitchtools import HarmonicDiatonicInterval


class ChordQualityIndicator(HarmonicDiatonicIntervalSegment):
    '''Chord quality indicator.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('major'),
        )

    _segment_to_quality_and_extent = {
        '<m3, m3>': ('diminished', 5),
        '<m3, M3>': ('minor', 5),
        '<M3, m3>': ('major', 5),
        '<M3, M3>': ('augmented', 5),
        '<m3, m3, m3>': ('diminished', 7),
        '<m3, m3, M3>': ('half diminished', 7),
        '<m3, M3, m3>': ('minor', 7),
        '<M3, m3, m3>': ('dominant', 7),
        '<M3, m3, M3>': ('major', 7),
        '<M3, m3, m3, M3>': ('dominant', 9),
        }
    ### INITIALIZER ###

    def __new__(self, quality_string, extent='triad', inversion='root'):
        if extent in ('triad', 5):
            intervals = self._init_triad(quality_string)
        elif extent in ('seventh', 7):
            intervals = self._init_seventh(quality_string)
        elif extent in ('ninth', 9):
            intervals = self._init_ninth(quality_string)
        else:
            raise ValueError('unknown chord quality indicator arguments.')
        intervals, rotation = self._invert_quality_indicator(
            intervals, inversion)
        new = tuple.__new__(self, intervals)
        tuple.__setattr__(new, '_rotation', rotation)
        tuple.__setattr__(new, '_quality_string', quality_string)
        return new

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._title_case_name, self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _acceptable_ninth_qualities(self):
        return (
            'dominant',
            )

    @property
    def _acceptable_seventh_qualities(self):
        return (
            'dominant',
            'major',
            'minor',
            'fully diminshed',
            'half diminished',
            )

    @property
    def _acceptable_triad_qualities(self):
        return (
            'major',
            'minor',
            'diminished',
            'augmented',
            )

    @property
    def _chord_position_string(self):
        return self.position.title().replace(' ', '')

    @property
    def _title_case_name(self):
        return '%s%sIn%s' % (self._quality_string.title(),
            self.extent_name.title(), self._chord_position_string)

    ### PRIVATE METHODS ###

    @staticmethod
    def _init_ninth(quality_string):
        if quality_string == 'dominant':
            intervals = [
                HarmonicDiatonicInterval('major', 3),
                HarmonicDiatonicInterval('perfect', 5),
                HarmonicDiatonicInterval('minor', 7),
                HarmonicDiatonicInterval('major', 9),
                ]
        else:
            raise ValueError('unacceptable quality string.')
        intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
        return intervals

    @staticmethod
    def _init_seventh(quality_string):
        if quality_string == 'dominant':
            intervals = [
                HarmonicDiatonicInterval('major', 3),
                HarmonicDiatonicInterval('perfect', 5),
                HarmonicDiatonicInterval('minor', 7),
                ]
        elif quality_string == 'major':
            intervals = [
                HarmonicDiatonicInterval('major', 3),
                HarmonicDiatonicInterval('perfect', 5),
                HarmonicDiatonicInterval('major', 7),
                ]
        elif quality_string == 'minor':
            intervals = [
                HarmonicDiatonicInterval('minor', 3),
                HarmonicDiatonicInterval('perfect', 5),
                HarmonicDiatonicInterval('minor', 7),
                ]
        elif quality_string in ('diminished', 'fully diminished'):
            intervals = [
                HarmonicDiatonicInterval('minor', 3),
                HarmonicDiatonicInterval('diminished', 5),
                HarmonicDiatonicInterval('diminished', 7),
                ]
        elif quality_string == 'half diminished':
            intervals = [
                HarmonicDiatonicInterval('minor', 3),
                HarmonicDiatonicInterval('perfect', 5),
                HarmonicDiatonicInterval('diminished', 7),
                ]
        else:
           raise ValueError('unaccpetable quality string.')
        intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
        return intervals

    @staticmethod
    def _init_triad(quality_string):
        if quality_string == 'major':
            intervals = [
                HarmonicDiatonicInterval('major', 3),
                HarmonicDiatonicInterval('perfect', 5),
                ]
        elif quality_string == 'minor':
            intervals = [
                HarmonicDiatonicInterval('minor', 3),
                HarmonicDiatonicInterval('perfect', 5),
                ]
        elif quality_string == 'diminished':
            intervals = [
                HarmonicDiatonicInterval('minor', 3),
                HarmonicDiatonicInterval('diminished', 5),
                ]
        elif quality_string == 'augmented':
            intervals = [
                HarmonicDiatonicInterval('major', 3),
                HarmonicDiatonicInterval('augmented', 5),
                ]
        else:
            raise ValueError('unacceptable quality string.')
        intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
        return intervals

    @staticmethod
    def _invert_quality_indicator(intervals, inversion):
        if isinstance(inversion, int):
            intervals = sequencetools.rotate_sequence(intervals, -inversion)
            rotation = -inversion
        elif inversion == 'root':
            rotation = 0
        elif inversion == 'first':
            intervals = sequencetools.rotate_sequence(intervals, -1)
            rotation = -1
        elif inversion == 'second':
            intervals = sequencetools.rotate_sequence(intervals, -2)
            rotation = -2
        elif inversion == 'third':
            intervals = sequencetools.rotate_sequence(intervals, -3)
            rotation = -3
        elif inversion == 'fourth':
            intervals = sequencetools.rotate_sequence(intervals, -4)
            rotation = -4
        else:
            message = 'unknown inversion indicator: {!r}.'
            raise ValueError(message.format(inversion))
        return intervals, rotation

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        return len(self)

    @property
    def extent(self):
        from abjad.tools import tonalitytools
        return tonalitytools.ChordClass.cardinality_to_extent(self.cardinality)

    @property
    def extent_name(self):
        from abjad.tools import tonalitytools
        return tonalitytools.ChordClass.extent_to_extent_name(self.extent)

    @property
    def inversion(self):
        return abs(self.rotation)

    @property
    def position(self):
        if self.rotation == 0:
            return 'root position'
        elif self.rotation == -1:
            return 'first inversion'
        elif self.rotation == -2:
            return 'second inversion'
        elif self.rotation == -3:
            return 'third inversion'
        elif self.rotation == -4:
            return 'fourth inversion'
        else:
            raise ValueError('unknown chord position.')

    @property
    def quality_string(self):
        return self._quality_string

    @property
    def rotation(self):
        return self._rotation

    ### PUBLIC METHODS ###

    @staticmethod
    def from_diatonic_interval_class_segment(segment):
        quality, extent = \
            ChordQualityIndicator._segment_to_quality_and_extent[str(segment)]
        return ChordQualityIndicator(quality, extent=extent)
