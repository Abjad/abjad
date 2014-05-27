# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.OctaveTranspositionMapping \
    import OctaveTranspositionMapping


class OctaveTranspositionMappingInventory(TypedList):
    '''An ordered list of octave transposition mappings.

    ::

        >>> mapping_1 = pitchtools.OctaveTranspositionMapping(
        ...     [('[A0, C4)', 15), ('[C4, C8)', 27)])
        >>> mapping_2 = pitchtools.OctaveTranspositionMapping(
        ...     [('[A0, C8]', -18)])
        >>> inventory = pitchtools.OctaveTranspositionMappingInventory(
        ...     [mapping_1, mapping_2])

    ::

        >>> print(format(inventory))
        pitchtools.OctaveTranspositionMappingInventory(
            [
                pitchtools.OctaveTranspositionMapping(
                    [
                        pitchtools.OctaveTranspositionMappingComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C4)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(15),
                            ),
                        pitchtools.OctaveTranspositionMappingComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[C4, C8)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(27),
                            ),
                        ]
                    ),
                pitchtools.OctaveTranspositionMapping(
                    [
                        pitchtools.OctaveTranspositionMappingComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C8]',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(-18),
                            ),
                        ]
                    ),
                ]
            )

    Octave transposition mapping inventories implement list interface
    and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest()

    @property
    def _item_callable(self):
        return OctaveTranspositionMapping