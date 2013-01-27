import abc
import copy
from experimental.tools.expressiontools.SetExpression import SetExpression


class SingleContextSetExpression(SetExpression):
    r'''Single-context set-expression.

    Set `attribute` to `expression` for single-context `anchor`::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> multiple_context_set_expression = red_segment.set_time_signatures([(4, 8), (3, 8)])

    ::

        >>> contexts = ['Voice 1', 'Voice 3']
        >>> multiple_context_set_expression = red_segment.set_divisions([(3, 16)], contexts=contexts)

    ::

        >>> score = score_specification.interpret()

    ::

        >>> single_context_set_expression = score_specification.single_context_set_expressions[1]

    ::

        >>> z(single_context_set_expression)
        expressiontools.SingleContextSetDivisionExpression(
            expression=expressiontools.PayloadExpression(
                ((3, 16),)
                ),
            anchor='red',
            context_name='Voice 1',
            fresh=True,
            persist=True
            )

    Composer set() methods product multiple-context set-expressions.

    Multiple-context set-expressions produce single-context settings.

    Single-context set-expressions produce region commands.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, attribute=None, expression=None, anchor=None, context_name=None, 
        fresh=True, persist=True, truncate=None):
        SetExpression.__init__(self, attribute=attribute, expression=expression, anchor=anchor, 
            fresh=fresh, persist=persist, truncate=truncate)
        assert isinstance(context_name, (str, type(None)))
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Single-context set-expression context name.

        Return string or none.
        '''
        return self._context_name

    @property
    def storage_format(self):
        '''Single-context set-expression storage format::

            >>> z(single_context_set_expression)
            expressiontools.SingleContextSetDivisionExpression(
                expression=expressiontools.PayloadExpression(
                    ((3, 16),)
                    ),
                anchor='red',
                context_name='Voice 1',
                fresh=True,
                persist=True
                )

        Return string.
        '''
        return SetExpression.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def copy_setting_to_segment_name(self, segment_name):
        '''Create new set expression. 

        Set new set expression start segment identifier to `segment_name`.

        Set new set expression `fresh` to false.

        Return new set expression.
        '''
        assert isinstance(segment_name, str)
        new_setting = copy.deepcopy(self)
        new_setting._set_start_segment_identifier(segment_name)
        new_setting._fresh = False
        return new_setting

    def evaluate(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_timespan_scoped_setting(self):
        '''Evaluate timespan of single-context setting.

        Return timespan-scoped single-context setting.
        '''
        pass
