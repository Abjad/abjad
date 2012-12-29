import re
from abjad.tools import *
from experimental.tools import helpertools
from experimental.tools import requesttools
from experimental.tools import selectortools
from experimental.tools import settingtools
from experimental.tools.specificationtools.Specification import Specification


class ScoreSpecification(Specification):
    r'''Score specification.

    ::

        >>> from experimental.tools import *

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
        self._all_division_region_commands = []
        self._all_rhythm_quintuples = []
        self._all_rhythm_region_commands = []
        self._all_time_signature_commands = []
        self._segment_specifications = specificationtools.SegmentSpecificationInventory()
        self._segment_specification_class = specificationtools.SegmentSpecification
        self._interface = settingtools.ScoreSettingInterface(self)

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        '''Get segment specification from segment specification name::

            >>> score_specification['yellow']
            SegmentSpecification('yellow')

        Get segment specification from segment specification index::

            >>> score_specification[2]
            SegmentSpecification('yellow')

        Return segment specification.
        '''
        return self.segment_specifications.__getitem__(expr)

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
    def all_division_region_commands(self):
        '''Read-only list of all division region commands::

            >>> for x in score_specification.all_division_region_commands:
            ...     z(x)
            settingtools.DivisionCommand(
                requesttools.AbsoluteRequest(
                    [(2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16)]
                    ),
                'Voice 1',
                durationtools.Offset(0, 1),
                durationtools.Offset(9, 4),
                fresh=True,
                truncate=True
                )
            settingtools.DivisionCommand(
                requesttools.AbsoluteRequest(
                    [(2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16)]
                    ),
                'Voice 2',
                durationtools.Offset(0, 1),
                durationtools.Offset(9, 4),
                fresh=True,
                truncate=True
                )

        Populate during interpretation.

        Return list.
        '''
        return self._all_division_region_commands

    @property
    def all_rhythm_quintuples(self):
        '''Read-only list of all rhythm quintuples.

            >>> for x in score_specification.all_rhythm_quintuples:
            ...     z(x)

        Popluate during interpretation. Then consume during interpretation.

        Return list.
        '''
        return self._all_rhythm_quintuples

    @property
    def all_rhythm_region_commands(self):
        '''Read-only list of all rhythm region commands.

            >>> for x in score_specification.all_rhythm_region_commands:
            ...     z(x)
            settingtools.RhythmCommand(
                requesttools.AbsoluteRequest(
                    rhythmmakertools.TaleaRhythmMaker(
                        [1],
                        16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        )
                    ),
                None,
                durationtools.Offset(0, 1),
                durationtools.Offset(9, 4),
                fresh=True
                )

        Populate during interpretation

        Return list.
        '''
        return self._all_rhythm_region_commands

    @property
    def all_time_signature_commands(self):
        '''Read-only list of all time signature settings.

            >>> for x in score_specification.all_time_signature_commands:
            ...     z(x)

        Populate during interpretation. Then consume during interpretation.

        Return list.
        '''
        return self._all_time_signature_commands

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
    def interface(self):
        '''Read-only reference to score setting interface::

            >>> score_specification.interface
            ScoreSettingInterface()

        Return score setting interface.
        '''
        return self._interface

    @property
    def multiple_context_settings(self):
        '''Read-only reference to multiple context settings::

            >>> for x in score_specification.multiple_context_settings:
            ...     z(x)
            settingtools.MultipleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(2, 8), (3, 8), (4, 8)]
                    ),
                anchor='red',
                persist=True
                )
            settingtools.MultipleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(4, 16), (4, 16)]
                    ),
                anchor='orange',
                persist=True
                )
            settingtools.MultipleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(5, 16), (5, 16)]
                    ),
                anchor='yellow',
                persist=True
                )
            settingtools.MultipleContextSetting(
                attribute='rhythm',
                request=requesttools.AbsoluteRequest(
                    rhythmmakertools.TaleaRhythmMaker(
                        [1],
                        16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        )
                    ),
                anchor='red',
                persist=True
                )

        Return context setting proxy.
        '''
        return Specification.multiple_context_settings.fget(self)
    
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
            settingtools.SingleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(2, 8), (3, 8), (4, 8)]
                    ),
                anchor='red',
                fresh=True,
                persist=True
                )
            settingtools.SingleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(4, 16), (4, 16)]
                    ),
                anchor='orange',
                fresh=True,
                persist=True
                )
            settingtools.SingleContextSetting(
                attribute='time_signatures',
                request=requesttools.AbsoluteRequest(
                    [(5, 16), (5, 16)]
                    ),
                anchor='yellow',
                fresh=True,
                persist=True
                )
            settingtools.SingleContextSetting(
                attribute='rhythm',
                request=requesttools.AbsoluteRequest(
                    rhythmmakertools.TaleaRhythmMaker(
                        [1],
                        16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        )
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

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment specification to score specification::

            >>> score_specification.append_segment(name='green')
            SegmentSettingInterface('green')

        Assign segment `name` or first unused segment number to segment.

        Return segment specification.
        '''
        name = name or str(self._find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = self.segment_specification_class(self.score_template, name)
        segment_specification._score_specification = self
        self.segment_specifications.append(segment_specification)
        segment_setting_interface = settingtools.SegmentSettingInterface(self, name)
        return segment_setting_interface

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

    def interpret(self):
        r'''Interpret score specification::

            >>> score = score_specification.interpret()

        ::
    
            >>> isinstance(score, scoretools.Score)
            True

        Return Abjad score object.
        '''
        from experimental.tools import interpretertools

        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def segment_identifier_expression_to_segment_index(self, segment_identifier_expression):
        r'''Segment index expression to segment index::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'red'")
            >>> score_specification.segment_identifier_expression_to_segment_index(
            ... segment_identifier_expression)
            0

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'orange'")
            >>> score_specification.segment_identifier_expression_to_segment_index(
            ... segment_identifier_expression)
            1

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'yellow'")
            >>> score_specification.segment_identifier_expression_to_segment_index(
            ... segment_identifier_expression)
            2

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression(
            ... "'red' + 'orange' + 'yellow'")
            >>> score_specification.segment_identifier_expression_to_segment_index(
            ... segment_identifier_expression)
            3

        Evaluate strings directlly::

            >>> score_specification.segment_identifier_expression_to_segment_index('yellow')
            2

        Return integers unchanged::

            >>> score_specification.segment_identifier_expression_to_segment_index(0)
            0

        Return nonnegative integer.
        '''
        if isinstance(segment_identifier_expression, int):
            return segment_identifier_expression
        if isinstance(segment_identifier_expression, str):
            segment_specification = self.segment_specifications[segment_identifier_expression]
            return self.segment_specifications.index(segment_specification)
        quoted_string_pattern = re.compile(r"""(['"]{1}[a-zA-Z1-9 _]+['"]{1})""")
        quoted_segment_names = quoted_string_pattern.findall(segment_identifier_expression.string)
        modified_string = str(segment_identifier_expression.string)
        for quoted_segment_name in quoted_segment_names:
            segment_name = quoted_segment_name[1:-1]
            segment_specification = self.segment_specifications[segment_name]
            segment_index = self.segment_specifications.index(segment_specification)
            modified_string = modified_string.replace(quoted_segment_name, str(segment_index))
        segment_index = eval(modified_string)
        return segment_index

    def segment_identifier_expression_to_timespan(self, segment_identifier_expression):
        '''Change `segment_identifier_expression` to timespan::

            >>> score_specification.segment_identifier_expression_to_timespan('yellow')
            Timespan(start_offset=Offset(13, 8), stop_offset=Offset(9, 4))

        Return timespan.
        '''
        segment_index = self.segment_identifier_expression_to_segment_index(
            segment_identifier_expression)
        segment_specification = self[segment_index]
        return segment_specification.timespan

    def segment_offset_to_score_offset(self, segment_name, segment_offset):
        r'''Change `segment_name` and `segment_offset` to score offset::

            >>> score_specification.segment_offset_to_score_offset('yellow', 0)
            Offset(13, 8)

        Return offset.
        '''
        timespan = self.segment_identifier_expression_to_timespan(segment_name)
        score_offset = timespan.start_offset + segment_offset
        return score_offset
