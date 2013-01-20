import abc
import copy
#from experimental.tools.settingtools.AnchoredObject import AnchoredObject
from abjad.tools.abctools import AbjadObject


#class Expression(AnchoredObject):
class Expression(AbjadObject):
    '''Expression base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _anchor_abbreviation(self):
        '''Form of expression suitable for inclusion in storage format.
        '''
        return self

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _evaluate(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Expression start offset.

        Return offset expression.
        '''
        from experimental.tools import settingtools
        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation)
        result._score_specification = self.score_specification
        return result

    @property
    def stop_offset(self):
        '''Expression stop offset.

        Return offset expression.
        '''
        from experimental.tools import settingtools
        result = settingtools.OffsetExpression(anchor=self._anchor_abbreviation, edge=Right)
        result._score_specification = self.score_specification
        return result
