from abjad import *


def test_OctaveTranspositionMappingInventory_storage_format_01():

    mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
    inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])

    r'''
    pitchtools.OctaveTranspositionMappingInventory([
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent(
                pitchtools.PitchRange(
                    '[A0, C4)'
                    ),
                pitchtools.NumberedChromaticPitch(
                    15
                    )
                ),
            pitchtools.OctaveTranspositionMappingComponent(
                pitchtools.PitchRange(
                    '[C4, C8)'
                    ),
                pitchtools.NumberedChromaticPitch(
                    27
                    )
                )
            ]),
        pitchtools.OctaveTranspositionMapping([
            pitchtools.OctaveTranspositionMappingComponent(
                pitchtools.PitchRange(
                    '[A0, C8]'
                    ),
                pitchtools.NumberedChromaticPitch(
                    -18
                    )
                )
            ])
        ])
    '''

    assert inventory.storage_format == "pitchtools.OctaveTranspositionMappingInventory([\n\tpitchtools.OctaveTranspositionMapping([\n\t\tpitchtools.OctaveTranspositionMappingComponent(\n\t\t\tpitchtools.PitchRange(\n\t\t\t\t'[A0, C4)'\n\t\t\t\t),\n\t\t\tpitchtools.NumberedChromaticPitch(\n\t\t\t\t15\n\t\t\t\t)\n\t\t\t),\n\t\tpitchtools.OctaveTranspositionMappingComponent(\n\t\t\tpitchtools.PitchRange(\n\t\t\t\t'[C4, C8)'\n\t\t\t\t),\n\t\t\tpitchtools.NumberedChromaticPitch(\n\t\t\t\t27\n\t\t\t\t)\n\t\t\t)\n\t\t]),\n\tpitchtools.OctaveTranspositionMapping([\n\t\tpitchtools.OctaveTranspositionMappingComponent(\n\t\t\tpitchtools.PitchRange(\n\t\t\t\t'[A0, C8]'\n\t\t\t\t),\n\t\t\tpitchtools.NumberedChromaticPitch(\n\t\t\t\t-18\n\t\t\t\t)\n\t\t\t)\n\t\t])\n\t])"
