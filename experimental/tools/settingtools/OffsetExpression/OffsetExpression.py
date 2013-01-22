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

    def _evaluate(self, score_specification, context_name):
        edge = self.edge or Left
        anchor_timespan = score_specification.get_anchor_timespan(self, context_name)
        if edge == Left:
            offset = anchor_timespan.start_offset
        else:
            offset = anchor_timespan.stop_offset
        offset = self._apply_callbacks(offset)
        return offset

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty callback inventory.
        '''
        filtered_result = []
        result = AnchoredExpression._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'callbacks=settingtools.CallbackInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

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
