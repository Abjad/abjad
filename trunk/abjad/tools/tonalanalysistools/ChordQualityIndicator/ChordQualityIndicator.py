# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.pitchtools import IntervalSegment


class ChordQualityIndicator(IntervalSegment):
    r'''A chord quality indicator.

    ::

        >>> tonalanalysistools.ChordQualityIndicator(
        ...     'German',
        ...     'augmented sixth',
        ...     )
        GermanAugmentedSixthInRootPosition('P1', '+M3', '+m3', '+aug2')

    Returns chord quality indicator.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('major'),
        )

    _segment_to_quality_and_extent = {
        '<+m3, +m3>': ('diminished', 5),
        '<+m3, +M3>': ('minor', 5),
        '<+M3, +m3>': ('major', 5),
        '<+M3, +M3>': ('augmented', 5),
        '<+M3, M2, +M3>': ('augmented French', 6),
        '<+M3, +m3, +2>': ('augmented German', 6),
        '<+M3, P1, +4>': ('augmented Italian', 6),
        '<+M3, +2, +m3>': ('augmented Swiss', 6),
        '<+m3, +m3, +m3>': ('diminished', 7),
        '<+m3, +m3, +M3>': ('half diminished', 7),
        '<+m3, +M3, +m3>': ('minor', 7),
        '<+M3, +m3, +m3>': ('dominant', 7),
        '<+M3, +m3, +M3>': ('major', 7),
        '<+M3, +m3, +m3, +M3>': ('dominant', 9),
        }

    __slots__ = (
        '_quality_string',
        '_rotation',
        )

    ### INITIALIZER ###

    def __init__(self, quality_string, extent='triad', inversion='root'):
        if extent in ('triad', 5):
            intervals = self._init_triad(quality_string)
        elif extent in ('seventh', 7):
            intervals = self._init_seventh(quality_string)
        elif extent in ('ninth', 9):
            intervals = self._init_ninth(quality_string)
        elif extent in ('augmented sixth', 6):
            intervals = self._init_augmented_sixth(quality_string)
        else:
            raise ValueError('unknown chord quality indicator arguments.')
        intervals, rotation = self._invert_quality_indicator(
            intervals, inversion)
        IntervalSegment.__init__(
            self,
            tokens=intervals,
            item_class=pitchtools.NamedInterval,
            )
        self._quality_string = quality_string
        self._rotation = rotation

    ### SPECIAL METHODS ###

    def __repr__(self):
        parts = []
        if self.item_class.__name__.startswith('Named'):
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return '{}({})'.format(
            self._title_case_name,
            ', '.join(parts),
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _acceptable_augmented_sixth_qualities(self):
        return (
            'french',
            'german',
            'italian',
            'swiss',
            )

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
    def _title_case_name(self):
        return '{}{}In{}'.format(
            stringtools.space_delimited_lowercase_to_upper_camel_case(
                self.quality_string),
            stringtools.space_delimited_lowercase_to_upper_camel_case(
                self.extent_name),
            stringtools.space_delimited_lowercase_to_upper_camel_case(
                self.position),
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _init_augmented_sixth(quality_string):
        if quality_string == 'French':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('major', 2), 
                pitchtools.NamedInterval('major', 3), 
                ]
        elif quality_string == 'German':
            intervals = [
                pitchtools.NamedInterval('major', 3), 
                pitchtools.NamedInterval('minor', 3), 
                pitchtools.NamedInterval('augmented', 2), 
                ]
        elif quality_string == 'Italian':
            intervals = [
                pitchtools.NamedInterval('major', 3), 
                pitchtools.NamedInterval('perfect', 1), 
                pitchtools.NamedInterval('augmented', 4), 
                ]
        elif quality_string == 'Swiss':
            intervals = [
                pitchtools.NamedInterval('major', 3), 
                pitchtools.NamedInterval('augmented', 2), 
                pitchtools.NamedInterval('minor', 3), 
                ]
        else:
           raise ValueError('unaccpetable quality string.')
        intervals.insert(0, pitchtools.NamedInterval('perfect', 1))
        return intervals
        
    @staticmethod
    def _init_ninth(quality_string):
        if quality_string == 'dominant':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('perfect', 5),
                pitchtools.NamedInterval('minor', 7),
                pitchtools.NamedInterval('major', 9),
                ]
        else:
            raise ValueError('unacceptable quality string.')
        intervals.insert(0, pitchtools.NamedInterval('perfect', 1))
        return intervals

    @staticmethod
    def _init_seventh(quality_string):
        if quality_string == 'dominant':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('perfect', 5),
                pitchtools.NamedInterval('minor', 7),
                ]
        elif quality_string == 'major':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('perfect', 5),
                pitchtools.NamedInterval('major', 7),
                ]
        elif quality_string == 'minor':
            intervals = [
                pitchtools.NamedInterval('minor', 3),
                pitchtools.NamedInterval('perfect', 5),
                pitchtools.NamedInterval('minor', 7),
                ]
        elif quality_string in ('diminished', 'fully diminished'):
            intervals = [
                pitchtools.NamedInterval('minor', 3),
                pitchtools.NamedInterval('diminished', 5),
                pitchtools.NamedInterval('diminished', 7),
                ]
        elif quality_string == 'half diminished':
            intervals = [
                pitchtools.NamedInterval('minor', 3),
                pitchtools.NamedInterval('perfect', 5),
                pitchtools.NamedInterval('diminished', 7),
                ]
        else:
           raise ValueError('unaccpetable quality string.')
        intervals.insert(0, pitchtools.NamedInterval('perfect', 1))
        return intervals

    @staticmethod
    def _init_triad(quality_string):
        if quality_string == 'major':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('perfect', 5),
                ]
        elif quality_string == 'minor':
            intervals = [
                pitchtools.NamedInterval('minor', 3),
                pitchtools.NamedInterval('perfect', 5),
                ]
        elif quality_string == 'diminished':
            intervals = [
                pitchtools.NamedInterval('minor', 3),
                pitchtools.NamedInterval('diminished', 5),
                ]
        elif quality_string == 'augmented':
            intervals = [
                pitchtools.NamedInterval('major', 3),
                pitchtools.NamedInterval('augmented', 5),
                ]
        else:
            raise ValueError('unacceptable quality string.')
        intervals.insert(0, pitchtools.NamedInterval('perfect', 1))
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
        from abjad.tools import tonalanalysistools
        return tonalanalysistools.ChordClass.cardinality_to_extent(self.cardinality)

    @property
    def extent_name(self):
        from abjad.tools import tonalanalysistools
        if self._quality_string.lower() in \
            self._acceptable_augmented_sixth_qualities:
            return 'augmented sixth'
        return tonalanalysistools.ChordClass.extent_to_extent_name(self.extent)

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
    def from_interval_class_segment(segment):
        quality, extent = \
            ChordQualityIndicator._segment_to_quality_and_extent[str(segment)]
        return ChordQualityIndicator(quality, extent=extent)
