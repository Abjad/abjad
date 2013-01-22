from abjad.tools import durationtools
from experimental.tools.settingtools.StartPositionedDivisionProduct import StartPositionedDivisionProduct


class StartPositionedMeasureProduct(StartPositionedDivisionProduct):
    '''Measure region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> measure_product = settingtools.StartPositionedMeasureProduct(payload, 'Voice 1', Offset(0))

    ::

        >>> z(measure_product)
        settingtools.StartPositionedMeasureProduct(
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
