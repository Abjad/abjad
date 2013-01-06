import copy
from abjad.tools import sequencetools
from experimental.tools.settingtools.RegionCommand import RegionCommand


class DivisionRegionCommand(RegionCommand):
    r'''Division command.

    RegionCommand indicating durated period of time 
    to which an evaluated request will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, request, context_name, timespan, fresh=None, truncate=None):
        RegionCommand.__init__(self, request, context_name, timespan, fresh=fresh)
        assert isinstance(truncate, (bool, type(None))), repr(truncate)
        self._truncate = truncate

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name):
        from experimental.tools import divisiontools
        from experimental.tools import selectortools
        from experimental.tools import settingtools
        region_timespan = self.timespan
        region_duration = self.timespan.duration
        # TODO: remove getattr() by implementing voice_name on all request classes
        request_voice_name = getattr(self.request, 'voice_name', None)
        if isinstance(self.request, selectortools.DivisionSelector):
            division_region_product = self.request._get_payload(score_specification, request_voice_name)
            if division_region_product is None:
                return
            divisions = division_region_product.payload.divisions[:]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            divisions = [settingtools.Division(x) for x in divisions]
            division_list = division_region_product.payload.new(divisions=divisions)
            division_region_product = division_region_product.new(payload=division_list)
            right = self.timespan.start_offset
            left = division_region_product.timespan.start_offset
            addendum = right - left
            division_region_product = division_region_product.translate_offsets(
                start_offset_translation=addendum, stop_offset_translation=addendum)
            return [division_region_product]
        else:
            divisions = self.request._get_payload(score_specification, request_voice_name)
            divisions = [settingtools.Division(x) for x in divisions]
            divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, region_duration)
            result = settingtools.DivisionRegionProduct(divisions, voice_name, region_timespan)
            return [result]

    ## READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return 'divisions'

    @property
    def truncate(self):
        return self._truncate

    @property
    def voice_name(self):
        '''Aliased to ``self.context_name``.
        '''
        return self.context_name

    ### PUBLIC METHODS ###

    def can_fuse(self, expr):
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
