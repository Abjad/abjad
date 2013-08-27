# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.datastructuretools.TypedTuple import TypedTuple


class IntervalClassSegment(TypedTuple):
    r'''Abjad model of an interval-class segment.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, tokens=None, item_class=None, name=None):
        from abjad.tools import pitchtools 
        if isinstance(tokens, str):
            tokens = tokens.split()
        elif all(isinstance(x, (pitchtools.Pitch, pitchtools.PitchClass))
            for x in tokens):
            tokens = mathtools.difference_series(tokens)
        if item_class is None and tokens is not None:
            if isinstance(tokens, type(self)):
                item_class = tokens.item_class
            elif len(tokens):
                if isinstance(tokens[0], str):
                    item_class = pitchtools.NamedIntervalClass
                elif isinstance(tokens[0], (int, float)):
                    item_class = pitchtools.NumberedIntervalClass
        elif item_class is None:
            item_class = pitchtools.NamedIntervalClass
        assert issubclass(item_class, pitchtools.IntervalClass)
        TypedTuple.__init__(
            self,
            tokens=tokens,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s)' % (self._class_name, self._format_string)

    def __str__(self):
        return '<%s>' % self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return ', '.join([str(x) for x in self])

    ### PUBLIC PROPERTIES ###

    @property
    def is_tertian(self):
        r'''True when all diatonic interval-classes in segment are tertian.
        Otherwise false:

        ::

            >>> interval_class_segment = pitchtools.IntervalClassSegment(
            ...     tokens=[('major', 3), ('minor', 6), ('major', 6)],
            ...     item_class=pitchtools.NamedMelodicIntervalClass,
            ...     )
            >>> interval_class_segment.is_tertian
            True

        Return boolean.
        '''
        from abjad.tools import pitchtools
        inversion_equivalent_interval_class_segment = self.new(
            item_class=pitchtools.NamedInversionEquivalentIntervalClass,
            )
        for interval in inversion_equivalent_interval_class_segment:
            if not interval.number == 3:
                return False
        return True

