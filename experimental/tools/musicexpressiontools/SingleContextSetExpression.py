# -*- encoding: utf-8 -*-
import abc
import copy
from experimental.tools.musicexpressiontools.TimeContiguousAnchoredSetExpression \
    import TimeContiguousAnchoredSetExpression


class SingleContextSetExpression(TimeContiguousAnchoredSetExpression):
    r'''Single-context set expression.

    Set `attribute` to `source_expression` for `target_timespan` in 
    `scope_name`.

    Example specification:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=4)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = \
        ...     red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> contexts = ['Voice 1', 'Voice 3']
        >>> multiple_context_set_expression = \
        ...     red_segment.set_divisions([(3, 16)], contexts=contexts)

    ::

        >>> score = score_specification.interpret()

    Example. Set time signatures to ``4/8``, ``3/8`` for red segment timespan 
    in score context:

    ::

        >>> fresh_single_context_set_expression = \
        ...     red_segment.specification.fresh_single_context_set_expressions[0]

    ::

        >>> print format(fresh_single_context_set_expression)
        musicexpressiontools.SingleContextTimeSignatureSetExpression(
            source_expression=musicexpressiontools.IterablePayloadExpression(
                payload=(
                    (4, 8),
                    (3, 8),
                    ),
                ),
            target_timespan='red',
            fresh=True,
            persist=True,
            )

    Set methods produce multiple-context set expressions.

    Multiple-context set expressions produce single-context set expressions.

    Single-context set expressions produce region expressions.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        attribute=None,
        source_expression=None,
        target_timespan=None,
        scope_name=None,
        fresh=True,
        persist=True,
        truncate=None,
        ):
        TimeContiguousAnchoredSetExpression.__init__(
            self,
            attribute=attribute,
            source_expression=source_expression,
            target_timespan=target_timespan,
            persist=persist,
            truncate=truncate,
            )
        assert isinstance(scope_name, (str, type(None)))
        self._fresh = fresh
        self._scope_name = scope_name

    ### PRIVATE METHODS ###

    def _copy_and_set_root_specification(self, root):
        r'''Copy single-context set expression.

        Set copy root specification to `root`.

        Set copy `fresh` to false.

        Returns copy.
        '''
        assert isinstance(root, (str, type(None)))
        new_set_expression = copy.deepcopy(self)
        new_set_expression._set_root_specification(root)
        new_set_expression._fresh = False
        return new_set_expression

    ### PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        r'''Is true when single-context set expression results 
        from explicit composer input.
        Otherwise false.

        Returns boolean.
        '''
        return self._fresh

    @property
    def scope_name(self):
        r'''Single-context set expression context name.

        Returns string or none.
        '''
        return self._scope_name

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def evaluate(self):
        r'''Evaluate single-context set expression.

        Returns timespan-delimited single-context set expression.
        '''
        pass

    def store_in_root_specification_by_context_and_attribute(self):
        r'''Store single-context set expression in root specification 
        by context and attribute.
        '''
        scope_name = self.scope_name or \
            self.score_specification.score_name
        scope_proxy = \
            self.root_specification.single_context_set_expressions_by_context[
                scope_name]
        expressions = \
            scope_proxy.single_context_set_expressions_by_attribute[
                self.attribute]
        for expression in expressions[:]:
            if expression.target_timespan == self.target_timespan:
                expressions.remove(expression)
        expressions.append(self)
