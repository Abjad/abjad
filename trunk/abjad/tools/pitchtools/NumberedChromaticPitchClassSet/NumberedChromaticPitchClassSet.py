from abjad.tools import sequencetools
from abjad.tools.pitchtools.PitchClassObjectSet import PitchClassObjectSet


class  NumberedChromaticPitchClassSet(PitchClassObjectSet):
    '''.. versionadded:: 2.0

    Abjad model of a numbered chromatic pitch-class set::

        >>> ncpcs = pitchtools.NumberedChromaticPitchClassSet([-2, -1.5, 6, 7, -1.5, 7])

    ::

        >>> ncpcs
        NumberedChromaticPitchClassSet([6, 7, 10, 10.5])

    ::

        >>> print ncpcs
        {6, 7, 10, 10.5}

    Numbered chromatic pitch-class sets are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __new__(klass, expr):
        from abjad.tools import pitchtools
        pcs = []
        # assume expr is iterable
        try:
            for x in expr:
                try:
                    pcs.append(pitchtools.NumberedChromaticPitchClass(x))
                except TypeError:
                    #pcs.extend(get_pitch_classes(x))
                    pcs.extend(pitchtools.get_numbered_chromatic_pitch_classes_from_pitch_carrier(x))
        # if expr is not iterable
        except TypeError:
            # assume expr can be turned into a single pc
            try:
                pc = pitchtools.NumberedChromaticPitchClass(expr)
                pcs.append(pc)
            # expr is a Rest or non-PC type
            except TypeError:
                pcs = []
        return frozenset.__new__(klass, pcs)

    ### SPECIAL METHODS ###

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
        return '%s([%s])' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        result = list(self)
        result.sort(lambda x, y: cmp(abs(x), abs(y)))
        return ', '.join([str(x) for x in result])

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def inversion_equivalent_chromatic_interval_class_set(self):
        '''Read-only inversion-equivalent chromatic interval-class set::

            >>> ncpcs.inversion_equivalent_chromatic_interval_class_set
            InversionEquivalentChromaticIntervalClassSet(0.5, 1, 3, 3.5, 4, 4.5)

        Return inversion-equivalent chromatic interval-class set.
        '''
        from abjad.tools import pitchtools
        interval_class_set = set([])
        for first_pc, second_pc in sequencetools.yield_all_unordered_pairs_of_sequence(self):
            interval_class = first_pc - second_pc
            interval_class_set.add(interval_class)
        interval_class_set = pitchtools.InversionEquivalentChromaticIntervalClassSet(
            interval_class_set)
        return interval_class_set

    @property
    def inversion_equivalent_chromatic_interval_class_vector(self):
        '''Read-only inversion-equivalent chromatic interval-class vector::

            >>> ncpcs.inversion_equivalent_chromatic_interval_class_vector
            InversionEquivalentChromaticIntervalClassVector(0 | 1 0 1 1 0 0 1 0 0 1 1 0)

        Return inversion-equivalent chromatic interval-class vector.
        '''
        from abjad.tools import pitchtools
        interval_classes = []
        for first_pc, second_pc in sequencetools.yield_all_unordered_pairs_of_sequence(self):
            interval_class = first_pc - second_pc
            interval_classes.append(interval_class)
        return pitchtools.InversionEquivalentChromaticIntervalClassVector(interval_classes)

    @property
    def numbered_chromatic_pitch_classes(self):
        '''Read-only numbered chromatic pitch-classes::

            >>> result = ncpcs.numbered_chromatic_pitch_classes

        ::

            >>> for x in result: x
            ...
            NumberedChromaticPitchClass(6)
            NumberedChromaticPitchClass(7)
            NumberedChromaticPitchClass(10)
            NumberedChromaticPitchClass(10.5)

        Return tuple.
        '''
        result = list(self)
        result.sort(lambda x, y: cmp(abs(x), abs(y)))
        return tuple(result)

    @property
    def prime_form(self):
        '''To be implemented.'''
        return None

    ### PUBLIC METHODS ###

    def invert(self):
        '''Invert numbered chromatic pitch-class set::

            >>> ncpcs.invert()
            NumberedChromaticPitchClassSet([1.5, 2, 5, 6])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.invert() for pc in self])

    def is_transposed_subset(self, pcset):
        '''True when self is transposed subset of `pcset`.
        False otherwise::

            >>> pcset_1 = pitchtools.NumberedChromaticPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7])
            >>> pcset_2 = pitchtools.NumberedChromaticPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8])

        ::

            >>> pcset_1.is_transposed_subset(pcset_2)
            True

        Return boolean.
        '''
        for n in range(12):
            if self.transpose(n).issubset(pcset):
                return True
        return False

    def is_transposed_superset(self, pcset):
        '''True when self is transposed superset of `pcset`.
        False otherwise::

            >>> pcset_1 = pitchtools.NumberedChromaticPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7])
            >>> pcset_2 = pitchtools.NumberedChromaticPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7, 7.5, 8])

        ::

            >>> pcset_2.is_transposed_superset(pcset_1)
            True

        Return boolean.
        '''
        for n in range(12):
            if self.transpose(n).issuperset(pcset):
                return True
        return False

    def multiply(self, n):
        '''Multiply numbered chromatic pitch-class set by `n`::

            >>> ncpcs.multiply(5)
            NumberedChromaticPitchClassSet([2, 4.5, 6, 11])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.multiply(n) for pc in self])

    def transpose(self, n):
        '''Transpose numbered chromatic pitch-class set by `n`::

            >>> ncpcs.transpose(5)
            NumberedChromaticPitchClassSet([0, 3, 3.5, 11])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.transpose(n) for pc in self])
