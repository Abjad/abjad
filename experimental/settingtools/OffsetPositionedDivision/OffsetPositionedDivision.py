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
        self._division = division

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

    ### PUBLIC METHODS ###

    def trim_to_start_offset(self, start_offset):
        '''Trim payload to start offset.

        Adjust wrapper start offset.

        Operate in place and return none.
        '''
        
        start_offset = durationtools.Offset(start_offset)
        assert self.start_offset <= start_offset
        duration_to_trim = start_offset - self.start_offset
        division = self.division - duration_to_trim
        self._division = division
        self._start_offset = start_offset

    def trim_to_stop_offset(self, stop_offset):
        '''Trim payload to stop offset.

        Adjust wrapper stop offset.

        Operate in place and return none.
        '''
        
        stop_offset = durationtools.Offset(stop_offset)
        assert stop_offset <= self.stop_offset
        duration_to_trim = self.stop_offset - stop_offset
        division = self.division - duration_to_trim
        self._divison = division
