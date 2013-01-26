from experimental.tools.settingtools.AnchoredExpression import AnchoredExpression
from experimental.tools.settingtools.LookupMethodMixin import LookupMethodMixin
from experimental.tools.settingtools.OffsetCallbackMixin import OffsetCallbackMixin


class OffsetExpression(AnchoredExpression, OffsetCallbackMixin, LookupMethodMixin):
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
            anchor=settingtools.CounttimeComponentSelectExpression(
                anchor='red',
                classes=settingtools.ClassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                voice_name='Voice 1'
                ),
            edge=Right
            )

    Offset expressions implement the lookup interface.

    Offset expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, edge=None, callbacks=None):
        from experimental.tools import settingtools
        assert edge in (Left, Right, None), repr(edge)
        AnchoredExpression.__init__(self, anchor=anchor)
        OffsetCallbackMixin.__init__(self, callbacks=callbacks)
        self._edge = edge

    ### PRIVATE METHODS ###

    def evaluate(self):
        from experimental.tools import settingtools
        edge = self.edge or Left
        anchor_timespan = self.get_anchor_timespan()
        if edge == Left:
            offset = anchor_timespan.start_offset
        else:
            offset = anchor_timespan.stop_offset
        offset = self._apply_callbacks(offset)
        expression = settingtools.PayloadExpression([offset])
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def edge(self):
        '''Offset expression edge:

        ::
        
            >>> offset.edge
            Right

        Value of none is interpreted as ``Left``.

        Return boolean or none.
        '''
        return self._edge
