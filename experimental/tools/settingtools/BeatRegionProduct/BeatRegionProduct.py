from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.settingtools.DivisionRegionProduct import DivisionRegionProduct


class BeatRegionProduct(DivisionRegionProduct):
    '''Beat region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> beat_region_product = settingtools.BeatRegionProduct(payload, 'Voice 1', Offset(0))

    ::

        >>> z(beat_region_product)
        settingtools.BeatRegionProduct(
            payload=settingtools.DivisionList(
                [Division('[6, 8]', start_offset=Offset(0, 1)),                 
                Division('[6, 8]', start_offset=Offset(3, 4)), 
                Division('[3, 4]', start_offset=Offset(3, 2))],
                voice_name='Voice 1',
                start_offset=durationtools.Offset(0, 1)
                ),
            voice_name='Voice 1',
            start_offset=durationtools.Offset(0, 1)
            )

    Contiguous block of one voice's beats.
    '''

    ### PRIVATE METHODS ###

    # TODO: eventually hoist to DivisionRegionProduct
    # TODO: return only result; do not return result.start_offset
    def _getitem(self, expr):
        assert isinstance(expr, slice), repr(expr)
        divisions = self.payload.__getitem__(expr)
        if divisions:
            start_offset = divisions[0].start_offset
        else:
            start_offset = durationtools.Offset(0)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=start_offset)
        return result, result.start_offset

    ### PUBLIC METHODS ###

    # TODO: eventually hoist to DivisionRegionProduct
    def repeat_to_duration(self, duration):
        divisions = sequencetools.repeat_sequence_to_weight_exactly(self.payload, duration)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result

    # TODO: eventually hoist to DivisionRegionProduct
    def repeat_to_length(self, length):
        divisions = sequencetools.repeat_sequence_to_length(self.payload, length)
        result = type(self)(payload=divisions, voice_name=self.voice_name, start_offset=self.start_offset)
        return result
