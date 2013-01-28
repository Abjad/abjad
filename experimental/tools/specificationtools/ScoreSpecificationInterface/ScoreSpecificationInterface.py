from experimental.tools.specificationtools.SpecificationInterface import SpecificationInterface


class ScoreSpecificationInterface(SpecificationInterface):
    r'''Score specification interface.

    Score specification:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)

    With three named segments:

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    All score specification interface properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        from experimental.tools import specificationtools
        self._score_template = score_template
        score_specification = specificationtools.ScoreSpecification(score_template)
        score_specification._interface = self
        self._score_specification = score_specification

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        return self.score_specification.__getitem__(expr)

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
            specificationtools.ScoreSpecificationInterface(
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

    def get_offset(self, offset):
        '''Get offset:

        ::

            >>> offset_expression = score_specification.get_offset(Offset(3, 8))

        ::

            >>> z(offset_expression)
            expressiontools.OffsetExpression(
                anchor=expressiontools.TimespanExpression(),
                callbacks=expressiontools.CallbackInventory([
                    'self._translate(offset, Duration(3, 8))'
                    ])
                )

        Return offset expression.
        '''
        offset = self.timespan.start_offset.translate(offset)
        return offset
        
    def interpret(self):
        '''Interpret score.
        '''
        return self.score_specification.interpret()

    def pop(self, n=None):
        '''Pop segment specification off of score specification.
        '''
        if n is None:
            return self.score_specification.segment_specifications.pop()
        else:
            return self.score_specification.segment_specifications.pop(n)
        
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
