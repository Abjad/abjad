from experimental.tools.musicexpressiontools.SpecificationInterface import SpecificationInterface


class ScoreSpecificationInterface(SpecificationInterface):
    r'''Score specification interface.

    Preliminary definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template=score_template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    Score specification interface properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        from experimental.tools import musicexpressiontools
        self._score_template = score_template
        score_specification = musicexpressiontools.ScoreSpecification(score_template)
        score_specification._interface = self
        self._score_specification = score_specification

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Score specification interface score specification.

        ::

            >>> score_specification.score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Return score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

    @property
    def score_template(self):
        '''Score specification interface score template.

        ::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Return score template.
        '''
        return self._score_template

    @property
    def specification(self):
        '''Score specification interface specification.

        ::

            >>> score_specification.specification
            ScoreSpecification('red', 'orange', 'yellow')

        Return score specification.
        '''
        return self._score_specification

    @property
    def specification_name(self):
        '''Score specification interface specification name.

        ::

            >>> score_specification.specification_name is None
            True

        Return none.
        '''
        return SpecificationInterface.specification_name.fget(self)

    @property
    def storage_format(self):
        '''Score specification interface storage format.

        ::

            >>> z(score_specification)
            musicexpressiontools.ScoreSpecificationInterface(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        '''Score specification interface timespan.

        ::

            >>> score_specification.timespan
            TimespanExpression()

        Return timespan expression.
        '''
        return SpecificationInterface.timespan.fget(self)

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        '''Append segment to score specification.

        ::

            >>> score_specification.append_segment(name='green')
            SegmentSpecificationInterface('green')

        Return segment specification interface.
        '''
        return self.score_specification.append_segment(name=name)

    def get_offset(self, offset):
        '''Get score specification offset.

        ::

            >>> offset_expression = score_specification.get_offset(Offset(3, 8))

        ::

            >>> z(offset_expression)
            musicexpressiontools.OffsetExpression(
                anchor=musicexpressiontools.TimespanExpression(),
                callbacks=musicexpressiontools.CallbackInventory([
                    'self._translate(offset, Duration(3, 8))'
                    ])
                )

        Return offset expression.
        '''
        offset = self.timespan.start_offset.translate(offset)
        return offset

    def interpret(self):
        '''Interpret score specification.

        Return score.
        '''
        return self.score_specification.interpret()

    def pop(self, n=None):
        '''Pop segment specification off of score specification.

        Return segment specification.
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
            musicexpressiontools.SegmentSelectExpression(
                voice_name='Voice 1'
                )

        Return segment select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = musicexpressiontools.SegmentSelectExpression(voice_name=voice_name)
        select_expression._score_specification = self.score_specification
        return select_expression
