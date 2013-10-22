# -*- encoding: utf-8 -*-
import re
from abjad.tools import *
from experimental.tools.musicexpressiontools.Specification \
	import Specification


class ScoreSpecification(Specification):
    r'''Score specification.

    Preliminary definitions:

    ::

        >>> template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=2)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(template)

    ::

        >>> red_segment = score_specification.append_segment(name='red')
        >>> orange_segment = score_specification.append_segment(name='orange')
        >>> yellow_segment = score_specification.append_segment(name='yellow')

    ::

        >>> set_expression = red_segment.set_time_signatures(
        ...     [(2, 8), (3, 8), (4, 8)])
        >>> set_expression = orange_segment.set_time_signatures(
        ...     [(4, 16), (4, 16)])
        >>> set_expression = yellow_segment.set_time_signatures(
        ...     [(5, 16), (5, 16)])
        >>> set_expression = red_segment.set_rhythm(library.sixteenths)

    ::

        >>> score = score_specification.interpret()

    ::

        >>> score_specification = score_specification.specification

    Score specification properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, score_template):
        from experimental.tools import musicexpressiontools
        Specification.__init__(self, score_template)
        self._postrhythm_set_expressions = \
            musicexpressiontools.ExpressionInventory()
        self._multiple_context_set_expressions = \
            timespantools.TimespanInventory()
        self._next_lexical_rank = 0
        self._region_expressions_by_attribute = \
            musicexpressiontools.AttributeDictionary()
        self._segment_specifications = \
            musicexpressiontools.SegmentSpecificationInventory()
        self._segment_specification_class = \
            musicexpressiontools.SegmentSpecification
        self._single_context_time_signature_set_expressions = \
            timespantools.TimespanInventory()
        self._voice_data_structures_by_voice = \
            musicexpressiontools.VoiceDictionary(score_template())

    ### SPECIAL METHODS ###

    def __repr__(self):
        r'''Score specification interpreter representation.

        ::

            >>> score_specification
            ScoreSpecification('red', 'orange', 'yellow')

        Returns string.
        '''
        segment_specification_names = [
            repr(x.specification_name) for x in self.segment_specifications]
        return '{}({})'.format(
            self.__class__.__name__, ', '.join(segment_specification_names))

    ### PRIVATE METHODS ###

    def _compare_expressions(self, x, y):
        result = self.compare_context_names(
            x.target_context_name, y.target_context_name)
        if result in (-1, 1):
            return result
        else:
            return cmp(x._lexical_rank, y._lexical_rank)

    def _find_first_unused_segment_number(self):
        candidate_segment_number = 1
        while True:
            for segment_specification in self.segment_specifications:
                if segment_specification.segment_name == \
                    str(candidate_segment_number):
                    candidate_segment_number += 1
                    break
            else:
                return candidate_segment_number

    ### PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        r'''Score specification context names.

        ::

            >>> for x in score_specification.context_names:
            ...     x
            ...
            'Grouped Rhythmic Staves Score'
            'Grouped Rhythmic Staves Staff Group'
            'Staff 1'
            'Voice 1'
            'Staff 2'
            'Voice 2'

        Returns list of strings.
        '''
        return Specification.context_names.fget(self)

    @property
    def fresh_single_context_set_expressions(self):
        r'''Score specification fresh single-context set expressions.

        ::

            >>> z(score_specification.fresh_single_context_set_expressions)
            timespantools.TimespanInventory([])

        Returns timespan inventory.
        '''
        return Specification.fresh_single_context_set_expressions.fget(self)

    @property
    def interface(self):
        r'''Score specification interface.

        ::

            >>> score_specification.interface
            ScoreSpecificationInterface()

        Returns score specification interface.
        '''
        return self._interface

    @property
    def multiple_context_set_expressions(self):
        r'''Score specification multiple-context set expressions.

        ::

            >>> z(score_specification.multiple_context_set_expressions)
            timespantools.TimespanInventory([
                musicexpressiontools.MultipleContextSetExpression(
                    attribute='time_signatures',
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((2, 8), (3, 8), (4, 8))
                        ),
                    target_timespan='red',
                    persist=True
                    ),
                musicexpressiontools.MultipleContextSetExpression(
                    attribute='time_signatures',
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((4, 16), (4, 16))
                        ),
                    target_timespan='orange',
                    persist=True
                    ),
                musicexpressiontools.MultipleContextSetExpression(
                    attribute='time_signatures',
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((5, 16), (5, 16))
                        ),
                    target_timespan='yellow',
                    persist=True
                    ),
                musicexpressiontools.MultipleContextSetExpression(
                    attribute='rhythm',
                    source_expression=musicexpressiontools.RhythmMakerExpression(
                        payload=rhythmmakertools.TaleaRhythmMaker(
                            talea=[1],
                            talea_denominator=16,
                            prolation_addenda=[],
                            secondary_divisions=[],
                            beam_each_cell=False,
                            beam_cells_together=True,
                            tie_split_notes=False
                            )
                        ),
                    target_timespan='red',
                    persist=True
                    )
                ])

        Returns context dictionary.
        '''
        return self._multiple_context_set_expressions

    @property
    def postrhythm_set_expressions(self):
        r'''Score specification generalized set expressions.

        ::

            >>> z(score_specification.postrhythm_set_expressions)
            musicexpressiontools.ExpressionInventory([])

        Returns expression inventory.
        '''
        return self._postrhythm_set_expressions

    @property
    def region_expressions_by_attribute(self):
        r'''Score specification region expressions by attribute.

        ::

            >>> for timespan_inventory in \
            ...     score_specification.region_expressions_by_attribute.itervalues():
            ...     if timespan_inventory:
            ...         z(timespan_inventory)
            timespantools.TimespanInventory([
                musicexpressiontools.LiteralDivisionRegionExpression(
                    source_expression=((2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16)),
                    start_offset=durationtools.Offset(0, 1),
                    total_duration=durationtools.Duration(9, 4),
                    voice_name='Voice 1'
                    ),
                musicexpressiontools.LiteralDivisionRegionExpression(
                    source_expression=((2, 8), (3, 8), (4, 8), (4, 16), (4, 16), (5, 16), (5, 16)),
                    start_offset=durationtools.Offset(0, 1),
                    total_duration=durationtools.Duration(9, 4),
                    voice_name='Voice 2'
                    )
                ])
            timespantools.TimespanInventory([
                musicexpressiontools.RhythmMakerRhythmRegionExpression(
                    source_expression=rhythmmakertools.TaleaRhythmMaker(
                        talea=[1],
                        talea_denominator=16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        ),
                    division_list=musicexpressiontools.DivisionList(
                        [Division('[2, 8]', start_offset=Offset(0, 1)),
                        Division('[3, 8]', start_offset=Offset(1, 4)),
                        Division('[4, 8]', start_offset=Offset(5, 8)),
                        Division('[4, 16]', start_offset=Offset(9, 8)),
                        Division('[4, 16]', start_offset=Offset(11, 8)),
                        Division('[5, 16]', start_offset=Offset(13, 8)),
                        Division('[5, 16]', start_offset=Offset(31, 16))],
                        start_offset=durationtools.Offset(0, 1),
                        voice_name='Voice 1'
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 1'
                    ),
                musicexpressiontools.RhythmMakerRhythmRegionExpression(
                    source_expression=rhythmmakertools.TaleaRhythmMaker(
                        talea=[1],
                        talea_denominator=16,
                        prolation_addenda=[],
                        secondary_divisions=[],
                        beam_each_cell=False,
                        beam_cells_together=True,
                        tie_split_notes=False
                        ),
                    division_list=musicexpressiontools.DivisionList(
                        [Division('[2, 8]', start_offset=Offset(0, 1)),
                        Division('[3, 8]', start_offset=Offset(1, 4)),
                        Division('[4, 8]', start_offset=Offset(5, 8)),
                        Division('[4, 16]', start_offset=Offset(9, 8)),
                        Division('[4, 16]', start_offset=Offset(11, 8)),
                        Division('[5, 16]', start_offset=Offset(13, 8)),
                        Division('[5, 16]', start_offset=Offset(31, 16))],
                        start_offset=durationtools.Offset(0, 1),
                        voice_name='Voice 2'
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 2'
                    )
                ])

        Returns attribute dictionary.
        '''
        return self._region_expressions_by_attribute

    @property
    def score_model(self):
        r'''Score specification score model.

        ::

            >>> score_specification.score_model
            Score-"Grouped Rhythmic Staves Score"<<1>>

        Returns score.
        '''
        return Specification.score_model.fget(self)

    @property
    def score_name(self):
        r'''Score specification score name.

        ::

            >>> score_specification.score_name
            'Grouped Rhythmic Staves Score'

        Returns string.
        '''
        return Specification.score_name.fget(self)

    @property
    def score_template(self):
        r'''Score specification score template.

        ::

            >>> score_specification.score_template
            GroupedRhythmicStavesScoreTemplate(staff_count=2)

        Returns score template.
        '''
        return Specification.score_template.fget(self)

    @property
    def segment_names(self):
        r'''Score specification segment names.

        ::

            >>> score_specification.segment_names
            ['red', 'orange', 'yellow']

        Returns list.
        '''
        return [segment_specification.segment_name 
            for segment_specification in self.segment_specifications]

    @property
    def segment_specification_class(self):
        r'''Score specification Segment specification class.

        ::

            >>> score_specification.segment_specification_class
            <class 'experimental.tools.musicexpressiontools.SegmentSpecification.SegmentSpecification.SegmentSpecification'>

        Returns segment specification class.
        '''
        return self._segment_specification_class

    @property
    def segment_specifications(self):
        r'''Score specification segment specifications.

        ::

            >>> for segment_specification in \
            ...     score_specification.segment_specifications:
            ...     segment_specification
            ...
            SegmentSpecification('red')
            SegmentSpecification('orange')
            SegmentSpecification('yellow')

        Returns segment specification inventory.
        '''
        return self._segment_specifications

    @property
    def single_context_set_expressions_by_context(self):
        r'''Score specification single-context set expressions by context.

        ::

            >>> for key in \
            ...     score_specification.single_context_set_expressions_by_context:
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
        return Specification.single_context_set_expressions_by_context.fget(self)

    @property
    def single_context_time_signature_set_expressions(self):
        r'''Score specification single-context time signature set expressions.

        ::

            >>> z(score_specification.single_context_time_signature_set_expressions)
            timespantools.TimespanInventory([
                musicexpressiontools.SingleContextTimeSignatureSetExpression(
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((2, 8), (3, 8), (4, 8))
                        ),
                    target_timespan='red',
                    fresh=True,
                    persist=True
                    ),
                musicexpressiontools.SingleContextTimeSignatureSetExpression(
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((4, 16), (4, 16))
                        ),
                    target_timespan='orange',
                    fresh=True,
                    persist=True
                    ),
                musicexpressiontools.SingleContextTimeSignatureSetExpression(
                    source_expression=musicexpressiontools.IterablePayloadExpression(
                        payload=((5, 16), (5, 16))
                        ),
                    target_timespan='yellow',
                    fresh=True,
                    persist=True
                    )
                ])

        Returns timespan inventory.
        '''
        return self._single_context_time_signature_set_expressions

    @property
    def specification_name(self):
        r'''Score specification specification name.

        ::

            >>> score_specification.specification_name is None
            True

        Returns none.
        '''
        return

    @property
    def storage_format(self):
        r'''Score specification storage format.

        ::

            >>> z(score_specification)
            musicexpressiontools.ScoreSpecification(
                scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
                    staff_count=2
                    )
                )

        Returns string.
        '''
        return Specification.storage_format.fget(self)

    @property
    def time_signatures(self):
        r'''Score specification time signatures.

        ::

            >>> for x in score_specification.time_signatures:
            ...     x
            NonreducedFraction(2, 8)
            NonreducedFraction(3, 8)
            NonreducedFraction(4, 8)
            NonreducedFraction(4, 16)
            NonreducedFraction(4, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(5, 16)

        Returns list.
        '''
        if hasattr(self, '_time_signatures'):
            return self._time_signatures
        else:
            result = []
            for segment_specification in self.segment_specifications:
                result.extend(segment_specification.time_signatures)
            return result

    @property
    def timespan(self):
        r'''Score specification timespan.

        ::

            >>> score_specification.timespan
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(9, 4))

        Returns timespan.
        '''
        return Specification.timespan.fget(self)

    @property
    def voice_data_structures_by_voice(self):
        r'''Score specification payload expressions by voice.

        ::

            >>> for voice_proxy in \
            ...     score_specification.voice_data_structures_by_voice.itervalues():
            ...     for timespan_inventory in \
            ...         voice_proxy.payload_expressions_by_attribute.itervalues():
            ...         if timespan_inventory:
            ...             z(timespan_inventory)
            timespantools.TimespanInventory([
                musicexpressiontools.StartPositionedDivisionPayloadExpression(
                    payload=musicexpressiontools.DivisionList(
                        [Division('[2, 8]', start_offset=Offset(0, 1)),
                        Division('[3, 8]', start_offset=Offset(1, 4)),
                        Division('[4, 8]', start_offset=Offset(5, 8)),
                        Division('[4, 16]', start_offset=Offset(9, 8)),
                        Division('[4, 16]', start_offset=Offset(11, 8)),
                        Division('[5, 16]', start_offset=Offset(13, 8)),
                        Division('[5, 16]', start_offset=Offset(31, 16))],
                        start_offset=durationtools.Offset(0, 1),
                        voice_name='Voice 1'
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 1'
                    )
                ])
            timespantools.TimespanInventory([
                musicexpressiontools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=[]
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 1'
                    )
                ])
            timespantools.TimespanInventory([
                musicexpressiontools.StartPositionedDivisionPayloadExpression(
                    payload=musicexpressiontools.DivisionList(
                        [Division('[2, 8]', start_offset=Offset(0, 1)),
                        Division('[3, 8]', start_offset=Offset(1, 4)),
                        Division('[4, 8]', start_offset=Offset(5, 8)),
                        Division('[4, 16]', start_offset=Offset(9, 8)),
                        Division('[4, 16]', start_offset=Offset(11, 8)),
                        Division('[5, 16]', start_offset=Offset(13, 8)),
                        Division('[5, 16]', start_offset=Offset(31, 16))],
                        start_offset=durationtools.Offset(0, 1),
                        voice_name='Voice 2'
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 2'
                    )
                ])
            timespantools.TimespanInventory([
                musicexpressiontools.StartPositionedRhythmPayloadExpression(
                    payload=containertools.Container(
                        music=[]
                        ),
                    start_offset=durationtools.Offset(0, 1),
                    voice_name='Voice 2'
                    )
                ])

        Returns voice dictionary.
        '''
        return self._voice_data_structures_by_voice

    ### PUBLIC METHODS ###

    def append_segment(self, name=None):
        r'''Append segment specification to score specification:

        ::

            >>> score_specification.append_segment(name='green')
            SegmentSpecificationInterface('green')

        Assign segment `name` or first unused segment number to segment.

        Returns segment specification interface.
        '''
        from experimental.tools import musicexpressiontools
        name = name or str(self._find_first_unused_segment_number())
        assert name not in self.segment_names, repr(name)
        segment_specification = \
            self.segment_specification_class(self.score_template, name)
        segment_specification._score_specification = self
        self.segment_specifications.append(segment_specification)
        segment_specification_interface = \
            musicexpressiontools.SegmentSpecificationInterface(self, name)
        segment_specification_interface._specification = segment_specification
        return segment_specification_interface

    def get_segment_specification(self, expr):
        r'''Get segment specification from segment name:

        ::

            >>> score_specification.get_segment_specification('yellow')
            SegmentSpecification('yellow')

        Get segment specification from segment index:

        ::

            >>> score_specification.get_segment_specification(2)
            SegmentSpecification('yellow')

        Get segment specification from segment identifier expression:

        ::

            >>> expression = musicexpressiontools.SegmentIdentifierExpression(
            ...     "'red' + 2")
            >>> score_specification.get_segment_specification(expression)
            SegmentSpecification('yellow')

        Returns segment specification.
        '''
        if isinstance(expr, (str, int)):
            return self.segment_specifications[expr]
        else:
            quoted_string_pattern = re.compile(
                r"""(['"]{1}[a-zA-Z1-9 _]+['"]{1})""")
            quoted_segment_names = quoted_string_pattern.findall(expr.string)
            modified_string = str(expr.string)
            for quoted_segment_name in quoted_segment_names:
                segment_name = quoted_segment_name[1:-1]
                segment_specification = \
                    self.segment_specifications[segment_name]
                segment_index = \
                    self.segment_specifications.index(segment_specification)
                modified_string = \
                    modified_string.replace(
                        quoted_segment_name, str(segment_index))
            segment_index = eval(modified_string)
            return self.segment_specifications[segment_index]

    def get_time_signature_slice(self, timespan):
        r'''Get time signature slice:

        ::

            >>> timespan = timespantools.Timespan((0, 4), (5, 4))
            >>> score_specification.get_time_signature_slice(timespan)
            [(2, 8), (3, 8), (4, 8), (2, 16)]

        Returns list.
        '''
        assert self.time_signatures
        weights = [timespan.start_offset, timespan.duration]
        shards = sequencetools.split_sequence_by_weights(
            self.time_signatures,
            weights,
            cyclic=False,
            overhang=False)
        result = shards[1]
        result = [x.pair for x in result]
        return result

    def interpret(self):
        r'''Interpret score specification.

        Returns Abjad score object.
        '''
        from experimental.tools import musicexpressiontools
        interpreter = musicexpressiontools.ConcreteInterpreter()
        self.interpreter = interpreter
        return interpreter(self)

    def make_default_timespan_scoped_single_context_division_set_expression(
        self, target_timespan, voice_name):
        from experimental.tools import musicexpressiontools
        divisions = self.get_time_signature_slice(target_timespan)
        return musicexpressiontools.TimespanScopedSingleContextDivisionSetExpression(
            source_expression=musicexpressiontools.IterablePayloadExpression(divisions),
            target_timespan=target_timespan,
            target_context_name=voice_name,
            fresh=True,
            truncate=True,
            )

    def make_default_timespan_scoped_single_context_rhythm_set_expression(
        self, target_timespan, voice_name):
        from experimental import library
        from experimental.tools import musicexpressiontools
        return musicexpressiontools.TimespanScopedSingleContextRhythmSetExpression(
            source_expression=musicexpressiontools.RhythmMakerExpression(library.skip_tokens),
            target_timespan=target_timespan,
            target_context_name=voice_name,
            fresh=True,
            )

    def make_default_timespan_scoped_single_context_set_expression(
        self, attribute, target_timespan, voice_name):
        if attribute == 'divisions':
            return self.make_default_timespan_scoped_single_context_division_set_expression(
                target_timespan, voice_name)
        elif attribute == 'rhythm':
            return self.make_default_timespan_scoped_single_context_rhythm_set_expression(
                target_timespan, voice_name)
        else:
            raise ValueError(attribute)

    def make_timespan_scoped_single_context_set_expressions_for_voice(self, attribute, voice_name):
        from experimental.tools import musicexpressiontools
        timespan_scoped_set_expressions = \
            musicexpressiontools.TimespanScopedSingleContextSetExpressionInventory()
        for specification in (self, ) + tuple(self.segment_specifications):
            single_context_set_expressions = \
                specification.get_single_context_set_expressions_rooted_to_specification_that_govern_context_name(
                attribute, voice_name)
            #if attribute == 'divisions':
            #    self._debug(specification, 'spc')
            #    self._debug_values(single_context_set_expressions, 'SSS')
            for single_context_set_expression in single_context_set_expressions:
                timespan_scoped_set_expression = single_context_set_expression.evaluate()
                # make sure set expression was set expression for 
                # timespan that exists in current segment
                if timespan_scoped_set_expression.target_timespan.is_well_formed:
                    timespan_scoped_set_expressions.append(
                        timespan_scoped_set_expression)
        #self._debug_values(timespan_scoped_set_expressions, 'TTT')
        timespan_scoped_set_expressions.sort(self._compare_expressions)
        assert timespan_scoped_set_expressions.all_are_well_formed
        return timespan_scoped_set_expressions

    def report_settings(self):
        for segment_specification in self.segment_specifications:
            print '### {} ### '.format(segment_specification)
            for context_proxy_name, context_proxy in \
                segment_specification.single_context_set_expressions_by_context.items():
                printed_context_proxy_name = False
                for key, value in \
                    context_proxy.single_context_set_expressions_by_attribute.items():
                    if value:
                        if not printed_context_proxy_name:
                            print context_proxy_name
                            printed_context_proxy_name = True
                        print key, value.storage_format
            print ''
        print '### SCORE ###'
        print self
        for context_proxy_name, context_proxy in \
            self.single_context_set_expressions_by_context.items():
            printed_context_proxy_name = False
            for key, value in \
                context_proxy.single_context_set_expressions_by_attribute.items():
                if value:
                    if not printed_context_proxy_name:
                        print context_proxy_name
                        printed_context_proxy_name = True
                    print key, value.storage_format
        print ''
        print '### SCORE-ROOTED ###'
        for context_proxy_name, context_proxy in \
            self.single_context_set_expressions_by_context.items():
            printed_context_proxy_name = False
            for key, value in \
                context_proxy.single_context_set_expressions_by_attribute.items():
                if value:
                    if not printed_context_proxy_name:
                        print context_proxy_name
                        printed_context_proxy_name = True
                    print key, value.storage_format
