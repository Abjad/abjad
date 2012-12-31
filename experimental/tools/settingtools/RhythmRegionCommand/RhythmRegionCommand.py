import copy
from experimental.tools.settingtools.RegionCommand import RegionCommand


class RhythmRegionCommand(RegionCommand):
    r'''Rhythm command.

    RegionCommand indicating durated period of time over which a rhythm payload will apply.
    '''
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'rhythm'

    ### PUBLIC METHODS ###

    def can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if expr.fresh:
            return False
        if expr.request != self.request:
            return False
        return True
