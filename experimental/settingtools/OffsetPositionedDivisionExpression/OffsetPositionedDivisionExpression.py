from experimental import divisiontools
from experimental.settingtools.OffsetPositionedExpression import OffsetPositionedExpression


class OffsetPositionedDivisionExpression(OffsetPositionedExpression):
    r'''.. versionadded:: 1.0

    Offset-positioned division expression.

    Composers do not create offset-positioned division expressions
    because division expression arise as a byproduct of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, division_list, voice_name=None, start_offset=None, stop_offset=None):
        OffsetPositionedExpression.__init__(
            self, voice_name, start_offset=start_offset, stop_offset=stop_offset)
        division_list = divisiontools.DivisionList(division_list)
        self._division_list = division_list

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        '''Offset-positioned division expression division list.

        Return division list object.
        '''
        return self._division_list

    @property
    def divisions(self):
        '''Offset-positioned division expression division list divisions.

        Delegate to ``self.division_list.divisions``.

        Return list.
        '''
        return self.division_list.divisions

    @property
    def duration(self):
        '''Duration of division expression.
        
        Return duration.
        '''
        return self.division_list.duration
