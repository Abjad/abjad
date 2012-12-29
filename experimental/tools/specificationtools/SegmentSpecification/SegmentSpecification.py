import numbers
from abjad.tools import *
from experimental.tools import helpertools
from experimental.tools import requesttools
from experimental.tools import selectortools
from experimental.tools import settingtools
from experimental.tools import timeexpressiontools
from experimental.tools.specificationtools.Specification import Specification


class SegmentSpecification(Specification):
    r'''Segment specification.

    ::

        >>> from experimental.tools import *

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> red_segment = score_specification['red']

    ::
            
        >>> red_segment
        SegmentSpecification('red')

    Segment specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_specification, score_template, segment_name):
        assert isinstance(segment_name, str), segment_name
        Specification.__init__(self, score_specification, score_template)
        self._segment_name = segment_name
        self._time_signatures = []

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        if isinstance(expr, int):
            return self.multiple_context_settings.__getitem__(expr)
        else:
            return self.contexts.__getitem__(expr) 
        
    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_name)

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def abbreviated_context_names(self):
        r'''Segment specification abbreviated context names::

            >>> red_segment.abbreviated_context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Return list of strings.
        '''
        return Specification.abbreviated_context_names.fget(self)

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
            'Staff 3'
            'Voice 3'
            'Staff 4'
            'Voice 4'

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
            'Staff 3'
            'Staff 4'
            'Voice 1'
            'Voice 2'
            'Voice 3'
            'Voice 4'

        Return context proxy dictionary.
        '''
        return Specification.contexts.fget(self)

    @property
    def duration(self):
        '''Segment specification duration.

            >>> red_segment.duration
            Duration(0, 1)

        Return duration.
        '''
        return durationtools.Duration(sum([durationtools.Duration(x) for x in self.time_signatures]))

    @property
    def score_name(self):
        r'''Segment specification score name::

            >>> red_segment.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    # TODO: maybe able to migrate to SegmentSpecificationInterface
    @property
    def score_specification(self):
        '''Read-only reference to score against which segment specification is defined.

        Return score specification.
        '''
        return self._score_specification

    @property
    def score_template(self):
        r'''Segment specification score template::

            >>> red_segment.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

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
    def single_context_settings(self):
        r'''Segment specification single-context settings::

            >>> red_segment.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def single_context_settings_by_context(self):
        r'''Segment specification single-context settings by context::

            >>> for key in red_segment.single_context_settings_by_context:
            ...     key
            ... 
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Staff 2'
            'Staff 3'
            'Staff 4'
            'Voice 1'
            'Voice 2'
            'Voice 3'
            'Voice 4'

        Return context proxy dictionary.
        '''
        return Specification.single_context_settings_by_context.fget(self)

    @property
    def specification_name(self):
        '''Generalized way of refering to both score and segment specifications.

        Specification name of segment specification is same as segment name.

        Return string.
        '''
        return self.segment_name

    @property
    def storage_format(self):
        r'''Segment specification storage format::

            >>> z(red_segment)
            specificationtools.SegmentSpecification(
                specificationtools.ScoreSpecification(
                    scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                        staff_count=4
                        )
                    ),
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    ),
                'red'
                )
        
        Return string.
        '''
        return Specification.storage_format.fget(self)

    # TODO: maybe migrate to SegmentSettingInterface
    @property
    def symbolic_start_offset(self):
        '''Segment specification symbolic start offset::

            >>> red_segment.symbolic_start_offset
            OffsetExpression(anchor='red', edge=Left)

        Return symbolic offset.
        '''
        return timeexpressiontools.OffsetExpression(anchor=self.specification_name, edge=Left)

    # TODO: maybe migrate to SegmentSettingInterface
    @property
    def symbolic_stop_offset(self):
        '''Segment specification symbolic stop offset::

            >>> red_segment.symbolic_stop_offset
            OffsetExpression(anchor='red', edge=Right)

        Return symbolic offset.
        '''
        return timeexpressiontools.OffsetExpression(anchor=self.specification_name, edge=Right)

    @property
    def time_signatures(self):
        '''Time signatures set on segment during time signature interpretation.

                >>> red_segment.time_signatures
                []

        Return list of zero or more nonreduced fractions.
        '''
        return [mathtools.NonreducedFraction(x) for x in self._time_signatures]
