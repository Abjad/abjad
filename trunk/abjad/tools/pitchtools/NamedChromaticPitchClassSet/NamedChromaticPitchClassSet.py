from abjad.tools.pitchtools._PitchClassSet import _PitchClassSet


class NamedChromaticPitchClassSet(_PitchClassSet):
    '''.. versionadded:: 2.0

    Abjad model of a named chromatic pitch-class set::

        abjad> named_chromatic_pitch_class_set = pitchtools.NamedChromaticPitchClassSet(['gs', 'g', 'as', 'c', 'cs'])

    ::

        abjad> named_chromatic_pitch_class_set
        NamedChromaticPitchClassSet(['as', 'c', 'cs', 'g', 'gs'])

    ::

        abjad> print named_chromatic_pitch_class_set
        {as, c, cs, g, gs}

    Named chromatic pitch-class sets are immutable.
    '''

    def __new__(self, expr):
        from abjad.tools import pitchtools
        npcs = []
        # assume expr is iterable
        try:
            for x in expr:
                try:
                    npcs.append(pitchtools.NamedChromaticPitchClass(x))
                except TypeError:
                    # TODO: probably fix next line #
                    npcs.extend(get_pitch_classes(x))
        # if expr is not iterable
        except TypeError:
            # assume expr can be turned into a single pc
            try:
                npc = pitchtools.NamedChromaticPitchClass(expr)
                npcs.append(npc)
            # expr is a Rest or non-PC type
            except TypeError:
                npcs = []
        return frozenset.__new__(self, npcs)

    ### OVERLOADS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            for element in arg:
                if element not in self:
                    return False
            else:
                return True
        return False

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s([%s])' % (type(self).__name__, self._repr_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE ATTRIBUTES ###

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
                return cmp(abs(x.numbered_chromatic_pitch_class), abs(y.numbered_chromatic_pitch_class))
            else:
                return cmp(x._diatonic_pitch_class_name, y._diatonic_pitch_class_name)
        result = list(self)
        result.sort(helper)
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def inversion_equivalent_diatonic_interval_class_vector(self):
        from abjad.tools import pitchtools
        pitches = [pitchtools.NamedChromaticPitch(x, 4) for x in self]
        return pitchtools.InversionEquivalentDiatonicIntervalClassVector(pitches)

    @property
    def numbered_chromatic_pitch_class_set(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedChromaticPitchClassSet(self)

    @property
    def named_chromatic_pitch_classes(self):
        '''Read-only named chromatic pitch-classes::

            abjad> named_chromatic_pitch_class_set = pitchtools.NamedChromaticPitchClassSet(['gs', 'g', 'as', 'c', 'cs'])
            abjad> named_chromatic_pitch_class_set.named_chromatic_pitch_classes # doctest: +SKIP
            (NamedChromaticPitchClass('c'), NamedChromaticPitchClass('cs'), NamedChromaticPitchClass('g'), NamedChromaticPitchClass('gs'), NamedChromaticPitchClass('as'))

        Return tuple.
        '''
        result = list(self)
        return tuple(self._sort_self())

    ### PUBLIC METHODS ###

    def order_by(self, npc_seg):
        from abjad.tools import pitchtools
        from abjad.tools import sequencetools
        if not len(self) == len(npc_seg):
            raise ValueError('set and segment must be of equal length.')
        for npcs in sequencetools.yield_all_permutations_of_sequence(self.named_chromatic_pitch_classes):
            candidate_npc_seg = pitchtools.NamedChromaticPitchClassSegment(npcs)
            if candidate_npc_seg.is_equivalent_under_transposition(npc_seg):
                return candidate_npc_seg
        message = 'named pitch-class set %s can not order by '
        message += 'named pitch-class segment %s.'
        raise ValueError(message % (self, npc_seg))

    def transpose(self, melodic_diatonic_interval):
        '''Transpose all npcs in self by melodic diatonic interval.'''
        return type(self)([npc + melodic_diatonic_interval for npc in self])
