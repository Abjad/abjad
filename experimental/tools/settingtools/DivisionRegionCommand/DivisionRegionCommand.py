import copy
from abjad.tools import sequencetools
from experimental.tools.settingtools.RegionCommand import RegionCommand


class DivisionRegionCommand(RegionCommand):
    r'''Division region command.

    Region command indicating durated period of time 
    to which a division-maker will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, request=None, context_name=None, timespan=None, fresh=None, truncate=None):
        RegionCommand.__init__(self, request, context_name, timespan, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ### PRIVATE METHODS ###

    def _can_fuse(self, expr):
        '''True when self can fuse `expr` to the end of self. Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if self.truncate:
            return False
        if expr.fresh or expr.truncate:
            return False
        if expr.request != self.request:
            return False
        return True

    def _get_payload(self, score_specification, voice_name=None):
        from experimental.tools import settingtools
        payload = self.request._get_payload(score_specification)
        if payload is None:
            return
        elif isinstance(payload, settingtools.DivisionRegionProduct):
            divisions = payload.payload.divisions[:]
        else:
            divisions = [settingtools.Division(x) for x in payload]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.timespan.duration)
        division_region_product = settingtools.DivisionRegionProduct(
            divisions, voice_name, self.timespan.start_offset)
        return [division_region_product]

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Return string.
        '''
        return 'divisions'

    @property
    def truncate(self):
        '''Return boolean.
        '''
        return self._truncate

    @property
    def voice_name(self):
        '''Aliased to division region command `context_name`.

        Return string.
        '''
        return self.context_name
