# -*- encoding: utf-8 -*-
from abjad.tools import *
from experimental.tools.musicexpressiontools.Specification \
    import Specification


class SegmentSpecification(Specification):
    r'''Segment specification.

    ::

        >>> template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=2)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    ::

        >>> set_expression = \
        ...     red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
        >>> set_expression = \
        ...     orange_segment.set_time_signatures([(4, 16), (4, 16)])
        >>> set_expression = \
        ...     yellow_segment.set_time_signatures([(5, 16), (5, 16)])
        >>> set_expression = red_segment.set_rhythm(library.sixteenths)

    ::

        >>> red_segment = \
        ...     score_specification.specification.segment_specifications['red']
        >>> orange_segment = \
        ...     score_specification.specification.segment_specifications['orange']
        >>> yellow_segment = \
        ...     score_specification.specification.segment_specifications['yellow']

    ::

        >>> score = score_specification.interpret()

    Segment specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template, segment_name):
        assert isinstance(segment_name, str), segment_name
        Specification.__init__(self, score_template)
        self._segment_name = segment_name
        self._time_signatures = []

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats segment specification.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print format(red_segment)
            musicexpressiontools.SegmentSpecification(
                templatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=2,
                    ),
                'red'
                )

        Returns string.
        '''
        superclass = super(SegmentSpecification, self)
        return superclass.__format__(format_specification=format_specification)

    def __repr__(self):
        r'''Segment specification interpreter representation.

        ::

            >>> red_segment
            SegmentSpecification('red')

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self.segment_name)

    ### PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        r'''Segment specification context names.

        ::

            >>> for x in red_segment.context_names:
            ...     x
            ...
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'
            'Staff 2'
            'Voice 2'

        Returns list.
        '''
        return Specification.context_names.fget(self)

    @property
    def fresh_single_context_set_expressions(self):
        r'''Segment specification fresh single-context set expressions.

        ::

            >>> print format(red_segment.fresh_single_context_set_expressions)
            timespantools.TimespanInventory(
                [
                    musicexpressiontools.SingleContextTimeSignatureSetExpression(
                        source_expression=musicexpressiontools.IterablePayloadExpression(
                            payload=(
                                (2, 8),
                                (3, 8),
                                (4, 8),
                                ),
                            ),
                        target_timespan='red',
                        fresh=True,
                        persist=True,
                        ),
                    musicexpressiontools.SingleContextRhythmSetExpression(
                        source_expression=musicexpressiontools.RhythmMakerExpression(
                            payload=rhythmmakertools.BurnishedTaleaRhythmMaker(
                                talea=(1,),
                                talea_denominator=16,
                                beam_each_cell=False,
                                beam_cells_together=True,
                                decrease_durations_monotonically=True,
                                tie_split_notes=False,
                                ),
                            ),
                        target_timespan='red',
                        fresh=True,
                        persist=True,
                        ),
                    ]
                )

        Returns timespan inventory.
        '''
        return Specification.fresh_single_context_set_expressions.fget(self)

    @property
    def score_model(self):
        r'''Segment specification score model.

        ::

            >>> red_segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Returns score.
        '''
        return Specification.score_model.fget(self)

    @property
    def score_name(self):
        r'''Segment specification score name.

        ::

            >>> red_segment.score_name
            'Grouped Rhythmic Staves Score'

        Returns string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Segment specification score template.

        ::

            >>> red_segment.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=2)

        Returns score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_name(self):
        r'''Segment specification name.

        ::

            >>> red_segment.segment_name
            'red'

        Returns string.
        '''
        return self._segment_name

    @property
    def single_context_set_expressions_by_context(self):
        r'''Segment specification single-context set expressions by context.

        ::

            >>> for key in \
            ...     red_segment.single_context_set_expressions_by_context:
            ...     key
            ...
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Staff 2'
            'Voice 1'
            'Voice 2'

        Returns context proxy dictionary.
        '''
        return Specification.single_context_set_expressions_by_context.fget(
            self)

    @property
    def specification_name(self):
        r'''Segment specification specification name.

        ::

            >>> red_segment.specification_name
            'red'

        Returns string.
        '''
        return self.segment_name

    @property
    def time_signatures(self):
        r'''Segment specification time signatures.

        ::

                >>> red_segment.time_signatures
                [NonreducedFraction(2, 8), NonreducedFraction(3, 8), NonreducedFraction(4, 8)]

        Returns list.
        '''
        return [mathtools.NonreducedFraction(x) for x in self._time_signatures]

    @property
    def timespan(self):
        r'''Segment specification timespan.

        ::

            >>> red_segment.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 8))

        Returns timespan.
        '''
        return Specification.timespan.fget(self)
