# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import pitchtools
from abjad.tools.pitchtools import IntervalSegment


class RootlessChordClass(IntervalSegment):
    r'''Rootless chord class.

    ::

        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        Major triad in root position:

        ::

            >>> tonalanalysistools.RootlessChordClass('major')
            MajorTriadInRootPosition('P1', '+M3', '+P5')

    ..  container:: example

        Dominant seventh in root position:

        ::

            >>> tonalanalysistools.RootlessChordClass('dominant', 7)
            DominantSeventhInRootPosition('P1', '+M3', '+P5', '+m7')

    ..  container:: example

        German augmented sixth in root position:

        >>> tonalanalysistools.RootlessChordClass('German', 'augmented sixth')
        GermanAugmentedSixthInRootPosition('P1', '+M3', '+m3', '+aug2')

    '''

    ### CLASS VARIABLES ###

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

    def __init__(
        self,
        quality_string='major',
        extent='triad',
        inversion='root',
        ):
        if extent in ('triad', 5):
            intervals = self._initialize_triad(quality_string)
        elif extent in ('seventh', 7):
            intervals = self._initialize_seventh(quality_string)
        elif extent in ('ninth', 9):
            intervals = self._initialize_ninth(quality_string)
        elif extent in ('augmented sixth', 6):
            intervals = self._initialize_augmented_sixth(quality_string)
        else:
            message = 'unknown chord quality arguments.'
            raise ValueError(message)
        intervals, rotation = self._invert_chord_quality(
            intervals, inversion)
        IntervalSegment.__init__(
            self,
            items=intervals,
            item_class=pitchtools.NamedInterval,
            )
        self._quality_string = quality_string
        self._rotation = rotation

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Gets interpreter representation of rootless chord-class.

        Returns string.
        '''
        parts = []
        if self.item_class.__name__.startswith('Named'):
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return '{}({})'.format(
            self._title_case_name,
            ', '.join(parts),
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _initialize_augmented_sixth(quality_string):
        if quality_string == 'French':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('M2'),
                pitchtools.NamedInterval('M3'),
                ]
        elif quality_string == 'German':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('aug2'),
                ]
        elif quality_string == 'Italian':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('P1'),
                pitchtools.NamedInterval('aug4'),
                ]
        elif quality_string == 'Swiss':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('aug2'),
                pitchtools.NamedInterval('m3'),
                ]
        else:
            message = 'unaccpetable quality string.'
            raise ValueError(message)
        intervals.insert(0, pitchtools.NamedInterval('P1'))
        return intervals

    @staticmethod
    def _initialize_ninth(quality_string):
        if quality_string == 'dominant':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('P5'),
                pitchtools.NamedInterval('m7'),
                pitchtools.NamedInterval('M9'),
                ]
        else:
            message = 'unacceptable quality string.'
            raise ValueError(message)
        intervals.insert(0, pitchtools.NamedInterval('P1'))
        return intervals

    @staticmethod
    def _initialize_seventh(quality_string):
        if quality_string == 'dominant':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('P5'),
                pitchtools.NamedInterval('m7'),
                ]
        elif quality_string == 'major':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('P5'),
                pitchtools.NamedInterval('M7'),
                ]
        elif quality_string == 'minor':
            intervals = [
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('P5'),
                pitchtools.NamedInterval('m7'),
                ]
        elif quality_string in ('diminished', 'fully diminished'):
            intervals = [
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('dim5'),
                pitchtools.NamedInterval('dim7'),
                ]
        elif quality_string == 'half diminished':
            intervals = [
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('P5'),
                pitchtools.NamedInterval('dim7'),
                ]
        else:
           message = 'unaccpetable quality string.'
           raise ValueError(message)
        intervals.insert(0, pitchtools.NamedInterval('P1'))
        return intervals

    @staticmethod
    def _initialize_triad(quality_string):
        if quality_string == 'major':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('P5'),
                ]
        elif quality_string == 'minor':
            intervals = [
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('P5'),
                ]
        elif quality_string == 'diminished':
            intervals = [
                pitchtools.NamedInterval('m3'),
                pitchtools.NamedInterval('dim5'),
                ]
        elif quality_string == 'augmented':
            intervals = [
                pitchtools.NamedInterval('M3'),
                pitchtools.NamedInterval('aug5'),
                ]
        else:
            message = 'unacceptable quality string: {!r}.'
            message = message.format(quality_string)
            raise ValueError(message)
        intervals.insert(0, pitchtools.NamedInterval('P1'))
        return intervals

    @staticmethod
    def _invert_chord_quality(intervals, inversion):
        import abjad
        if isinstance(inversion, int):
            intervals = abjad.Sequence(intervals).rotate(n=-inversion)
            rotation = -inversion
        elif inversion == 'root':
            rotation = 0
        elif inversion == 'first':
            intervals = abjad.Sequence(intervals).rotate(n=-1)
            rotation = -1
        elif inversion == 'second':
            intervals = abjad.Sequence(intervals).rotate(n=-2)
            rotation = -2
        elif inversion == 'third':
            intervals = abjad.Sequence(intervals).rotate(n=-3)
            rotation = -3
        elif inversion == 'fourth':
            intervals = abjad.Sequence(intervals).rotate(n=-4)
            rotation = -4
        else:
            message = 'unknown chord inversion: {!r}.'
            raise ValueError(message.format(inversion))
        return intervals, rotation

    ### PUBLIC METHODS ###

    @staticmethod
    def from_interval_class_segment(segment):
        r'''Makes new rootless chord-class from `segment`.

        ..  container:: example

            ::

                >>> segment = abjad.IntervalClassSegment([
                ...     abjad.NamedInversionEquivalentIntervalClass('m3'),
                ...     abjad.NamedInversionEquivalentIntervalClass('m3'),
                ...     ])
                >>> class_ = tonalanalysistools.RootlessChordClass
                >>> class_.from_interval_class_segment(segment)
                DiminishedTriadInRootPosition('P1', '+m3', '+dim5')

        ..  container:: example

                >>> segment = abjad.IntervalClassSegment([
                ...     abjad.NamedInversionEquivalentIntervalClass('m3'),
                ...     abjad.NamedInversionEquivalentIntervalClass('M3'),
                ...     ])
                >>> class_ = tonalanalysistools.RootlessChordClass
                >>> class_.from_interval_class_segment(segment)
                MinorTriadInRootPosition('P1', '+m3', '+P5')

        ..  container:: example

                >>> segment = abjad.IntervalClassSegment([
                ...     abjad.NamedInversionEquivalentIntervalClass('M3'),
                ...     abjad.NamedInversionEquivalentIntervalClass('m3'),
                ...     ])
                >>> class_ = tonalanalysistools.RootlessChordClass
                >>> class_.from_interval_class_segment(segment)
                MajorTriadInRootPosition('P1', '+M3', '+P5')

        Returns new rootless chord-class.
        '''
        quality, extent = RootlessChordClass._segment_to_quality_and_extent[
            str(segment)
            ]
        return RootlessChordClass(quality, extent=extent)

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
            datastructuretools.String(self.quality_string).to_upper_camel_case(),
            datastructuretools.String(self.extent_name).to_upper_camel_case(),
            datastructuretools.String(self.position).to_upper_camel_case(),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        r'''Gets cardinality.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).cardinality
                4

        Returns nonnegative integer.
        '''
        return len(self)

    @property
    def extent(self):
        r'''Gets extent.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).extent
                7

        Returns nonnegative integer.
        '''
        from abjad.tools import tonalanalysistools
        return tonalanalysistools.RootedChordClass.cardinality_to_extent(self.cardinality)

    @property
    def extent_name(self):
        r'''Gets extent name.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).extent_name
                'seventh'

        '''
        from abjad.tools import tonalanalysistools
        if self._quality_string.lower() in \
            self._acceptable_augmented_sixth_qualities:
            return 'augmented sixth'
        return tonalanalysistools.RootedChordClass.extent_to_extent_name(self.extent)

    @property
    def inversion(self):
        r'''Gets inversion.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).inversion
                0

        Returns nonnegative integer.
        '''
        return abs(self.rotation)

    @property
    def position(self):
        r'''Gets position.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).position
                'root position'

        Returns string.
        '''
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
            message = 'unknown chord position: {!r}.'
            message = message.format(self)
            raise ValueError(message)

    @property
    def quality_string(self):
        r'''Gets quality string.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).quality_string
                'dominant'

        Returns string.
        '''
        return self._quality_string

    @property
    def rotation(self):
        r'''Gets rotation.

        ..  container:: example

            ::

                >>> tonalanalysistools.RootlessChordClass('dominant', 7).rotation
                0

        Returns nonnegative integer.
        '''
        return self._rotation
