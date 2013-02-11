import abc
from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import expressiontools


class Specification(AbjadObject):
    r'''Specification.

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
        self._fresh_single_context_set_expressions = timespantools.TimespanInventory()
        self._multiple_context_set_expressions = timespantools.TimespanInventory()
        self._score_template = score_template
        self._score_model = score_template()
        self._single_context_set_expressions_by_context = \
            specificationtools.ContextDictionary(score_template())
        self._initialize_context_name_abbreviations()

    ### READ-ONLY PRIVATE PROPERTIES ###

    def _context_name_to_improper_parentage_names(self, context_name):
        context = componenttools.get_first_component_in_expr_with_name(self.score_model, context_name)
        parentage = componenttools.get_improper_parentage_of_component(context)
        parentage_names = [parent.name for parent in parentage]
        return parentage_names

    def _get_first_expression_that_governs_context_name(self, expressions, context_name):
        parentage_names = self._context_name_to_improper_parentage_names(context_name)
        for parentage_name in parentage_names:
            for expression in expressions:
                if expression.target_context_name is None:
                    return expression
                elif expression.target_context_name == parentage_name:
                    return expression

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
        '''Specification context names.

        Return list.
        '''
        return self._context_names

    @property
    def fresh_single_context_set_expressions(self):
        '''Specification fresh single-context set expressions.

        Return timespan inventory.
        '''
        return self._fresh_single_context_set_expressions

    @property
    def multiple_context_set_expressions(self):
        '''Specification multiple-context set expressions.

        Return timespan inventory.
        '''
        return self._multiple_context_set_expressions

    @property
    def score_model(self):
        '''Specification score model.

        Return score.
        '''
        return self._score_model

    @property
    def score_name(self):
        '''Specification score name.

        Return string or none.
        '''
        return self._score_name

    @property
    def score_template(self):
        '''Specification score template.

        Return score template.
        '''
        return self._score_template

    @property
    def single_context_set_expressions_by_context(self):
        '''Specification single-context set expressions by context.

        Return context dictionary.
        '''
        return self._single_context_set_expressions_by_context

    @property
    def timespan(self):
        '''Specification timespan.

        Return timespan.
        '''
        return self._timespan

    ### PUBLIC METHODS ###

    def compare_context_names(self, x, y):
        '''Compare context names.

        Root context sorts first and voice contexts sort last.

            >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
            >>> score_specification = specificationtools.ScoreSpecificationInterface(template)
            >>> score_specification = score_specification.specification

        ::

            >>> score_specification.compare_context_names(None, 'Voice 1')
            -1
            
        ::

            >>> score_specification.compare_context_names('Voice 1', None)
            1
            
        ::

            >>> score_specification.compare_context_names('Voice 1', 'Voice 1')
            0 

        Return -1, 0 or 1.
        '''
        x_depth = self.context_name_to_depth(x)
        y_depth = self.context_name_to_depth(y)
        return cmp(x_depth, y_depth)

    def context_name_to_depth(self, context_name):
        '''Context name to context depth.

        Score context evaluates to ``0``.
        Nonscore contexts evaluate to greater than ``0``.
        
            >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
            >>> score_specification = specificationtools.ScoreSpecificationInterface(template)
            >>> score_specification = score_specification.specification

        ::

            >>> score_specification.context_name_to_depth(None)
            0

        ::

            >>> score_specification.context_name_to_depth('Grouped Rhythmic Staves Score')
            0

        ::

            >>> score_specification.context_name_to_depth('Grouped Rhythmic Staves Staff Group')
            1

        ::

            >>> score_specification.context_name_to_depth('Staff 1')
            2

        ::

            >>> score_specification.context_name_to_depth('Voice 1')
            3

        Return nonzero integer.
        '''
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        if context_name is None:
            return 0
        elif context_name == self.score_model.name:
            return 0
        else:
            context = self.score_model[context_name]
            return context.parentage.depth

    def get_single_context_set_expressions_rooted_to_specification_that_govern_context_name(
        self, attribute, context_name):
        '''Get single-context set expressions rooted to specification that govern `context_name`.

        Return list such that highest level (most general) context set expressions appear first.

        Lowest level (most specific) context set expressions appear last.
        '''
        result = []
        context_names = self._context_name_to_improper_parentage_names(context_name)
        for context_name in reversed(context_names):
            context_proxy = self.single_context_set_expressions_by_context[context_name]
            expressions = context_proxy.single_context_set_expressions_by_attribute.get(attribute, [])
            result.extend(expressions)
        return result
