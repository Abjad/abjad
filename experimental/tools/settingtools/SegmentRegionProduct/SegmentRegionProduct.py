from experimental.tools.settingtools.RegionProduct import RegionProduct


class SegmentRegionProduct(RegionProduct):
    '''Segment region product:

    .. note:: add example.

    Contiguous block of one voice's segments.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _payload_elements(self):
        return self.payload

    ### PRIVATE METHODS ###

    def _split_payload_at_offsets(self, offsets):
        raise NotImplemented
