import abc
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import expressiontools


class Specification(AbjadObject):
    r'''Specification.

    Abstract base class from which score specification and 
    segment specification classes inherit.

    Interpreter interprets score and segment specifications.

    Abjad score object results from interpretation.

    Specification properties are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = expressiontools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_template):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        self._abbreviated_context_names = []
        self._context_names = []
        self._context_proxies = specificationtools.ContextProxyDictionary(score_template())
        # TODO: maybe remove in favor of self.context_proxies[].single_context_set_expression_attribute_dict?
        self._fresh_single_context_set_expressions_by_attribute = \
            expressiontools.SingleContextSetExpressionAttributeDictionary()
        self._multiple_context_set_expressions = expressiontools.SetExpressionInventory()
        self._score_template = score_template
        self._score_model = score_template()
        self._initialize_context_name_abbreviations()

    ### READ-ONLY PRIVATE PROPERTIES ###

    def _context_name_to_improper_parentage_names(self, context_name):
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        parentage = componenttools.get_improper_parentage_of_component(context)
        context_names = [context.name for context in parentage]
        return context_names

    def _get_first_element_in_expr_by_parentage(self, expr, context_name):
        context_names = self._context_name_to_improper_parentage_names(context_name)
        for context_name in context_names:
            for element in expr:
                if element.target_context_name is None:
                    return element
                if element.target_context_name == context_name:
                    return element

    ### PRIVATE METHODS ###

    def _context_token_to_context_names(self, context_token):
        if context_token is None:
            context_names = None
        elif context_token == [self.score_name]:
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = [context_token.score_name]
        elif context_token in self._abbreviated_context_names:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all([
            x in self._abbreviated_context_names for x in context_token]):
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
    def context_names(self):
        return self._context_names

    @property
    def context_proxies(self):
        return self._context_proxies

    @property
    def fresh_single_context_set_expressions_by_attribute(self):
        return self._fresh_single_context_set_expressions_by_attribute

    @property
    def multiple_context_set_expressions(self):
        return self._multiple_context_set_expressions

    @property
    def score_model(self):
        return self._score_model

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def timespan(self):
        return self._timespan
