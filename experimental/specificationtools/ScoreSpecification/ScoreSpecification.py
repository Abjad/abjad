from abjad.tools import *
from experimental import helpertools
from experimental import interpretertools
from experimental import requesttools
from experimental import selectortools
from experimental import timespantools
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
from experimental.specificationtools.SegmentSpecificationInventory import SegmentSpecificationInventory
from experimental.specificationtools.Specification import Specification
import re


class ScoreSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Score specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    With three named segments::

        >>> segment = score_specification.append_segment('red')
        >>> segment = score_specification.append_segment('orange')
        >>> segment = score_specification.append_segment('yellow')

    All score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        Specification.__init__(self, score_template)
        self._segment_specifications = SegmentSpecificationInventory()
        self._segment_specification_class = SegmentSpecification

    ### SPECIAL METHODS ###

    def __getitem__(self, expr):
        return self.segment_specifications.__getitem__(expr)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.segment_specifications)

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

            >>> score_specification.context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Only names for which context abbreviations exist are included.

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
        r'''Score specification duration::

            >>> score_specification.duration
            Duration(0, 1)

        Return duration.
        '''

        result = []
        for segment_specification in self.segment_specifications:
            duration = segment_specification.duration
            if duration is not None:
                result.append(duration)
        return durationtools.Duration(sum(result))

    @property
    def resolved_single_context_settings(self):
        r'''Score specification resolved single-context settings::

            >>> for key in score_specification.resolved_single_context_settings:
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
        return Specification.resolved_single_context_settings.fget(self)

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
            <class 'experimental.specificationtools.SegmentSpecification.SegmentSpecification.SegmentSpecification'>
        
        Return segment specification class.
        '''
        return self._segment_specification_class

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
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Return score template.
        '''
        return Specification.score_template.fget(self)

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

            >>> score_specification.single_context_settings
            SingleContextSettingInventory([])

        Return single-context setting inventory.
        '''
        return Specification.single_context_settings.fget(self)

    @property
    def storage_format(self):
        r'''Score specification storage format::

            >>> z(score_specification)
            specificationtools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=4
                    )
                )

        Return string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signatures(self):
        r'''Score specification time signatures::

            >>> score_specification.time_signatures
            []

        Return list of zero or more time signatures.
        '''
        result = []
        for segment_specification in self.segment_specifications:
            time_signatures = segment_specification.time_signatures
            result.extend(segment_specification.time_signatures)
        return result

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment specification to score specification::

            >>> score_specification.append_segment('green')
            SegmentSpecification('green')

        Assign segment `name` or first unused segment number to segment.

        Return segment specification.
        '''
        name = name or str(self._find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = self.segment_specification_class(self.score_template, name)
        self.segment_specifications.append(segment_specification)
        return segment_specification

    def get_segment_specification(self, expr):
        segment_identifier = getattr(expr, 'segment_identifier', expr)
        return self.segment_specifications[segment_identifier]

    def interpret(self):
        r'''Interpret score specification::

            >>> score = score_specification.interpret()

        ::

            >>> f(score)
            \context Score = "Grouped Rhythmic Staves Score" <<
                \context TimeSignatureContext = "TimeSignatureContext" {
                }
                \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                    \context RhythmicStaff = "Staff 1" {
                        \context Voice = "Voice 1" {
                        }
                    }
                    \context RhythmicStaff = "Staff 2" {
                        \context Voice = "Voice 2" {
                        }
                    }
                    \context RhythmicStaff = "Staff 3" {
                        \context Voice = "Voice 3" {
                        }
                    }
                    \context RhythmicStaff = "Staff 4" {
                        \context Voice = "Voice 4" {
                        }
                    }
                >>
            >>

        Return Abjad score object.
        '''
        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def request_divisions(self, voice, start_segment, segment_count=1):
        r'''Request `voice` divisions starting in `start_segment`
        for a total of `segment_count` segments.

            >>> request = score_specification.request_divisions('Voice 1', 'red', segment_count=3)

        ::

            >>> z(request)
            requesttools.AttributeRequest(
                'divisions',
                selectortools.SegmentSliceSelector(
                    start_identifier='red',
                    stop_identifier=helpertools.SegmentIdentifierExpression("'red' + 3")
                    ),
                context_name='Voice 1'
                )

        Return attribute request.
        '''
        start_segment_name = helpertools.expr_to_segment_name(start_segment)
        voice_name = helpertools.expr_to_component_name(voice)
        expression = '{!r} + {}'.format(start_segment_name, segment_count)
        held_expression = helpertools.SegmentIdentifierExpression(expression)
        start, stop = start_segment_name, held_expression
        selector = selectortools.SegmentSliceSelector(start_identifier=start, stop_identifier=stop)
        request = requesttools.AttributeRequest('divisions', selector, context_name=voice_name)
        return request

    def segment_identifier_expression_to_segment_index(self, segment_identifier_expression):
        r'''Segment index expression to segment index::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'red'")
            >>> score_specification.segment_identifier_expression_to_segment_index(segment_identifier_expression)
            0

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'orange'")
            >>> score_specification.segment_identifier_expression_to_segment_index(segment_identifier_expression)
            1

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'yellow'")
            >>> score_specification.segment_identifier_expression_to_segment_index(segment_identifier_expression)
            2

        ::

            >>> segment_identifier_expression = helpertools.SegmentIdentifierExpression("'red' + 'orange' + 'yellow'")
            >>> score_specification.segment_identifier_expression_to_segment_index(segment_identifier_expression)
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
            return self.segment_name_to_segment_index(segment_identifier_expression)
        quoted_string_pattern = re.compile(r"""(['"]{1}[a-zA-Z1-9 _]+['"]{1})""")
        quoted_segment_names = quoted_string_pattern.findall(segment_identifier_expression.string)
        modified_string = str(segment_identifier_expression.string)
        for quoted_segment_name in quoted_segment_names:
            segment_name = quoted_segment_name[1:-1]
            segment_index = self.segment_name_to_segment_index(segment_name)
            modified_string = modified_string.replace(quoted_segment_name, str(segment_index))
        segment_index = eval(modified_string)
        return segment_index

    def segment_name_to_segment_index(self, segment_name):
        r'''Segment name to segment index::

            >>> score_specification.segment_name_to_segment_index('red')
            0

        Return nonnegative integer.
        '''
        segment_specification = self.segment_specifications[segment_name]
        return self.segment_specifications.index(segment_specification)

    def segment_name_to_segment_offsets(self, segment_name, segment_count=1):
        r'''Segment name to segment offsets::

            >>> score_specification.segment_name_to_segment_offsets('red')
            (Offset(0, 1), Offset(0, 1))

        Return offset pair.
        '''
        if hasattr(self, 'segment_offset_pairs'):
            start_segment_index = self.segment_name_to_segment_index(segment_name)        
            stop_segment_index = start_segment_index + segment_count - 1
            start_offset_pair = self.segment_offset_pairs[start_segment_index]
            stop_offset_pair = self.segment_offset_pairs[stop_segment_index]
            return start_offset_pair[0], stop_offset_pair[1]
