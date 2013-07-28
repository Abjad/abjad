from experimental.tools.musicexpressiontools.AnchoredExpression \
    import AnchoredExpression
from experimental.tools.musicexpressiontools.LookupMethodMixin \
    import LookupMethodMixin
from experimental.tools.musicexpressiontools.OffsetCallbackMixin \
    import OffsetCallbackMixin


class OffsetExpression(
    AnchoredExpression, OffsetCallbackMixin, LookupMethodMixin):
    r'''Offset expression.

    Definitions:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example. Symbolic offset indicating the right edge of voice ``1`` 
    note ``10`` that starts during segment ``'red'``:

    ::

        >>> notes = red_segment.select_notes_and_chords('Voice 1')
        >>> offset = notes.stop_offset

    ::

        >>> z(offset)
        musicexpressiontools.OffsetExpression(
            anchor=musicexpressiontools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=musicexpressiontools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                ),
            edge=Right
            )

    Offset expressions implement the lookup interface.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, callbacks=None):
        from experimental.tools import musicexpressiontools
        assert edge in (Left, Right, None), repr(edge)
        AnchoredExpression.__init__(self, anchor=anchor)
        OffsetCallbackMixin.__init__(self, callbacks=callbacks)
        self._edge = edge

    ### PUBLIC PROPERTIES ###

    @property
    def edge(self):
        '''Offset expression edge.

        Return boolean or none.
        '''
        return self._edge

    ### PUBLIC METHODS ##

    def evaluate(self):
        '''Evaluate offset expression.

        Return none when nonevaluable.

        Return payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        edge = self.edge or Left
        anchor_timespan = self._evaluate_anchor_timespan()
        if anchor_timespan is None:
            return
        if edge == Left:
            offset = anchor_timespan.start_offset
        else:
            offset = anchor_timespan.stop_offset
        offset = self._apply_callbacks(offset)
        expression = musicexpressiontools.IterablePayloadExpression([offset])
        return expression
