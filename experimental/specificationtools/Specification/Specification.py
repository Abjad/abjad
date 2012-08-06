from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools
from experimental import settingtools


class Specification(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete specification classes inherit.

    Score and segment specifications constitute the primary vehicle of composition.

    Composers make settings against score and segment specifications.

    Interpreter code interprets score and segment specifications.

    Abjad score object results from interpretation.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, score_template):
        from experimental import specificationtools
        self._score_template = score_template
        self._context_names = []
        self._resolved_single_context_settings = specificationtools.ContextProxyDictionary(self.score_template())
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
        elif context_token in self.context_names:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all([x in self.context_names for x in context_token]):
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
            self._context_names.append(context_name)
        score = self.score_template()
        self._score_name = score.name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        return self._context_names

    @property
    def contexts(self):
        return self._contexts

    @property
    def resolved_single_context_settings(self):
        return self._resolved_single_context_settings

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def single_context_settings(self):
        return self._single_context_settings
