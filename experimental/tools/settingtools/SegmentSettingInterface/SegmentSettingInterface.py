from experimental.tools.settingtools.SetMethodMixin import SetMethodMixin
from experimental.tools.timeexpressiontools.SelectMethodMixin import SelectMethodMixin


class SegmentSettingInterface(SelectMethodMixin, SetMethodMixin):
    r'''Segment setting interface.

    ::

        >>> from experimental.tools import *

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        
    ::
    
        >>> red_segment = score_specification.append_segment(name='red')

    ::
            
        >>> red_segment
        SegmentSettingInterface('red')

    Segment specification properties are read-only.
    '''
    
    ### INITIALIZER ###

    def __init__(self, score_specification, segment_name):
        assert isinstance(segment_name, str), segment_name
        #SettingInterface.__init__(self, score_specification)
        self._score_specification = score_specification
        self._segment_name = segment_name

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        return self.specification_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Read-only reference to score against which segment specification is defined.

        Return score specification.
        '''
        return self._score_specification

    @property
    def segment_name(self):
        '''Segment specification name::

            >>> red_segment.segment_name
            'red'

        Return string.
        '''
        return self._segment_name

    @property
    def specification_name(self):
        '''Generalized way of refering to both score and segment specifications.

        Specification name of segment specification is same as segment name.

        Return string.
        '''
        return self.segment_name

    # TODO: decide between this and self.symbolic_start_offset
    @property
    def start_offset(self):
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self._anchor_abbreviation)

    # TODO: decide between this and self.symbolic_stop_offset
    @property
    def stop_offset(self):
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self._anchor_abbreviation, edge=Right)

    @property
    def symbolic_start_offset(self):
        '''Segment specification symbolic start offset::

            >>> red_segment.symbolic_start_offset
            OffsetExpression(anchor='red', edge=Left)

        Return symbolic offset.
        '''
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self.specification_name, edge=Left)

    @property
    def symbolic_stop_offset(self):
        '''Segment specification symbolic stop offset::

            >>> red_segment.symbolic_stop_offset
            OffsetExpression(anchor='red', edge=Right)

        Return symbolic offset.
        '''
        from experimental.tools import timeexpressiontools
        return timeexpressiontools.OffsetExpression(anchor=self.specification_name, edge=Right)

    @property
    def timespan(self):
        from experimental.tools import timeexpressiontools
        timespan = timeexpressiontools.TimespanExpression(anchor=self.specification_name)
        timespan._score_specification = self.score_specification
        return timespan
