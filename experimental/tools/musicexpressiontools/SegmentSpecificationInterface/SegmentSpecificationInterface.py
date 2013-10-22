# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.SpecificationInterface \
    import SpecificationInterface


class SegmentSpecificationInterface(SpecificationInterface):
    r'''Segment specification interface.

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template=score_template)

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
        r'''Segment specification interface interpreter representation.

            >>> red_segment
            SegmentSpecificationInterface('red')

        Returns string.
        '''
        return '{}({!r})'.format(self.__class__.__name__, self.segment_name)

    ### PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        r'''Segment specification interface score specification.

        ::

            >>> z(red_segment.score_specification)
            musicexpressiontools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Returns score specification.
        '''
        return SpecificationInterface.score_specification.fget(self)

    @property
    def segment_name(self):
        r'''Segment specification segment name.

        ::

            >>> red_segment.segment_name
            'red'

        Returns string.
        '''
        return self._segment_name

    @property
    def specification(self):
        r'''Segment specification interface specification.

        ::

            >>> red_segment.specification
            SegmentSpecification('red')

        Returns segment specification.
        '''
        return self._specification

    @property
    def specification_name(self):
        r'''Segment specification interface specification name.

        ::

            >>> red_segment.specification_name
            'red'

        Returns string.
        '''
        return self.segment_name

    @property
    def storage_format(self):
        r'''Segment specification interface storage format.

        ::

            >>> z(red_segment)
            musicexpressiontools.SegmentSpecificationInterface(
                musicexpressiontools.ScoreSpecification(
                    scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                        staff_count=4
                        )
                    ),
                'red'
                )

        Returns string.
        '''
        return SpecificationInterface.storage_format.fget(self)

    @property
    def timespan(self):
        r'''Segment specification interface timespan.

        ::

            >>> red_segment.timespan
            TimespanExpression(anchor='red')

        Returns timespan expression.
        '''
        from experimental.tools import musicexpressiontools
        timespan = musicexpressiontools.TimespanExpression(
            anchor=self.specification_name)
        timespan._score_specification = self.score_specification
        return timespan
