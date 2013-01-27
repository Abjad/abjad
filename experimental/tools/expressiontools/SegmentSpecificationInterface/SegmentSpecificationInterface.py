from experimental.tools.expressiontools.SpecificationInterface import SpecificationInterface


class SegmentSpecificationInterface(SpecificationInterface):
    r'''Segment specification interface.

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        
    ::
    
        >>> red_segment = score_specification.append_segment(name='red')

    ::
            
        >>> red_segment
        SegmentSpecificationInterface('red')

    Segment specification properties are read-only.
    '''
    
    ### INITIALIZER ###

    def __init__(self, score_specification, segment_name):
        assert isinstance(segment_name, str), segment_name
        SpecificationInterface.__init__(self, score_specification)
        self._segment_name = segment_name

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Segment specification interface score specification reference::

            >>> z(red_segment.score_specification)
            specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

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
        '''Segment specification interface storage format::

            >>> z(red_segment)
            expressiontools.SegmentSpecificationInterface(
                specificationtools.ScoreSpecification(
                    scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                        staff_count=4
                        )
                    ),
                'red'
                )

        Return string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        '''Segment specification interface timespan::

            >>> red_segment.timespan
            TimespanExpression(anchor='red')

        Return timespan expression.
        '''
        from experimental.tools import expressiontools
        timespan = expressiontools.TimespanExpression(anchor=self.specification_name)
        timespan._score_specification = self.score_specification
        return timespan
