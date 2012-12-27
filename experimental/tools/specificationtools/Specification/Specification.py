import abc
import numbers
from abjad.tools import *
from experimental.tools import helpertools
from experimental.tools import requesttools
from experimental.tools import settingtools
from experimental.tools import symbolictimetools
from experimental.tools.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class Specification(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

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
    def __init__(self, score_specification, score_template):
        from experimental.tools import specificationtools
        SymbolicTimespan.__init__(self)
        self._score_specification = score_specification
        self._score_template = score_template
        self._score_model = score_template()
        self._abbreviated_context_names = []
        self._context_names = []
        self._multiple_context_settings = settingtools.MultipleContextSettingInventory()
        self._single_context_settings_by_context = specificationtools.ContextProxyDictionary(score_template())
        self._initialize_context_name_abbreviations()
        self._contexts = specificationtools.ContextProxyDictionary(score_template())
        self._single_context_settings = settingtools.SingleContextSettingInventory()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _timespan_abbreviation(self):
        '''Form of symbolic timespan suitable for writing to disk.
        
        Specifications alias this property to specification name.
        '''
        return self.specification_name

    ### PRIVATE METHODS ###

    # TODO: this can be removed once Specification no longer inherits from SymbolicTimespan
    def __deepcopy__(self, memo):
        # voice indication is a hack
        return self.select('Voice 1')

    def _context_token_to_context_names(self, context_token):
        if context_token is None:
            #context_names = [self.score_name] 
            context_names = None
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
    def multiple_context_settings(self):
        '''Secification multiple-context settings.

        Return multiple-context setting inventory.
        '''
        return self._multiple_context_settings

    @property
    def score_model(self):
        '''Secification score model.

        Return Abjad score object.
        '''
        return self._score_model

    @property
    def score_name(self):
        return self._score_name

    @abc.abstractproperty
    def score_specification(self):
        pass

    @property
    def score_template(self):
        return self._score_template

    @property
    def single_context_settings(self):
        return self._single_context_settings

    @property
    def single_context_settings_by_context(self):
        return self._single_context_settings_by_context

    @property
    def start_offset(self):
        from experimental.tools import symbolictimetools
        return symbolictimetools.SymbolicOffset(anchor=self._timespan_abbreviation)

    @property
    def stop_offset(self):
        from experimental.tools import symbolictimetools
        return symbolictimetools.SymbolicOffset(anchor=self._timespan_abbreviation, edge=Right)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def select(self):
        pass
