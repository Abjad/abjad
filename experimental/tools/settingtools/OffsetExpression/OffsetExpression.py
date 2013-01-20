from abjad.tools import durationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.Expression import Expression
from experimental.tools.settingtools.LookupMethodMixin import LookupMethodMixin


class OffsetExpression(Expression, LookupMethodMixin):
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

    # TODO: initialize with callback inventory
    def __init__(self, anchor=None, edge=None):
        assert edge in (Left, Right, None), repr(edge)
        Expression.__init__(self, anchor=anchor)
        self._edge = edge

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` is a offset with anchor
        and edge equal to offset those of offset expression.
        
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        elif not self.anchor == expr.anchor:
            return False
        elif not self.edge == expr.edge:
            return False
        else:
            return True

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification, context_name):
        edge = self.edge or Left
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        if edge == Left:
            offset = anchor_timespan.start_offset
        else:
            offset = anchor_timespan.stop_offset
        # TODO: apply callbacks
        return offset

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def edge(self):
        '''Symbolic offset edge indicator specified by user.
        
            >>> offset.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge

    # TODO: hoist to Expression
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
