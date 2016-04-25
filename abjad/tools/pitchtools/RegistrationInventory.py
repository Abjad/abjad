# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class RegistrationInventory(TypedList):
    '''Registration inventory.

    ..  container:: example

        **Example.** Inventory with two registrations:
        
        ::

            >>> registration_1 = pitchtools.Registration(
            ...     [('[A0, C4)', 15), ('[C4, C8)', 27)]
            ...     )
            >>> registration_2 = pitchtools.Registration(
            ...     [('[A0, C8]', -18)]
            ...     )
            >>> inventory = pitchtools.RegistrationInventory(
            ...     [registration_1, registration_2]
            ...     )

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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import pitchtools
        return pitchtools.Registration
