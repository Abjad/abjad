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

    @abc.abstractproperty
    def timespan(self):
        pass
    
    ### PUBLIC METHODS ###

    def request_divisions(self, voice, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment divisions in `voice`::

            >>> request = red_segment.request_divisions('Voice 1')

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'divisions',
                'Voice 1',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )

        Return material request.        
        '''
        timespan = timespan or self.timespan
        return requesttools.MaterialRequest(
            'divisions', voice, timespan, time_relation=time_relation,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def request_naive_beats(self, voice, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment naive beats in `voice`::

            >>> request = red_segment.request_naive_beats('Voice 1')

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'naive_beats',
                'Voice 1',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )

        Return material request.        
        '''
        assert isinstance(voice, str)
        timespan = timespan or self.timespan
        return requesttools.MaterialRequest(
            'naive_beats', voice, timespan, time_relation=time_relation,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    # TODO: could this be done with self.timespan.divide_by_ratio() instead?
    def request_partitioned_time(self, ratio, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request segment partitioned total time according to `ratio`.

        .. note:: add example.

        Return material request.
        '''
        timespan = timespan or self.timespan
        request = requesttools.MaterialRequest(
            'partitioned_time', None, timespan, time_relation=time_relation,
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
                'Voice 1',
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    ),
                start_segment_name='red'
                )

        Return rhythm request.        
        '''
        timespan = timespan or self.timespan
        return requesttools.MaterialRequest(
            'rhythm', voice, timespan, start_segment_name=getattr(self, 'segment_name', None),
            time_relation=time_relation, 
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def request_time_signatures(self, voice=None, timespan=None, time_relation=None,
        index=None, count=None, reverse=None, rotation=None, callback=None):
        r'''Request `voice` time signatures that start during segment ``'red'``::

            >>> request = red_segment.request_time_signatures()

        ::

            >>> z(request)
            requesttools.MaterialRequest(
                'time_signatures',
                None,
                symbolictimetools.SingleSegmentSymbolicTimespan(
                    identifier='red'
                    )
                )

        Return material request.
        '''
        assert voice is None
        timespan = timespan or self.timespan
        return requesttools.MaterialRequest(
            'time_signatures', voice, timespan, time_relation=time_relation,
            index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)

    def select_background_measures(self, start=None, stop=None, time_relation=None):
        '''Select the first five background measures that start during segment 'red'::

            >>> timespan = red_segment.select_background_measures(stop=5)

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

    def select_divisions(self, start=None, stop=None, time_relation=None, voice=None):
        '''Select the first five divisions that start during segment 'red'::

            >>> timespan = red_segment.select_divisions(stop=5)

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

    def select_leaves(self, start=None, stop=None, time_relation=None, voice=None):
        '''Select the first ``40`` voice ``1`` leaves that start during segment ``'red'``::

            >>> timespan = red_segment.select_leaves(voice='Voice 1', stop=40)

        ::

            >>> z(timespan)
            symbolictimetools.CounttimeComponentSymbolicTimespan(
                anchor='red',
                klass=leaftools.Leaf,
                stop_identifier=40,
                voice_name='Voice 1'
                )

        Return timespan.
        '''
        assert isinstance(voice, (str, type(None)))
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
        selector = self.timespan
        return symbolictimetools.OffsetSymbolicTimespan(selector, start_offset=start, stop_offset=stop)
