# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveTranspositionMappingInventory_storage_format_01():

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
    inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])

    assert testtools.compare(
        inventory.storage_format,
        r'''
        pitchtools.OctaveTranspositionMappingInventory([
            pitchtools.OctaveTranspositionMapping([
                pitchtools.OctaveTranspositionMappingComponent(
                    pitchtools.PitchRange(
                        '[A0, C4)'
                        ),
                    pitchtools.NumberedPitch(15)
                    ),
                pitchtools.OctaveTranspositionMappingComponent(
                    pitchtools.PitchRange(
                        '[C4, C8)'
                        ),
                    pitchtools.NumberedPitch(27)
                    )
                ]),
            pitchtools.OctaveTranspositionMapping([
                pitchtools.OctaveTranspositionMappingComponent(
                    pitchtools.PitchRange(
                        '[A0, C8]'
                        ),
                    pitchtools.NumberedPitch(-18)
                    )
                ])
            ])
        '''
        )
