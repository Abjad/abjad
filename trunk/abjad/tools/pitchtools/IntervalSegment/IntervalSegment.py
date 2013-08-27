# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.datastructuretools import TypedTuple


class IntervalSegment(TypedTuple):
    r'''Abjad model of an interval segment.
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
                    item_class = pitchtools.NamedMelodicInterval
                elif isinstance(tokens[0], (int, float)):
                    item_class = pitchtools.NumberedMelodicInterval
        elif item_class is None:
            item_class = pitchtools.NamedMelodicInterval
        assert issubclass(item_class, pitchtools.Interval)
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

    ### PUBLIC METHODS ###

    def rotate(self, n):
        return self.new(self[-n:] + self[:-n])
