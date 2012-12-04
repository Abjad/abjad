import abc
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools
from experimental import requesttools
from experimental import selectortools
from experimental import settingtools


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

    def _return_ratio_part_selectors(self, selector, ratio, is_count=True):
        result = []
        for part in range(len(ratio)):
            result.append(self._wrap_selector_with_ratio_part_selector(
                selector, ratio, part, is_count=is_count))
        return tuple(result)

    def _wrap_selector_with_ratio_part_selector(self, selector, ratio, part, is_count=True):
        if is_count:
            return selectortools.CountRatioPartTimespanSelector(selector, ratio, part)
        else:
            return selectortools.TimeRatioPartTimespanSelector(selector, ratio, part)

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
                selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    ),
                context_name='Voice 1'
                )

        Return material request.        
        '''
        timespan = timespan or self.select_segment_timespan()
        #time_relation = time_relation or timerelationtools.timespan_2_starts_during_timespan_1()
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
                selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    ),
                context_name='Voice 1'
                )

        Return material request.        
        '''
        timespan = timespan or self.select_segment_timespan()
        #time_relation = time_relation or timerelationtools.timespan_2_starts_during_timespan_1()
        return requesttools.MaterialRequest(
            'naive_beats', timespan, time_relation=time_relation, context_name=context, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    # TODO: could this be done with a TimeRatioPartTimespanSelector instead?
    def request_partitioned_time(self, ratio, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment partitioned total time according to `ratio`.

        .. note:: add example.

        Return material request.
        '''
        timespan = timespan or self.select_segment_timespan()
        #time_relation = time_relation or timerelationtools.timespan_2_starts_during_timespan_1()
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
                selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    ),
                context_name='Voice 1'
                )

        Return rhythm request.        
        '''
        timespan = timespan or self.select_segment_timespan()
        #time_relation = time_relation or timerelationtools.timespan_2_starts_during_timespan_1()
        #if timespan.time_relation is not None:
        #    time_relation = timerelationtools.timespan_2_starts_during_timespan_1()
        return requesttools.MaterialRequest(
            'rhythm', timespan, time_relation=time_relation, context_name=voice, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def request_time_signatures(self, context=None, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment time signatures in `context`::

            >>> request = red_segment.request_time_signatures()

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'time_signatures',
                selectortools.SingleSegmentTimespanSelector(
                    identifier='red'
                    )
                )

        Return material request.
        '''
        timespan = timespan or self.select_segment_timespan()
        #time_relation = time_relation or timerelationtools.timespan_2_starts_during_timespan_1()
        return requesttools.MaterialRequest(
            'time_signatures', timespan, time_relation=time_relation, context_name=context, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
