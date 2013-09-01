# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet


class NamedPitchClassSet(PitchClassSet):
    '''Abjad model of a named chromatic pitch-class set:

    ::

        >>> named_chromatic_pitch_class_set = \
        ...     pitchtools.NamedPitchClassSet(
        ...     ['gs', 'g', 'as', 'c', 'cs'])

    ::

        >>> named_chromatic_pitch_class_set
        NamedPitchClassSet(['as', 'c', 'cs', 'g', 'gs'])

    ::

        >>> print named_chromatic_pitch_class_set
        {as, c, cs, g, gs}

    Named chromatic pitch-class sets are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        PitchClassSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NamedPitchClass,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._repr_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self._sort_self()])

    @property
    def _repr_string(self):
        return ', '.join([repr(str(x)) for x in self._sort_self()])

    ### PRIVATE METHODS ###

    def _sort_self(self):
        def helper(x, y):
            if x._diatonic_pitch_class_name == y._diatonic_pitch_class_name:
                return cmp(
                    abs(x.numbered_chromatic_pitch_class), 
                    abs(y.numbered_chromatic_pitch_class),
                    )
            else:
                return cmp(
                    x._diatonic_pitch_class_name, 
                    y._diatonic_pitch_class_name,
                    )
        result = list(self)
        result.sort(helper)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_diatonic_interval_class_vector(self):
        from abjad.tools import pitchtools
        pitches = [pitchtools.NamedPitch(x, 4) for x in self]
        return pitchtools.NamedInversionEquivalentIntervalClassVector(
            pitches)

    @property
    def named_chromatic_pitch_classes(self):
        r'''Named chromatic pitch-classes:

        ::

            >>> ncpcs = pitchtools.NamedPitchClassSet(
            ...     ['gs', 'g', 'as', 'c', 'cs'])

        ::

            >>> for x in ncpcs.named_chromatic_pitch_classes:
            ...     x
            NamedPitchClass('as')
            NamedPitchClass('c')
            NamedPitchClass('cs')
            NamedPitchClass('g')
            NamedPitchClass('gs')

        Return tuple.
        '''
        result = list(self)
        return tuple(self._sort_self())

    @property
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return self.new(item_class=pitchtools.NumberedPitchClass)

    ### PUBLIC METHODS ###

    def order_by(self, npc_seg):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if not len(self) == len(npc_seg):
            raise ValueError('set and segment must be of equal length.')
        for npcs in sequencetools.yield_all_permutations_of_sequence(
            self.named_chromatic_pitch_classes):
            candidate_npc_seg = \
                pitchtools.PitchClassSegment(npcs)
            if candidate_npc_seg.is_equivalent_under_transposition(npc_seg):
                return candidate_npc_seg
        message = 'named pitch-class set %s can not order by '
        message += 'named pitch-class segment %s.'
        raise ValueError(message % (self, npc_seg))

    def transpose(self, melodic_diatonic_interval):
        r'''Transpose all npcs in self by melodic diatonic interval.
        '''
        return type(self)([npc + melodic_diatonic_interval for npc in self])
