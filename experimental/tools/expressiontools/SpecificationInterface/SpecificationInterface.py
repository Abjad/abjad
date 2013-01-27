import abc
from experimental.tools.expressiontools.SetMethodMixin import SetMethodMixin
from experimental.tools.expressiontools.SelectMethodMixin import SelectMethodMixin


class SpecificationInterface(SelectMethodMixin, SetMethodMixin):
    r'''InputSetExpression interface.

    Score and segment set expression interfaces constitute the primary vehicle of composition.

    Composers make set expressions against score and segment set expression interfaces.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_specification):
        self._score_specification = score_specification

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}()'.format(self._class_name)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _expression_abbreviation(self):
        return self.specification_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        '''Read-only reference to score against which segment specification is defined.

        Return score specification.
        '''
        return self._score_specification

    @property
    def specification_name(self):
        return

    @property
    def timespan(self):
        from experimental.tools import expressiontools
        timespan = expressiontools.TimespanExpression()
        timespan._score_specification = self.score_specification
        return timespan
