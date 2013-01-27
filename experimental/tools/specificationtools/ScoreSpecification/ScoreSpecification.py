import re
from abjad.tools import *
from experimental.tools import library
from experimental.tools import expressiontools
from experimental.tools.specificationtools.Specification import Specification


class ScoreSpecification(Specification):
    r'''Score specification.

    The examples below reference the score specification defined here::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    ::

        >>> setting = red_segment.set_time_signatures([(2, 8), (3, 8), (4, 8)])
        >>> setting = orange_segment.set_time_signatures([(4, 16), (4, 16)])
        >>> setting = yellow_segment.set_time_signatures([(5, 16), (5, 16)])
        >>> setting = red_segment.set_rhythm(library.sixteenths)

    ::

        >>> score = score_specification.interpret()
    
    Score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        from experimental.tools import specificationtools
        Specification.__init__(self, score_template)
        self._timespan_scoped_single_context_division_settings = []
        self._division_region_expressions = []
        self._rhythm_region_expressions = []
        self._timespan_scoped_single_context_rhythm_settings = []
        self._time_signature_settings = []
        self._segment_specifications = specificationtools.SegmentSpecificationInventory()
        self._segment_specification_class = specificationtools.SegmentSpecification
        self._interface = expressiontools.ScoreSpecificationInterface(self)

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        '''Get segment specification from segment name::

            >>> score_specification['yellow']
            SegmentSpecification('yellow')

        Get segment specification from segment index::

            >>> score_specification[2]
            SegmentSpecification('yellow')

        Get segment specification from segment identifier expression::

            >>> expression = expressiontools.SegmentIdentifierExpression("'red' + 2")
            >>> score_specification[expression]
            SegmentSpecification('yellow')

        Return segment specification.
        '''
        if isinstance(expr, (str, int)):
            return self.segment_specifications[expr]
        else: 
            quoted_string_pattern = re.compile(r"""(['"]{1}[a-zA-Z1-9 _]+['"]{1})""")
            quoted_segment_names = quoted_string_pattern.findall(expr.string)
            modified_string = str(expr.string)
            for quoted_segment_name in quoted_segment_names:
                segment_name = quoted_segment_name[1:-1]
                segment_specification = self.segment_specifications[segment_name]
                segment_index = self.segment_specifications.index(segment_specification)
                modified_string = modified_string.replace(quoted_segment_name, str(segment_index))
            segment_index = eval(modified_string)
            return self.segment_specifications[segment_index]

    def __repr__(self):
        '''Score specification interpreter representation::

            >>> score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Return string.
        '''
        segment_specification_names = [repr(x.specification_name) for x in self.segment_specifications]
        return '{}({})'.format(self._class_name, ', '.join(segment_specification_names))

    ### PRIVATE METHODS ###

    def _find_first_unused_segment_number(self):
        candidate_segment_number = 1
        while True:
            for segment_specification in self.segment_specifications:
                if segment_specification.segment_name == str(candidate_segment_number):
                    candidate_segment_number += 1
                    break
            else:
                return candidate_segment_number

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        r'''Score specification context names::

            >>> for x in score_specification.context_names:
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
        r'''Score specification context proxy dictionary::

            >>> for key in score_specification.contexts:
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
    def division_region_expressions(self):
        '''Read-only list of division region expressions.

        Popluate during interpretation.

        Return list.
        '''
        return self._division_region_expressions

    @property
    def interface(self):
        '''Read-only reference to score setting interface::

            >>> score_specification.interface
            ScoreSpecificationInterface()

        Return score setting interface.
        '''
        return self._interface

    @property
    def multiple_context_settings(self):
        '''Read-only reference to multiple context settings::

            >>> for x in score_specification.multiple_context_settings:
            ...     z(x)
            expressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                expression=expressiontools.PayloadExpression(
                    ((2, 8), (3, 8), (4, 8))
                    ),
                anchor='red',
                persist=True
                )
            expressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                expression=expressiontools.PayloadExpression(
                    ((4, 16), (4, 16))
                    ),
                anchor='orange',
                persist=True
                )
            expressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                expression=expressiontools.PayloadExpression(
                    ((5, 16), (5, 16))
                    ),
                anchor='yellow',
                persist=True
                )
            expressiontools.MultipleContextSetExpression(
                attribute='rhythm',
                expression=expressiontools.RhythmMakerPayloadExpression(
                    payload=(TaleaRhythmMaker('sixteenths'),)
                    ),
                anchor='red',
                persist=True
                )

        Return context setting proxy.
        '''
        return Specification.multiple_context_settings.fget(self)
    
    @property
    def rhythm_region_expressions(self):
        '''Read-only list of rhythm region expressions:

        ::

            >>> for x in score_specification.rhythm_region_expressions:
            ...     z(x)

        Popluate during interpretation. Then consume during interpretation.

        Return list.
        '''
        return self._rhythm_region_expressions

    @property
    def score_model(self):
        '''Score specification score model::

            >>> score_specification.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Return Abjad score object.
        '''
        return Specification.score_model.fget(self)

    @property
    def score_name(self):
        r'''Score specification score name::

            >>> score_specification.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Score specification score template::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=2)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_names(self):
        r'''Score segment names::

            >>> score_specification.segment_names
            ['red', 'orange', 'yellow']

        Return list of zero or more strings.
        '''
        return [segment_specification.segment_name for segment_specification in self.segment_specifications]

    @property
    def segment_specification_class(self):
        r'''Segment specification class of score specification::

            >>> score_specification.segment_specification_class
            <class 'experimental.tools.specificationtools.SegmentSpecification.SegmentSpecification.SegmentSpecification'>
        
        Return segment specification class.
        '''
        return self._segment_specification_class

    @property
    def segment_specifications(self):
        r'''Segment specifications defined against score specification::

            >>> for segment_specification in score_specification.segment_specifications:
            ...     segment_specification
            ... 
            SegmentSpecification('red')
            SegmentSpecification('orange')
            SegmentSpecification('yellow')

        Return segment specification inventory.
        '''
        return self._segment_specifications

    @property
    def single_context_settings(self):
        r'''Score specification single-context settings::

            >>> for x in score_specification.single_context_settings:
            ...     z(x)
            expressiontools.SingleContextSetTimeSignatureExpression(
                expression=expressiontools.PayloadExpression(
                    ((2, 8), (3, 8), (4, 8))
                    ),
                anchor='red',
                fresh=True,
                persist=True
                )
            expressiontools.SingleContextSetTimeSignatureExpression(
                expression=expressiontools.PayloadExpression(
                    ((4, 16), (4, 16))
                    ),
                anchor='orange',
                fresh=True,
                persist=True
                )
            expressiontools.SingleContextSetTimeSignatureExpression(
                expression=expressiontools.PayloadExpression(
                    ((5, 16), (5, 16))
                    ),
                anchor='yellow',
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
        return Specification.single_context_settings.fget(self)

    @property
    def single_context_settings_by_context(self):
        r'''Score specification single-context settings by context::

            >>> for key in score_specification.single_context_settings_by_context:
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
        return Specification.single_context_settings_by_context.fget(self)

    @property
    def specification_name(self):
        '''Generalized way of refering to both score and segment specifications.

            >>> score_specification.specification_name is None
            True
        
        Specification name of score is always none.

        Return none.
        '''
        return

    @property
    def storage_format(self):
        r'''Score specification storage format::

            >>> z(score_specification)
            specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=2
                    )
                )

        Return string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signature_settings(self):
        '''Read-only list of all time signature settings.

            >>> for x in score_specification.time_signature_settings:
            ...     z(x)

        Populate during interpretation. Then consume during interpretation.

        Return list.
        '''
        return self._time_signature_settings

    @property
    def time_signatures(self):
        r'''Score specification time signatures::

            >>> for x in score_specification.time_signatures:
            ...     x
            NonreducedFraction(2, 8)
            NonreducedFraction(3, 8)
            NonreducedFraction(4, 8)
            NonreducedFraction(4, 16)
            NonreducedFraction(4, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(5, 16)

        Return list of zero or more nonreduced fractions.
        '''
        result = []
        for segment_specification in self.segment_specifications:
            result.extend(segment_specification.time_signatures)
        return result

    @property
    def timespan(self):
        '''Score specification timespan::

            >>> score_specification.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Return timespan.
        '''
        return Specification.timespan.fget(self)

    @property
    def timespan_scoped_single_context_division_settings(self):
        '''Read-only list of all division region commands::

            >>> for x in score_specification.timespan_scoped_single_context_division_settings:
            ...     z(x)
            expressiontools.TimespanScopedSingleContextSetDivisionExpression(
                expression=expressiontools.PayloadExpression(
                    ((2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16))
                    ),
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    ),
                context_name='Voice 1',
                fresh=True,
                truncate=True
                )
            expressiontools.TimespanScopedSingleContextSetDivisionExpression(
                expression=expressiontools.PayloadExpression(
                    ((2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16))
                    ),
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    ),
                context_name='Voice 2',
                fresh=True,
                truncate=True
                )

        Populate during interpretation.

        Return list.
        '''
        return self._timespan_scoped_single_context_division_settings

    @property
    def timespan_scoped_single_context_rhythm_settings(self):
        '''Read-only list of all rhythm region commands.

            >>> for x in score_specification.timespan_scoped_single_context_rhythm_settings:
            ...     z(x)
            expressiontools.TimespanScopedSingleContextSetRhythmExpression(
                expression=expressiontools.RhythmMakerPayloadExpression(
                    payload=(TaleaRhythmMaker('sixteenths'),)
                    ),
                timespan=timespantools.Timespan(
                    start_offset=durationtools.Offset(0, 1),
                    stop_offset=durationtools.Offset(9, 4)
                    ),
                fresh=True
                )

        Populate during interpretation

        Return list.
        '''
        return self._timespan_scoped_single_context_rhythm_settings


    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment specification to score specification::

            >>> score_specification.append_segment(name='green')
            SegmentSpecificationInterface('green')

        Assign segment `name` or first unused segment number to segment.

        Return segment specification.
        '''
        name = name or str(self._find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = self.segment_specification_class(self.score_template, name)
        segment_specification._score_specification = self
        self.segment_specifications.append(segment_specification)
        segment_setting_interface = expressiontools.SegmentSpecificationInterface(self, name)
        return segment_setting_interface

    def clear_persistent_single_context_settings_by_context(self, context_name, attribute):
        if attribute in self.single_context_settings_by_context[context_name]:
            del(self.single_context_settings_by_context[context_name][attribute])

    # TODO: possibly remove in favor of self.get_anchor_timespan().
    def get_start_segment_specification(self, expr):
        r'''Get start segment specification from `expr`::

            >>> score_specification.get_start_segment_specification(1)
            SegmentSpecification('orange')

        Return segment specification or raise key error when none is found.
        '''
        if isinstance(expr, (int, str)):
            start_segment_identifier = expr
        else:
            start_segment_identifier = getattr(expr, 'start_segment_identifier', None)
        if start_segment_identifier is None:
            start_segment_identifier = getattr(expr, 'anchor', None)
        assert isinstance(start_segment_identifier, (int, str)), repr(start_segment_identifier)
        return self.segment_specifications[start_segment_identifier]

    def get_time_signature_slice(self, timespan):
        '''Get time signature slice::

            >>> timespan = timespantools.Timespan((0, 4), (5, 4))
            >>> score_specification.get_time_signature_slice(timespan)
            [(2, 8), (3, 8), (4, 8), (2, 16)]

        Return list.
        '''
        assert self.time_signatures
        weights = [timespan.start_offset, timespan.duration]
        shards = sequencetools.split_sequence_by_weights(
            self.time_signatures, weights, cyclic=False, overhang=False)
        result = shards[1]
        result = [x.pair for x in result]
        return result

    def get_timespan_scoped_single_context_settings_for_voice(self, attribute, context_name):
        timespan_scoped_settings = expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for segment_specification in self.segment_specifications:
            single_context_settings = \
                segment_specification.get_single_context_settings_that_start_during_segment(
                context_name, attribute, include_improper_parentage=True)
            for single_context_setting in single_context_settings:
                timespan_scoped_setting = single_context_setting.to_timespan_scoped_setting()
                # make sure setting was setting for timespan that exists in current segment
                if timespan_scoped_setting.timespan.is_well_formed:
                    timespan_scoped_settings.append(timespan_scoped_setting)
        assert timespan_scoped_settings.all_are_well_formed
        return timespan_scoped_settings

    def interpret(self):
        r'''Interpret score specification.

        Return Abjad score object.
        '''
        from experimental.tools import interpretertools

        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def make_default_timespan_scoped_single_context_division_setting(self, voice_name, timespan):
        divisions = self.get_time_signature_slice(timespan)
        return expressiontools.TimespanScopedSingleContextSetDivisionExpression(
            expression=expressiontools.PayloadExpression(divisions),
            timespan=timespan,
            context_name=voice_name,
            fresh=True,
            truncate=True
            )

    def make_default_timespan_scoped_single_context_rhythm_setting(self, voice_name, timespan):
        return expressiontools.TimespanScopedSingleContextSetRhythmExpression(
            expression=expressiontools.RhythmMakerPayloadExpression(library.skip_tokens),
            timespan=timespan,
            context_name=voice_name,
            fresh=True
            )

    def make_default_timespan_scoped_single_context_setting(self, attribute, voice_name, timespan):
        if attribute == 'divisions':
            return self.make_default_timespan_scoped_single_context_division_setting(voice_name, timespan)
        elif attribute == 'rhythm':
            return self.make_default_timespan_scoped_single_context_rhythm_setting(voice_name, timespan)
        else:
            raise ValueError(attribute)
