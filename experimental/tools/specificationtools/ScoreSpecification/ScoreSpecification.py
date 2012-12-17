import re
from abjad.tools import *
from experimental.tools import helpertools
from experimental.tools import requesttools
from experimental.tools import settingtools
from experimental.tools import symbolictimetools
from abjad.tools import timerelationtools
from experimental.tools.specificationtools.Specification import Specification


class ScoreSpecification(Specification):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Score specification::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(template)

    With three named segments::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    All score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        from experimental.tools import specificationtools
        Specification.__init__(self, self, score_template)
        self._all_division_region_commands = []
        self._all_rhythm_quintuples = []
        self._all_rhythm_region_commands = []
        self._all_time_signature_commands = []
        self._segment_specifications = specificationtools.SegmentSpecificationInventory()
        self._segment_specification_class = specificationtools.SegmentSpecification

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

    def _get_offsets(self, score_specification, context_name):
        assert score_specification is self # is this right?
        return self.offsets

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def abbreviated_context_names(self):
        r'''Score specification abbreviated context names::

            >>> score_specification.abbreviated_context_names
            ['Voice 1', 'Voice 2', 'Voice 3', 'Voice 4']

        Return list of strings.
        '''
        return Specification.abbreviated_context_names.fget(self)

    @property
    def all_division_region_commands(self):
        '''Read-only list of all division region commands.

        Populated at the beginning of division interpretation by interpreter.

        Return list.
        '''
        return self._all_division_region_commands

    @property
    def all_rhythm_quintuples(self):
        '''Read-only list of all rhythm quintuples.

        Return list.
        '''
        return self._all_rhythm_quintuples

    @property
    def all_rhythm_region_commands(self):
        '''Read-only list of all rhythm region commands.

        Populated at the beginning of rhythm interpretation by interpreter.

        Return list.
        '''
        return self._all_rhythm_region_commands

    @property
    def all_time_signature_commands(self):
        '''Read-only list of all time signature settings.

        Populated at the beginning of time signature interpretation by interpreter.

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
            'Staff 3'
            'Voice 3'
            'Staff 4'
            'Voice 4'

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
    def offsets(self):
        r'''Score specification start and stop offsets.

        .. note:: add example.

        Start offset always equal to ``0``.

        Stop offset always equal to score duration.

        Only available after time signature interpretation completes.

        Return offset pair.
        '''
        return self.start_offset, self.stop_offset

    @property
    def score_duration(self):
        r'''Score specification score duration.

        .. note:: add example.

        Only available after time signature interpretation completes.

        Return duration.
        '''
        return self._score_duration

    @property
    def score_name(self):
        r'''Score specification score name::

            >>> score_specification.score_name
            'Grouped Rhythmic Staves Score'

        Return string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_specification(self):
        '''Read-only reference to self.

            >>> score_specification.score_specification
            ScoreSpecification(SegmentSpecificationInventory([SegmentSpecification('red'), SegmentSpecification('orange'), SegmentSpecification('yellow')]))

        Return self.
        '''
        return self
        
    @property
    def score_template(self):
        r'''Score specification score template::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=4)

        Return score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_durations(self):
        r'''Score specification segment durations.

        .. note:: add example.

        Only available after time signature interpretation completes.

        Return list of durations.
        '''
        return self._segment_durations

    @property
    def segment_names(self):
        r'''Score segment names::

            >>> score_specification.segment_names
            ['red', 'orange', 'yellow']

        Return list of zero or more strings.
        '''
        return [segment_specification.segment_name for segment_specification in self.segment_specifications]

    @property
    def segment_offset_pairs(self):
        r'''Score specification segment offset pairs.

        .. note:: add example.

        Only available after time signature interpretation completes.

        Return list of pairs.
        '''
        return self._segment_offset_pairs

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

            >>> score_specification.single_context_settings
            SingleContextSettingInventory([])

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
        
        Specification name of score is always none.

        Return none.
        '''
        return

    @property
    def start_offset(self):
        r'''Score specification start offset.

        .. note:: add example.

        Always equal to ``0``.

        Only available after time signature interpreation.

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        r'''Score specification stop offset.

        .. note:: add example.

        Always equal to duration of entire score.

        Only available after time signature interpreation.

        Return offset.
        '''
        return self._stop_offset

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

        Return list of zero or more nonreduced fractions.
        '''
        result = []
        for segment_specification in self.segment_specifications:
            result.extend(segment_specification.time_signatures)
        return result

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment specification to score specification::

            >>> score_specification.append_segment(name='green')
            SegmentSpecification('green')

        Assign segment `name` or first unused segment number to segment.

        Return segment specification.
        '''
        name = name or str(self._find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = self.segment_specification_class(self, self.score_template, name)
        segment_specification._score_specification = self
        self.segment_specifications.append(segment_specification)
        return segment_specification

    def get_start_segment_specification(self, expr):
        r'''Get start segment specification from `expr`.

        Use ``expr.start_segment_identifier`` to return segment specification.

        Otherwise use `expr` directly to return segment specification::

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
        from experimental.tools import interpretertools

        interpreter = interpretertools.ConcreteInterpreter()
        return interpreter(self)

    def score_offset_to_segment_identifier(self, score_offset):
        r'''Change `score_offset` to segment_identifier.

        This is the same as finding the name of the segment
        in which `score_offset` falls.
        '''
        segment_start_offset, segment_stop_offset = durationtools.Offset(0), None
        for segment in self.segment_specifications:
            segment_stop_offset = segment_start_offset + segment.duration
            if segment_start_offset <= score_offset < segment_stop_offset:
                return segment.segment_name
            segment_start_offset = segment_stop_offset
        raise Exception('score offset {!r} is beyond score duration.'.format(score_offset))

    def score_offsets_to_segment_offset_pairs(self, start_offset=None, stop_offset=None):
        raise NotImplementedError('implement this at some point.')

    def segment_identifier_expression_to_offsets(self, segment_identifier_expression):
        '''Change `segment_identifier_expression` to start offset and stop offset.

        Return pair of offsets.
        '''
        segment_index = self.segment_identifier_expression_to_segment_index(
            segment_identifier_expression)
        return self.segment_offset_pairs[segment_index]

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

        Return pair of start- and stop-offsets.
        '''
        if hasattr(self, 'segment_offset_pairs'):
            start_segment_index = self.segment_name_to_segment_index(segment_name)        
            stop_segment_index = start_segment_index + segment_count - 1
            start_offset_pair = self.segment_offset_pairs[start_segment_index]
            stop_offset_pair = self.segment_offset_pairs[stop_segment_index]
            return start_offset_pair[0], stop_offset_pair[1]

    def segment_offset_to_score_offset(self, segment_name, segment_offset):
        r'''Change `segment_name` and `segment_offset` to score offset.

        If segment offset ``(7, 8)`` is in segment ``'blue'``, how far from the
        beginning of the entire score is this point?

        .. note:: Add example.
        '''
        segment_start_offset, segment_stop_offset = self.segment_name_to_segment_offsets(segment_name)
        score_offset = segment_start_offset + segment_offset
        return score_offset

    def segment_offsets_to_score_offsets(self,
        segment_identifier, segment_start_offset=None, segment_stop_offset=None):
        '''Change `segment_start_offset` and `segment_stop_offset`
        to start offset and stop offset.

        .. note:: Add example.

        Return pair.
        '''
        if segment_start_offset is not None:
            start_offset = self.segment_offset_to_score_offset(segment_identifier, segment_start_offset)
        else:
            start_offset = None
        if segment_stop_offset is not None:
            stop_offset = self.segment_offset_to_score_offset(
                segment_identifier, segment_stop_offset)
        else:
            stop_offset = None
        return start_offset, stop_offset

    def select(self):
        '''Select score::

            >>> score_specification.select()
            ScoreSelector()

        Return score selector.
        '''
        selector = symbolictimetools.ScoreSelector()
        selector._score_specification = self
        return selector

    def select_segments(self, start=None, stop=None):
        '''Select segments::

            >>> score_specification.select_segments('red', ('red', 3))
            SegmentSelector(start_identifier='red', stop_identifier=SegmentIdentifierExpression("'red' + 3"))

        Return segment selector.
        '''
        selector = symbolictimetools.SegmentSelector(start_identifier=start, stop_identifier=stop)
        selector._score_specification = self
        return selector
