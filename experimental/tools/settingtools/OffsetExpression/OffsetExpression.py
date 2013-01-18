from abjad.tools import durationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.LookupMethodMixin import LookupMethodMixin


class OffsetExpression(LookupMethodMixin):
    r'''Offset expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Symbolic offset indicating the right edge of voice ``1`` note ``10`` that starts
    during segment ``'red'``::

        >>> notes = red_segment.select_notes_and_chords('Voice 1')
        >>> offset = notes.stop_offset

    ::

        >>> z(offset)
        settingtools.OffsetExpression(
            anchor=selectortools.CounttimeComponentSelector(
                anchor='red',
                classes=settingtools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                ),
            edge=Right
            )

    Symbolic offsets are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, multiplier=None, addendum=None): 
        from experimental.tools import specificationtools
        from experimental.tools import settingtools
        assert isinstance(anchor, (
            settingtools.TimespanExpression, 
            type(None), str)), repr(anchor)
        assert edge in (Left, Right, None), repr(edge)
        if multiplier is not None:
            multiplier = durationtools.Multiplier(multiplier)
        if addendum is not None:
            addendum = durationtools.Offset(addendum)
        self._anchor = anchor
        self._multiplier = multiplier
        self._edge = edge
        self._addendum = addendum

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a offset with score object indicator,
        edge and addendum all indicating those of `self`.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.anchor == other.anchor:
            return False
        elif not self.edge == other.edge:
            return False
        elif not self.multiplier == other.multiplier:
            return False
        elif not self.addendum == other.addendum:
            return False
        else:
            return True

    ### PRIVATE METHODS ###

    def _get_offset(self, score_specification, context_name):
        edge = self.edge or Left
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        if edge == Left:
            offset = anchor_timespan.start_offset
        else:
            offset = anchor_timespan.stop_offset
        multiplier = self.multiplier or durationtools.Multiplier(1)
        offset *= multiplier
        addendum = self.addendum or durationtools.Offset(0)
        offset += addendum
        return offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def addendum(self):
        '''Symbolic offset addendum specified by user.

            >>> offset.addendum is None
            True

        Value of none is interpreted as ``Offset(0)``.
            
        Return offset or none.
        '''
        return self._addendum

    @property
    def anchor(self):
        '''Symbolic offset anchor specified by user.
        
            >>> z(offset.anchor)
            selectortools.CounttimeComponentSelector(
                anchor='red',
                classes=settingtools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                )

        Value of none is taken equal the entire score.

        Return anchor or none.
        '''
        return self._anchor

    @property
    def edge(self):
        '''Symbolic offset edge indicator specified by user.
        
            >>> offset.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge

    @property
    def multiplier(self):
        '''Symbolic offset multiplier specified by user.

            >>> offset.multiplier is None
            True

        Value of none is interpreted as ``Multiplier(1)``.

        Return multiplier or none.
        '''
        return self._multiplier

    @property
    def start_segment_identifier(self):
        '''Symbolic offset start segment identifier.

            >>> offset.start_segment_identifier
            'red'

        Delegate to ``self.anchor.start_segment_identifier``.

        Return string or none.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier
