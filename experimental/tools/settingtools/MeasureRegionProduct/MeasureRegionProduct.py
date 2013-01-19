from experimental.tools.settingtools.DivisionRegionProduct import DivisionRegionProduct


class MeasureRegionProduct(DivisionRegionProduct):
    '''Measure region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> measure_region_product = settingtools.MeasureRegionProduct(payload, 'Voice 1', Offset(0))

    ::

        >>> z(measure_region_product)
        settingtools.MeasureRegionProduct(
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

    Contiguous block of one voice's measures.
    '''

    pass
