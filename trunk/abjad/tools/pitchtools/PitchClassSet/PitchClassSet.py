# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools import TypedFrozenset


class PitchClassSet(TypedFrozenset):
    '''Abjad model of a pitch-class set.

    ::

        >>> numbered_pitch_class_set = pitchtools.PitchClassSet(
        ...     tokens=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitchClass,
        ...     )
        >>> numbered_pitch_class_set
        PitchClassSet([6, 7, 10, 10.5])

    ::

        >>> named_pitch_class_set = pitchtools.PitchClassSet(
        ...     tokens=['c', 'ef', 'bqs,', 'd'],
        ...     item_class=pitchtools.NamedPitchClass,
        ...     )
        >>> named_pitch_class_set
        PitchClassSet(['c', 'bqs', 'd', 'ef'])

    Return pitch-class set.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools
        assert item_class in (
            None,
            pitchtools.NamedPitchClass,
            pitchtools.NumberedPitchClass,
            )
        if item_class is None:
            item_class = pitchtools.NumberedPitchClass
        TypedFrozenset.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}([{}])'.format(self._class_name, self._repr_string)

    def __str__(self):
        return '<{}>'.format(self._format_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        from abjad.tools import pitchtools
        parts = []
        if self.item_class is pitchtools.NamedPitchClass:
            parts = [repr(str(x)) for x in self]
        else:
            parts = [str(x) for x in self]
        return ', '.join(parts)

    @property
    def _repr_string(self):
        return self._format_string
