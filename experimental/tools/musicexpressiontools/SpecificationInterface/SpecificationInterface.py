# -*- encoding: utf-8 -*-
import abc
from experimental.tools.musicexpressiontools.TimeContiguousSetMethodMixin \
    import TimeContiguousSetMethodMixin
from experimental.tools.musicexpressiontools.SelectMethodMixin \
    import SelectMethodMixin


class SpecificationInterface(SelectMethodMixin, TimeContiguousSetMethodMixin):
    r'''Specification interface.

    Score and segment specification interfaces constitute the 
    primary vehicle of composition.

    Composers call many methods against score and segment specification 
    interfaces.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, score_specification):
        self._score_specification = score_specification

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _expression_abbreviation(self):
        return self.specification_name

    ### PUBLIC PROPERTIES ###

    @property
    def score_specification(self):
        r'''Read-only reference to score against which segment 
        specification is defined.

        Return score specification.
        '''
        return self._score_specification

    @abc.abstractproperty
    def specification(self):
        r'''Specification interface specification.

        Return specification.
        '''
        return self._specification

    @property
    def specification_name(self):
        return

    @property
    def timespan(self):
        from experimental.tools import musicexpressiontools
        timespan = musicexpressiontools.TimespanExpression()
        timespan._score_specification = self.score_specification
        return timespan
