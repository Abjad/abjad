# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.OctaveTranspositionMapping \
	import OctaveTranspositionMapping


class OctaveTranspositionMappingInventory(TypedList):
    '''Model of an ordered list of octave transposition mappings:

    ::

        >>> mapping_1 = pitchtools.OctaveTranspositionMapping(
        ...     [('[A0, C4)', 15), ('[C4, C8)', 27)])
        >>> mapping_2 = pitchtools.OctaveTranspositionMapping(
        ...     [('[A0, C8]', -18)])
        >>> inventory = pitchtools.OctaveTranspositionMappingInventory(
        ...     [mapping_1, mapping_2])

    ::

        >>> z(inventory)
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

    Octave transposition mapping inventories implement list interface 
    and are mutable.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return OctaveTranspositionMapping
