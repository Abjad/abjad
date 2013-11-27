# -*- encoding: utf-8 -*-
import abc
from abjad.tools import *
from abjad.tools.topleveltools import iterate
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.musicexpressiontools.AttributeNameEnumeration \
    import AttributeNameEnumeration


class Specification(AbjadObject):
    r'''Specification.

    Specification properties are immutable.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_template):
        from experimental.tools import musicexpressiontools
        self._context_name_abbreviations = []
        self._context_names = []
        self._fresh_single_context_set_expressions = \
            timespantools.TimespanInventory()
        self._score_template = score_template
        self._score_model = score_template()
        self._single_context_set_expressions_by_context = \
            musicexpressiontools.ContextDictionary(score_template())
        self._initialize_context_name_abbreviations()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats specification.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PRIVATE PROPERTIES ###

    def _context_name_to_improper_parentage_names(self, context_name):
        context = self.score_model[context_name]
        parentage = context._get_parentage(include_self=True)
        parentage_names = [parent.name for parent in parentage]
        return parentage_names

    def _get_first_expression_that_governs_context_name(
        self, expressions, context_name):
        parentage_names = \
            self._context_name_to_improper_parentage_names(context_name)
        for parentage_name in parentage_names:
            for expression in expressions:
                if expression.scope_name is None:
                    return expression
                elif expression.scope_name == parentage_name:
                    return expression

    ### PRIVATE METHODS ###

    def _context_token_to_context_names(self, context_token):
        if context_token is None:
            context_names = None
        elif context_token == [self.score_name]:
            context_names = context_token
        elif isinstance(context_token, type(self)):
            context_names = [context_token.score_name]
        elif context_token in self.context_names:
            context_names = [context_token]
        elif context_token in self.context_name_abbreviations:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all(
            x in self.context_name_abbreviations for x in context_token):
            context_names = context_token
        elif isinstance(context_token, (tuple, list)) and all(
            x in self.context_names for x in context_token):
            context_names = context_token
        elif isinstance(context_token, scoretools.Context):
            context_names = [context_token.name]
        elif indicatortools.all_are_contexts(context_token):
            context_names = [context.name for context in context_token]
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names

    def _initialize_context_name_abbreviations(self):
        context_name_abbreviations = getattr(
            self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in \
            context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
            self._context_name_abbreviations.append(context_name)
        score = self.score_template()
        self._score_name = score.name
        for context in iterate(score).by_class(scoretools.Context):
            if hasattr(context, 'name'):
                self._context_names.append(context.name)
        self._context_names = tuple(self._context_names)

    ### PUBLIC PROPERTIES ###

    @property
    def context_name_abbreviations(self):
        r'''Specification context name abbreviations.

        Returns tuple.
        '''
        return self._context_name_abbreviations

    @property
    def context_names(self):
        r'''Specification context names.

        Returns tuple.
        '''
        return self._context_names

    @property
    def fresh_single_context_set_expressions(self):
        r'''Specification fresh single-context set expressions.

        Returns timespan inventory.
        '''
        return self._fresh_single_context_set_expressions

    @property
    def score_model(self):
        r'''Specification score model.

        Returns score.
        '''
        return self._score_model

    @property
    def score_name(self):
        r'''Specification score name.

        Returns string or none.
        '''
        return self._score_name

    @property
    def score_template(self):
        r'''Specification score template.

        Returns score template.
        '''
        return self._score_template

    @property
    def single_context_set_expressions_by_context(self):
        r'''Specification single-context set expressions by context.

        Returns context dictionary.
        '''
        return self._single_context_set_expressions_by_context

    @property
    def timespan(self):
        r'''Specification timespan.

        Returns timespan.
        '''
        return self._timespan

    ### PUBLIC METHODS ###

    def compare_context_names(self, x, y):
        r'''Compare context names.

        Root context sorts first and voice contexts sort last.

            >>> template = \
            ...     templatetools.GroupedRhythmicStavesScoreTemplate(
            ...     staff_count=2)
            >>> score_specification = \
            ...     musicexpressiontools.ScoreSpecificationInterface(template)
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

        Returns -1, 0 or 1.
        '''
        x_depth = self.context_name_to_depth(x)
        y_depth = self.context_name_to_depth(y)
        return cmp(x_depth, y_depth)

    def context_name_to_depth(self, context_name):
        r'''Context name to context depth.

        Score context evaluates to ``0``.
        Nonscore contexts evaluate to greater than ``0``.

            >>> template = \
            ...     templatetools.GroupedRhythmicStavesScoreTemplate(
            ...     staff_count=2)
            >>> score_specification = \
            ...     musicexpressiontools.ScoreSpecificationInterface(
            ...     template)
            >>> score_specification = score_specification.specification

        ::

            >>> score_specification.context_name_to_depth(None)
            0

        ::

            >>> score_specification.context_name_to_depth(
            ...     'Grouped Rhythmic Staves Score')
            0

        ::

            >>> score_specification.context_name_to_depth(
            ...     'Grouped Rhythmic Staves Staff Group')
            1

        ::

            >>> score_specification.context_name_to_depth('Staff 1')
            2

        ::

            >>> score_specification.context_name_to_depth('Voice 1')
            3

        Returns nonzero integer.
        '''
        assert isinstance(context_name, (str, type(None)))
        if context_name is None:
            return 0
        elif context_name == self.score_model.name:
            return 0
        else:
            context = self.score_model[context_name]
            return context._get_parentage().depth

    def get_single_context_set_expressions_rooted_to_specification_that_govern_context_name(
        self, attribute, context_name):
        r'''Get single-context set expressions rooted to specification 
        that govern `context_name`.

        Returns list such that highest level (most general) context 
        set expressions appear first.

        Lowest level (most specific) context set expressions appear last.
        '''
        result = []
        context_names = \
            self._context_name_to_improper_parentage_names(context_name)
        for context_name in reversed(context_names):
            context_proxy = \
                self.single_context_set_expressions_by_context[context_name]
            expressions = \
                context_proxy.single_context_set_expressions_by_attribute.get(
                    attribute, [])
            result.extend(expressions)
        return result
