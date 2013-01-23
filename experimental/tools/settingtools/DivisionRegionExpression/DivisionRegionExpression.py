import copy
from abjad.tools import sequencetools
from experimental.tools.settingtools.RegionExpression import RegionExpression


class DivisionRegionExpression(RegionExpression):
    r'''Division region command.

    Region command indicating durated period of time 
    to which a division-maker will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, expression=None, context_name=None, timespan=None, fresh=None, truncate=None):
        RegionExpression.__init__(self, expression, context_name, timespan, fresh=fresh)
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
        if expr.expression != self.expression:
            return False
        return True

    def _evaluate(self):
        from experimental.tools import settingtools
        result = self.expression._evaluate()
        if result is None:
            return
        assert isinstance(result, (settingtools.PayloadExpression, tuple, list)), repr(result)
        # TODO: eventually remove this branch in favor of the next branch
        if isinstance(result, settingtools.VoicedStartPositionedDivisionPayloadExpression):
            divisions = result.payload.divisions[:]
        elif isinstance(result, settingtools.VoicedStartPositionedPayloadExpression):
            divisions = result._payload_elements[:]
        elif isinstance(result, list) and len(result) == 1 and isinstance(result[0], tuple):
            divisions = result[0][:]
        else:
            divisions = [settingtools.Division(x) for x in result]
        divisions = sequencetools.repeat_sequence_to_weight_exactly(divisions, self.timespan.duration)
        result = settingtools.VoicedStartPositionedDivisionPayloadExpression(
            divisions, self.voice_name, self.timespan.start_offset)
        return [result]

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
