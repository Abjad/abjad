from abjad.tools import durationtools
from abjad.tools import sequencetools
from experimental.tools.settingtools.StartPositionedDivisionProduct import StartPositionedDivisionProduct


class StartPositionedBeatProduct(StartPositionedDivisionProduct):
    '''Beat region product:

    ::

        >>> payload = [(6, 8), (6, 8), (3, 4)]
        >>> beat_region_product = settingtools.StartPositionedBeatProduct(payload, 'Voice 1', Offset(0))

    ::

        >>> z(beat_region_product)
        settingtools.StartPositionedBeatProduct(
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

    pass
