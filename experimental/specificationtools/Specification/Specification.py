import abc
import numbers
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools
from experimental import requesttools
from experimental import settingtools
from experimental import symbolictimetools


class Specification(AbjadObject):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Abstract base class from which concrete specification classes inherit.

    Score and segment specifications constitute the primary vehicle of composition.

    Composers make settings against score and segment specifications.

    Interpreter code interprets score and segment specifications.

    Abjad score object results from interpretation.

    The examples below reference the following segment specification::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        
    ::
    
        >>> red_segment = score_specification.append_segment(name='red')

    ::
            
        >>> red_segment
        SegmentSpecification('red')

    Return specification instance.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_template):
        from experimental import specificationtools
        self._score_template = score_template
        self._abbreviated_context_names = []
        self._context_names = []
        self._single_context_settings_by_context = \
            specificationtools.ContextProxyDictionary(self.score_template())
        self._initialize_context_name_abbreviations()
        self._contexts = specificationtools.ContextProxyDictionary(self.score_template())
        self._single_context_settings = settingtools.SingleContextSettingInventory()

    ### PRIVATE METHODS ###

    def _context_token_to_context_names(self, context_token):
        if context_token is None:
            context_names = [self.score_name] 
        elif context_token == [self.score_name]:
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = [context_token.score_name]
        elif context_token in self.abbreviated_context_names:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all([
            x in self.abbreviated_context_names for x in context_token]):
            context_names = context_token
        elif isinstance(context_token, contexttools.Context):
            context_names = [context_token.name]
        elif contexttools.all_are_contexts(context_token):
            context_names = [context.name for context in context_token]
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names

    def _initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
            self._abbreviated_context_names.append(context_name)
        score = self.score_template()
        self._score_name = score.name
        for context in iterationtools.iterate_contexts_in_expr(score):
            if hasattr(context, 'name'):
                self._context_names.append(context.name)

    # TODO: externalize this as a package function; need to implement on Specification
    # TODO: could implement as a SymbolicTimespan method that returns new symbolic timespan
    def _return_ratio_part_selectors(self, selector, ratio, is_count=True):
        result = []
        for part in range(len(ratio)):
            result.append(self._wrap_selector_with_ratio_part_selector(
                selector, ratio, part, is_count=is_count))
        return tuple(result)

    # TODO: externalize this as a package function; need to implement on Specification
    # TODO: could implement as a SymbolicTimespan method that returns new symbolic timespan
    def _wrap_selector_with_ratio_part_selector(self, selector, ratio, part, is_count=True):
        if is_count:
            return symbolictimetools.CountRatioPartSymbolicTimespan(selector, ratio, part)
        else:
            return symbolictimetools.TimeRatioPartSymbolicTimespan(selector, ratio, part)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def abbreviated_context_names(self):
        return self._abbreviated_context_names

    @property
    def context_names(self):
        return self._context_names

    @property
    def contexts(self):
        return self._contexts

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def single_context_settings(self):
        return self._single_context_settings

    @property
    def single_context_settings_by_context(self):
        return self._single_context_settings_by_context

    ### PUBLIC METHODS ###

    def request_divisions(self, voice, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment divisions in `voice`::

            >>> request = red_segment.request_divisions('Voice 1')

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'divisions',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                context_name='Voice 1'
                )

        Return material request.        
        '''
        timespan = timespan or self.select_timespan()
        return requesttools.MaterialRequest(
            'divisions', timespan, time_relation=time_relation, context_name=voice, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def request_naive_beats(self, context=None, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment naive beats in `voice`::

            >>> request = red_segment.request_naive_beats('Voice 1')

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'naive_beats',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                context_name='Voice 1'
                )

        Return material request.        
        '''
        timespan = timespan or self.select_timespan()
        return requesttools.MaterialRequest(
            'naive_beats', timespan, time_relation=time_relation, context_name=context, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    # TODO: could this be done with a TimeRatioPartSymbolicTimespan instead?
    def request_partitioned_time(self, ratio, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment partitioned total time according to `ratio`.

        .. note:: add example.

        Return material request.
        '''
        timespan = timespan or self.select_timespan()
        request = requesttools.MaterialRequest(
            'partitioned_time', timespan, time_relation=time_relation, context_name=None, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        request.ratio = ratio
        return request

    def request_rhythm(self, voice, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment rhythm in `voice`::

            >>> request = red_segment.request_rhythm('Voice 1')

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'rhythm',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_segment_name='red',
                context_name='Voice 1'
                )

        Return rhythm request.        
        '''
        timespan = timespan or self.select_timespan()
        return requesttools.MaterialRequest(
            'rhythm', timespan, start_segment_name=getattr(self, 'segment_name', None),
            time_relation=time_relation, context_name=voice, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def request_time_signatures(self, context=None, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment time signatures in `context`::

            >>> request = red_segment.request_time_signatures()

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'time_signatures',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )

        Return material request.
        '''
        timespan = timespan or self.select_timespan()
        return requesttools.MaterialRequest(
            'time_signatures', timespan, time_relation=time_relation, context_name=context, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def select_background_measure_timespan(self, start=None, stop=None, time_relation=None):
        '''Select the first five background measures anchored that start during segment 'red'::

            >>> timespan = red_segment.select_background_measure_timespan(stop=5)

        ::

            >>> z(timespan)
            symbolictimetools.BackgroundMeasureSymbolicTimespan(
                anchor='red',
                stop_identifier=5
                )

        Return background measure symbolic timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        timespan = symbolictimetools.BackgroundMeasureSymbolicTimespan(
            anchor=self.specification_name,
            start_identifier=start, 
            stop_identifier=stop, 
            time_relation=time_relation)
        return timespan

    def select_division_timespan(self, start=None, stop=None, time_relation=None, voice=None):
        '''Select the first five divisions that start during segment 'red'::

            >>> timespan = red_segment.select_division_timespan(stop=5)

        ::
            
            >>> z(timespan)
            symbolictimetools.DivisionSymbolicTimespan(
                anchor='red',
                stop_identifier=5
                )

        Return timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        assert isinstance(time_relation, (timerelationtools.TimeRelation, type(None))), repr(time_relation)
        timespan = symbolictimetools.DivisionSymbolicTimespan(
            anchor=self.specification_name,
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice,
            time_relation=time_relation)
        return timespan

    # TODO: merge into self.select_timespan() and then remove
    def select_offsets(self, start=None, stop=None):
        r'''Select segment from ``1/8`` to ``3/8``::

            >>> selector = red_segment.select_offsets(start=(1, 8), stop=(3, 8))

        ::

            >>> z(selector)
            symbolictimetools.OffsetSymbolicTimespan(
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_offset=durationtools.Offset(1, 8),
                stop_offset=durationtools.Offset(3, 8)
                )

        Return selector.
        '''
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        selector = self.select_timespan()
        return symbolictimetools.OffsetSymbolicTimespan(selector, start_offset=start, stop_offset=stop)

    # TODO: externalize this as a package function; need to implement on Specification
    # TODO: could implement as a SymbolicTimespan method that returns new symbolic timespan
    def select_count_ratio_parts(self, selector, ratio):
        return self._return_ratio_part_selectors(selector, ratio, is_count=True)

    # TODO: externalize this as a package function; need to implement on Specification
    # TODO: could implement as a SymbolicTimespan method that returns new symbolic timespan
    def select_time_ratio_parts(self, selector, ratio):
        return self._return_ratio_part_selectors(selector, ratio, is_count=False)

    def select_ratio(self, ratio):
        r'''Select the first third of segment::

            >>> selector = red_segment.select_ratio((1, 1, 1))[0]

        ::

            >>> z(selector)
            symbolictimetools.TimeRatioPartSymbolicTimespan(
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        ratio = mathtools.Ratio(ratio)
        selector = self.select_timespan()
        return self._return_ratio_part_selectors(selector, ratio, is_count=False)

    def select_ratio_of_background_measures(self, ratio, is_count=True, time_relation=None):
        r'''Select ratio of background measures.
    
        Example 1. Select the first third of segment background measures 
        calculated according to count of segment background measures::

            >>> selector = red_segment.select_ratio_of_background_measures((1, 1, 1), is_count=True)[0]

        ::

            >>> z(selector)
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Example 2. Select the first third of segment background measures calculated
        according to duration of segment background measures::

            >>> selector = red_segment.select_ratio_of_background_measures((1, 1, 1), is_count=False)[0]

        ::

            >>> z(selector)
            symbolictimetools.TimeRatioPartSymbolicTimespan(
                symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Example 3. Return one selector per ratio part::

            >>> selectors = red_segment.select_ratio_of_background_measures((1, 1, 1), is_count=True)

        ::

            >>> z(selectors[0])
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        ::

            >>> z(selectors[1])
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                1
                )


        ::

            >>> z(selectors[2])
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                2
                )

        Return selector.
        '''
        ratio = mathtools.Ratio(ratio)
        selector = self.select_background_measure_timespan(time_relation=time_relation)
        return self._return_ratio_part_selectors(selector, ratio, is_count=is_count)

    def select_ratio_of_divisions(self, ratio, is_count=True, time_relation=None, voice=None):
        r'''Select the first third divisions that start during segment 'red'::

            >>> selector = red_segment.select_ratio_of_divisions((1, 1, 1))[0]

        ::

            >>> z(selector)
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.DivisionSymbolicTimespan(
                    anchor='red'
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        ratio = mathtools.Ratio(ratio)
        selector = self.select_division_timespan(time_relation=time_relation, voice=voice)
        return self._return_ratio_part_selectors(selector, ratio, is_count=is_count)

    def select_leaf_timespan(self, start=None, stop=None, time_relation=None, voice=None):
        '''Select the first ``40`` segment leaves::

            >>> timespan = red_segment.select_leaf_timespan(stop=40)

        ::

            >>> z(timespan)
            symbolictimetools.CounttimeComponentSymbolicTimespan(
                anchor='red',
                klass=leaftools.Leaf,
                stop_identifier=40
                )

        Return timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        timespan = symbolictimetools.CounttimeComponentSymbolicTimespan(
            anchor=self.specification_name,
            time_relation=time_relation, 
            klass=leaftools.Leaf, 
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice)
        return timespan

    def select_ratio_of_leaves(self, ratio, is_count=True, time_relation=None, voice=None):
        r'''Select the first third of segment leaves::

            >>> selector = red_segment.select_ratio_of_leaves((1, 1, 1))[0]

        ::

            >>> z(selector)
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.CounttimeComponentSymbolicTimespan(
                    anchor='red',
                    klass=leaftools.Leaf
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        ratio = mathtools.Ratio(ratio)
        selector = self.select_leaf_timespan(time_relation=time_relation, voice=voice)
        return self._return_ratio_part_selectors(selector, ratio, is_count=is_count)

    def select_note_and_chord_timespan(self, start=None, stop=None, time_relation=None, voice=None):
        '''Select the first ``40`` segment notes and chords::

            >>> timespan = red_segment.select_note_and_chord_timespan(stop=40)

        ::

            >>> z(timespan)
            symbolictimetools.CounttimeComponentSymbolicTimespan(
                anchor='red',
                klass=helpertools.KlassInventory([
                    notetools.Note,
                    chordtools.Chord
                    ]),
                stop_identifier=40
                )

        Return timespan.
        '''
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        timespan = symbolictimetools.CounttimeComponentSymbolicTimespan(
            anchor=self.specification_name,
            time_relation=time_relation, 
            klass=(notetools.Note, chordtools.Chord),
            start_identifier=start, 
            stop_identifier=stop, 
            voice_name=voice)
        return timespan

    def select_ratio_of_notes_and_chords(self, ratio, is_count=True, time_relation=None, voice=None):
        r'''Select the first third of segment notes and chords::

            >>> selector = red_segment.select_ratio_of_notes_and_chords((1, 1, 1))[0]

        ::

            >>> z(selector)
            symbolictimetools.CountRatioPartSymbolicTimespan(
                symbolictimetools.CounttimeComponentSymbolicTimespan(
                    anchor='red',
                    klass=helpertools.KlassInventory([
                        notetools.Note,
                        chordtools.Chord
                        ])
                    ),
                mathtools.Ratio(1, 1, 1),
                0
                )

        Return selector.
        '''
        ratio = mathtools.Ratio(ratio)
        selector = self.select_note_and_chord_timespan(time_relation=time_relation, voice=voice)
        return self._return_ratio_part_selectors(selector, ratio, is_count=is_count)

    @abc.abstractmethod
    def select_timespan(self):
        pass
