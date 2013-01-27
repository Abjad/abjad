from abjad.tools import *
from experimental.tools.specificationtools.Specification import Specification


class SegmentSpecification(Specification):
    r'''Segment specification.

    The examples below reference the segment specifications defined here::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    ::

        >>> set_expression = red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
        >>> set_expression = orange_segment.set_time_signatures([(4, 16), (4, 16)])
        >>> set_expression = yellow_segment.set_time_signatures([(5, 16), (5, 16)])
        >>> set_expression = red_segment.set_rhythm(library.sixteenths)

    ::

        >>> red_segment = score_specification['red']
        >>> orange_segment = score_specification['orange']
        >>> yellow_segment = score_specification['yellow']

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

    def __getitem__(self, expr):
        '''Get context with name::

            >>> red_segment['Voice 1']
            ContextProxy()

        Also get multiple-context set-expression with integer `expr`.

        Return multiple-context set-expression or context proxy.
        '''
        if isinstance(expr, int):
            return self.multiple_context_set_expressions.__getitem__(expr)
        else:
            return self.contexts.__getitem__(expr) 
        
    def __repr__(self):
        '''Segment specification interpreter representation::

            >>> red_segment
            SegmentSpecification('red')

        Return string.
        '''
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        r'''Segment specification context names::

            >>> for x in red_segment.context_names:
            ...     x
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'
            'Staff 2'
            'Voice 2'

        Return list of strings.
        '''
        return Specification.context_names.fget(self)

    @property
    def contexts(self):
        r'''Segment specification context proxy dictionary::

            >>> for key in red_segment.contexts:
            ...     key
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Staff 2'
            'Voice 1'
            'Voice 2'

        Return context proxy dictionary.
        '''
        return Specification.contexts.fget(self)

    @property
    def multiple_context_set_expressions(self):
        '''Segment specification multiple-context set-expressions::

            >>> for x in red_segment.multiple_context_set_expressions:
            ...     z(x)

        Return setting inventory.
        '''
        return Specification.multiple_context_set_expressions.fget(self)

    @property
    def score_model(self):
        '''Segment specification score model::

            >>> red_segment.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return Specification.score_model.fget(self)

    @property
    def score_name(self):
        r'''Segment specification score name::

            >>> red_segment.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Segment specification score template::

            >>> red_segment.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=2)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_name(self):
        '''Segment specification name::

            >>> red_segment.segment_name
            'red'

        Return string.
        '''
        return self._segment_name

    @property
    def single_context_set_expressions(self):
        r'''Segment specification single-context settings::

            >>> for x in red_segment.single_context_set_expressions:
            ...     z(x)
            expressiontools.SingleContextSetTimeSignatureExpression(
                expression=expressiontools.PayloadExpression(
                    ((2, 8), (3, 8), (4, 8))
                    ),
                anchor='red',
                fresh=True,
                persist=True
                )
            expressiontools.SingleContextSetRhythmExpression(
                expression=expressiontools.RhythmMakerPayloadExpression(
                    payload=(TaleaRhythmMaker('sixteenths'),)
                    ),
                anchor='red',
                fresh=True,
                persist=True
                )

        Return single-context setting inventory.
        '''
        return Specification.single_context_set_expressions.fget(self)

    @property
    def single_context_set_expressions_by_context(self):
        r'''Segment specification single-context settings by context::

            >>> for key in red_segment.single_context_set_expressions_by_context:
            ...     key
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Staff 2'
            'Voice 1'
            'Voice 2'

        Return context proxy dictionary.
        '''
        return Specification.single_context_set_expressions_by_context.fget(self)

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
        r'''Segment specification storage format::

            >>> z(red_segment)
            specificationtools.SegmentSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=2
                    ),
                'red'
                )
        
        Return string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signatures(self):
        '''Time signatures set on segment during time signature interpretation.

                >>> red_segment.time_signatures
                [NonreducedFraction(2, 8), NonreducedFraction(3, 8), NonreducedFraction(4, 8)]

        Return list of zero or more nonreduced fractions.
        '''
        return [mathtools.NonreducedFraction(x) for x in self._time_signatures]

    @property
    def timespan(self): 
        '''Segment specification timespan::

            >>> red_segment.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 8))

        Return timespan.
        '''
        return Specification.timespan.fget(self)

    ### PUBLIC METHODS ###

    def get_single_context_set_expressions_that_start_during_segment(self, context_name, attribute, 
        include_improper_parentage=False):
        result = []
        context_names = [context_name]
        if include_improper_parentage:
            context_names.extend(self._context_name_to_parentage_names(context_name))
        for context_name in reversed(context_names):
            single_context_set_expressions = self.single_context_set_expressions_by_context[context_name]
            single_context_set_expressions = single_context_set_expressions.get_set_expressions(attribute=attribute)
            result.extend(single_context_set_expressions)
        return result
