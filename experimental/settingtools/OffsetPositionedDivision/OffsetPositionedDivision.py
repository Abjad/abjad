import copy
from abjad.tools import durationtools
from experimental import divisiontools
from experimental.settingtools.OffsetPositionedExpression import OffsetPositionedExpression


class OffsetPositionedDivision(OffsetPositionedExpression):
    r'''.. versionadded:: 1.0

    Offset-positioned division.

    Composers do not create offset-positioned divisions
    because divisions arise as a byproduct of interpretation. 
    '''

    ### INITIALIZER ###

    def __init__(self, division, voice_name=None, start_offset=None, stop_offset=None):
        OffsetPositionedExpression.__init__(
            self, voice_name, start_offset=start_offset, stop_offset=stop_offset)
        division = divisiontools.Division(division)
        self._division = divisions

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division(self):
        '''Offset-positioned division payload.

        Return division.
        '''
        return self._division 

    @property
    def duration(self):
        '''Duration of offset-positioned division.
        
        Return duration.
        '''
        return self.division.duration
