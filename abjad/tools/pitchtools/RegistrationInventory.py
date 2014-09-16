# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.Registration \
    import Registration


class RegistrationInventory(TypedList):
    '''An ordered list of octave transposition mappings.

    ::

        >>> mapping_1 = pitchtools.Registration(
        ...     [('[A0, C4)', 15), ('[C4, C8)', 27)])
        >>> mapping_2 = pitchtools.Registration(
        ...     [('[A0, C8]', -18)])
        >>> inventory = pitchtools.RegistrationInventory(
        ...     [mapping_1, mapping_2])

    ::

        >>> print(format(inventory))
        pitchtools.RegistrationInventory(
            [
                pitchtools.Registration(
                    [
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[A0, C4)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(15),
                            ),
                        pitchtools.RegistrationComponent(
                            source_pitch_range=pitchtools.PitchRange(
                                range_string='[C4, C8)',
                                ),
                            target_octave_start_pitch=pitchtools.NumberedPitch(27),
                            ),
                        ]
                    ),
                pitchtools.Registration(
                    [
                        pitchtools.RegistrationComponent(
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
    def _coerce_item(self):
        return Registration