from experimental.tools.expressiontools.SpecificationInterface import SpecificationInterface


class ScoreSpecificationInterface(SpecificationInterface):
    r'''Score specification interface.

    Score specification:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = expressiontools.ScoreSpecificationInterface(score_template=score_template)

    With three named segments:

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    All score specification interface properties are read-only.
    '''

    ### INITIALIZER ###

    #def __init__(self, score_specification):
    #    SpecificationInterface.__init__(self, score_specification)

    def __init__(self, score_template):
        from experimental.tools import specificationtools
        self._score_template = score_template
        score_specification = specificationtools.ScoreSpecification(score_template)
        score_specification._interface = self
        self._score_specification = score_specification

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Score specification interface score specification reference::

            >>> score_specification.score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Return score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

    @property
    def score_template(self):
        '''Score specification interface score template.
        
        Return score template.
        '''
        return self._score_template

    @property
    def specification_name(self):
        '''Score specification interface specification name::

            >>> score_specification.specification_name is None
            True

        Return none.
        '''
        return SpecificationInterface.specification_name.fget(self)

    @property
    def storage_format(self):
        '''Score specification interface storage format::

            >>> z(score_specification)
            expressiontools.ScoreSpecificationInterface(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        '''Score specification interface timespan::

            >>> score_specification.timespan
            TimespanExpression()

        Return timespan expression.
        '''
        return SpecificationInterface.timespan.fget(self)
    
    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        '''Append segment.

            >>> score_specification.append_segment(name='green')
            SegmentSpecificationInterface('green')

        Return segment specification interface.
        '''
        return self.score_specification.append_segment(name=name)

    def interpret(self):
        '''Interpret score.
        '''
        return self.score_specification.interpret()

    def select_segments(self, voice_name):
        '''Select voice ``1`` segments in score::

            >>> select_expression = score_specification.select_segments('Voice 1')

        ::

            >>> z(select_expression)
            expressiontools.SegmentSelectExpression(
                voice_name='Voice 1'
                )

        Return segment select expression.
        '''
        from experimental.tools import expressiontools
        select_expression = expressiontools.SegmentSelectExpression(voice_name=voice_name)
        select_expression._score_specification = self
        return select_expression
