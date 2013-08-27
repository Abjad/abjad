# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.PitchClassSet import PitchClassSet


class  NumberedPitchClassSet(PitchClassSet):
    '''Abjad model of a numbered chromatic pitch-class set:

    ::

        >>> ncpcs = pitchtools.NumberedPitchClassSet(
        ...     [-2, -1.5, 6, 7, -1.5, 7])

    ::

        >>> ncpcs
        NumberedPitchClassSet([6, 7, 10, 10.5])

    ::

        >>> print ncpcs
        {6, 7, 10, 10.5}

    Numbered chromatic pitch-class sets are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        PitchClassSet.__init__(
            self,
            tokens=tokens,
            item_class=pitchtools.NumberedPitchClass,
            name=name,
            )

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return '%s([%s])' % (self._class_name, self._format_string)

    def __str__(self):
        return '{%s}' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        result = list(self)
        result.sort(key=lambda x: abs(x))
        return ', '.join([str(x) for x in result])

    ### PUBLIC PROPERTIES ###

    @property
    def prime_form(self):
        r'''To be implemented.
        '''
        return None

    ### PUBLIC METHODS ###

    def invert(self):
        r'''Invert numbered chromatic pitch-class set:

        ::

            >>> ncpcs.invert()
            NumberedPitchClassSet([1.5, 2, 5, 6])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.invert() for pc in self])

    def is_transposed_subset(self, pcset):
        r'''True when self is transposed subset of `pcset`.
        False otherwise:

        ::

            >>> pcset_1 = pitchtools.NumberedPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7])
            >>> pcset_2 = pitchtools.NumberedPitchClassSet(
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
        r'''True when self is transposed superset of `pcset`.
        False otherwise:

        ::

            >>> pcset_1 = pitchtools.NumberedPitchClassSet(
            ... [-2, -1.5, 6, 7, -1.5, 7])
            >>> pcset_2 = pitchtools.NumberedPitchClassSet(
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
        r'''Multiply numbered chromatic pitch-class set by `n`:

        ::

            >>> ncpcs.multiply(5)
            NumberedPitchClassSet([2, 4.5, 6, 11])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.multiply(n) for pc in self])

    def transpose(self, n):
        r'''Transpose numbered chromatic pitch-class set by `n`:

        ::

            >>> ncpcs.transpose(5)
            NumberedPitchClassSet([0, 3, 3.5, 11])

        Return numbered chromatic pitch-class set.
        '''
        return type(self)([pc.transpose(n) for pc in self])
