from experimental.tools.settingtools.SettingInterface import SettingInterface


class SegmentSettingInterface(SettingInterface):
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
        SettingInterface.__init__(self, score_specification)
        self._segment_name = segment_name

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Segment setting interface score specification reference::

            >>> z(red_segment.score_specification)
            specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return score specification.
        '''
        return SettingInterface.score_specification.fget(self)

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
        '''Generalized way of refering to both score and segment specifications::

            >>> red_segment.specification_name
            'red'

        Specification name of segment specification is same as segment name.

        Return string.
        '''
        return self.segment_name

    @property
    def storage_format(self):
        '''Segment setting interface storage format::

            >>> z(red_segment)
            settingtools.SegmentSettingInterface(
                specificationtools.ScoreSpecification(
                    scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                        staff_count=4
                        )
                    ),
                'red'
                )

        Return string.
        '''
        return SettingInterface.storage_format.fget(self)

    @property
    def timespan(self):
        '''Segment setting interface timespan::

            >>> red_segment.timespan
            TimespanExpression(anchor='red')

        Return timespan expression.
        '''
        from experimental.tools import timeexpressiontools
        timespan = timeexpressiontools.TimespanExpression(anchor=self.specification_name)
        timespan._score_specification = self.score_specification
        return timespan
