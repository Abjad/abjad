# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.SpecificationInterface \
    import SpecificationInterface


class ScoreSpecificationInterface(SpecificationInterface):
    r'''Score specification interface.

    Preliminary definitions:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)

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
        score_specification = \
            musicexpressiontools.ScoreSpecification(score_template)
        score_specification._interface = self
        self._score_specification = score_specification

    ### PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        r'''Score specification interface score specification.

        ::

            >>> score_specification.score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Returns score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

    @property
    def score_template(self):
        r'''Score specification interface score template.

        ::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Returns score template.
        '''
        return self._score_template

    @property
    def specification(self):
        r'''Score specification interface specification.

        ::

            >>> score_specification.specification
            ScoreSpecification('red', 'orange', 'yellow')

        Returns score specification.
        '''
        return self._score_specification

    @property
    def specification_name(self):
        r'''Score specification interface specification name.

        ::

            >>> score_specification.specification_name is None
            True

        Returns none.
        '''
        return SpecificationInterface.specification_name.fget(self)

    @property
    def storage_format(self):
        r'''Score specification interface storage format.

        ::

            >>> print score_specification.storage_format
            musicexpressiontools.ScoreSpecificationInterface(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Returns string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        r'''Score specification interface timespan.

        ::

            >>> score_specification.timespan
            TimespanExpression()

        Returns timespan expression.
        '''
        return SpecificationInterface.timespan.fget(self)

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment to score specification.

        ::

            >>> score_specification.append_segment(name='green')
            SegmentSpecificationInterface('green')

        Returns segment specification interface.
        '''
        return self.score_specification.append_segment(name=name)

    def get_offset(self, offset):
        r'''Get score specification offset.

        ::

            >>> offset_expression = \
            ...     score_specification.get_offset(Offset(3, 8))

        ::

            >>> print offset_expression.storage_format
            musicexpressiontools.OffsetExpression(
                anchor=musicexpressiontools.TimespanExpression(),
                callbacks=musicexpressiontools.CallbackInventory([
                    'self._translate(offset, Duration(3, 8))'
                    ])
                )

        Returns offset expression.
        '''
        offset = self.timespan.start_offset.translate(offset)
        return offset

    def interpret(self):
        r'''Interpret score specification.

        Returns score.
        '''
        return self.score_specification.interpret()

    def pop(self, n=None):
        r'''Pop segment specification off of score specification.

        Returns segment specification.
        '''
        if n is None:
            return self.score_specification.segment_specifications.pop()
        else:
            return self.score_specification.segment_specifications.pop(n)

    def select_segments(self, voice_name):
        r'''Select voice ``1`` segments in score:

        ::

            >>> select_expression = \
            ...     score_specification.select_segments('Voice 1')

        ::

            >>> print select_expression.storage_format
            musicexpressiontools.SegmentSelectExpression(
                voice_name='Voice 1'
                )

        Returns segment select expression.
        '''
        from experimental.tools import musicexpressiontools
        select_expression = musicexpressiontools.SegmentSelectExpression(
            voice_name=voice_name)
        select_expression._score_specification = self.score_specification
        return select_expression
