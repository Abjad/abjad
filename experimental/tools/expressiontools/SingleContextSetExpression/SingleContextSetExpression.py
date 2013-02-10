import abc
import copy
from experimental.tools.expressiontools.AnchoredSetExpression import AnchoredSetExpression


class SingleContextSetExpression(AnchoredSetExpression):
    r'''Single-context set expression.

    Set `attribute` to `source` for single-context `target_timespan`::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> contexts = ['Voice 1', 'Voice 3']
        >>> multiple_context_set_expression = red_segment.set_divisions([(3, 16)], contexts=contexts)

    ::

        >>> score = score_specification.interpret()

    ::

        >>> fresh_single_context_set_expression = \
        ...     red_segment.specification.fresh_single_context_set_expressions[0]

    ::

        >>> z(fresh_single_context_set_expression)
        expressiontools.SingleContextTimeSignatureSetExpression(
            source=expressiontools.PayloadExpression(
                ((4, 8), (3, 8))
                ),
            target_timespan='red',
            fresh=True,
            persist=True
            )

    Composers create multiple-context set expressions with set methods.

    Multiple-context set expressions produce single-context set expressions.

    Single-context set expressions produce region expressions.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, source=None, target_timespan=None, target_context_name=None, 
        fresh=True, persist=True, truncate=None):
        AnchoredSetExpression.__init__(self, attribute=attribute, source=source, 
            target_timespan=target_timespan, persist=persist, truncate=truncate)
        assert isinstance(target_context_name, (str, type(None)))
        self._fresh = fresh
        self._target_context_name = target_context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''True when single-context set expression results from explicit composer input.
        Otherwise false.

        Return boolean.
        '''
        return self._fresh

    @property
    def storage_format(self):
        '''Single-context set expression storage format::

            >>> z(fresh_single_context_set_expression)
            expressiontools.SingleContextTimeSignatureSetExpression(
                source=expressiontools.PayloadExpression(
                    ((4, 8), (3, 8))
                    ),
                target_timespan='red',
                fresh=True,
                persist=True
                )

        Return string.
        '''
        return InputSetExpression.storage_format.fget(self)

    @property
    def target_context_name(self):
        '''Single-context set expression context name.

        Return string or none.
        '''
        return self._target_context_name

    ### PUBLIC METHODS ###

    def copy_and_set_root(self, root):
        '''Copy single-context set expression.

        Set copy root to `root`.

        Set copy `fresh` to false.
        
        Return copy.
        '''
        assert isinstance(root, (str, type(None)))
        new_set_expression = copy.deepcopy(self)
        new_set_expression._set_root(root)
        new_set_expression._fresh = False
        return new_set_expression

    @abc.abstractmethod
    def evaluate(self):
        '''Evaluate single-context set expression.

        Return timespan-scoped single-context set expression.
        '''
        pass

    def store_in_root_specification_by_context_and_attribute(self):
        '''Store single-context set expression in root specification by context and attribute.
        '''
        target_context_name = self.target_context_name or self.score_specification.score_name
        target_context_proxy = \
            self.root_specification.single_context_set_expressions_by_context[target_context_name]
        expressions = target_context_proxy.single_context_set_expressions_by_attribute[self.attribute]
        for expression in expressions[:]:
            if expression.target_timespan == self.target_timespan:
                expressions.remove(expression)
        expressions.append(self)
