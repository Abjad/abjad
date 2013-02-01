import abc
import copy
from experimental.tools.expressiontools.InputSetExpression import InputSetExpression


class SingleContextSetExpression(InputSetExpression):
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
        ...     score_specification.specification.fresh_single_context_set_expressions_by_attribute[
        ...     'divisions'][0]

    ::

        >>> z(fresh_single_context_set_expression)
        expressiontools.SingleContextDivisionSetExpression(
            source=expressiontools.PayloadExpression(
                ((3, 16),)
                ),
            target_timespan='red',
            target_context_name='Voice 1',
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
        InputSetExpression.__init__(self, attribute=attribute, source=source, 
            target_timespan=target_timespan, fresh=fresh, persist=persist, truncate=truncate)
        assert isinstance(target_context_name, (str, type(None)))
        self._target_context_name = target_context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Single-context set expression storage format::

            >>> z(fresh_single_context_set_expression)
            expressiontools.SingleContextDivisionSetExpression(
                source=expressiontools.PayloadExpression(
                    ((3, 16),)
                    ),
                target_timespan='red',
                target_context_name='Voice 1',
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

    def store_by_segment_context_and_attribute(self, clear_persistent_first=False):
        '''Copy single-context set expression.

        Find single-context set expression root segment specification.

        Find single-context set expression target context.
        
        Find single-context set expression attribute.

        Store copied single-context set expression first by segment,
        then by context and finally by attribute.

        If set expression persists then also store reference to 
        single-context set expression in score specification
        first by context and then by attribute.
        '''
        # TODO: maybe able to remove deepcopy?
        single_context_set_expression = copy.deepcopy(self)
        root_segment_specification = single_context_set_expression.root_segment_specification
        # TODO: this will have to be extended to handle score-rooted expressions
        assert root_segment_specification is not None
        target_context_name = single_context_set_expression.target_context_name
        if target_context_name is None:
            target_context_name = root_segment_specification.context_proxies.score_name
        attribute = single_context_set_expression.attribute
        if clear_persistent_first:
            self.score_specification.clear_persistent_single_context_set_expressions_by_context(
                attribute, target_context_name)
        root_segment_specification.context_proxies[
            target_context_name].single_context_set_expressions_by_attribute[attribute].append(
            single_context_set_expression)
        if single_context_set_expression.persist:
            self.score_specification.context_proxies[
                target_context_name].single_context_set_expressions_by_attribute[attribute].append(
                single_context_set_expression)
