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

    def prolongs_expr(self, expr):
        from experimental.tools import selectortools
        from experimental.tools import settingtools
        # check that current rhythm command bears a rhythm material request
        current_material_request = self.request
        assert isinstance(current_material_request, selectortools.CounttimeComponentSelector)
        # fuse only if expr is also a rhythm command that bears a rhythm material request
        if not isinstance(expr, settingtools.RhythmRegionCommand):
            return False
        else:
            previous_rhythm_command = expr
        previous_material_request = getattr(previous_rhythm_command, 'request', None)
        if not isinstance(previous_material_request, selectortools.CounttimeComponentSelector):
            return False
        # fuse only if current and previous commands request same material
        if not current_material_request == previous_material_request:
            return False
        return True
