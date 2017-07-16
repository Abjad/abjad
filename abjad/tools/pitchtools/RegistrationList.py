# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class RegistrationList(TypedList):
    '''Registration list.

    ::

        >>> import abjad

    ..  container:: example

        Two registrations:
        
        ::

            >>> registration_1 = abjad.Registration(
            ...     [('[A0, C4)', 15), ('[C4, C8)', 27)]
            ...     )
            >>> registration_2 = abjad.Registration(
            ...     [('[A0, C8]', -18)]
            ...     )
            >>> registrations = abjad.RegistrationList(
            ...     [registration_1, registration_2]
            ...     )

        ::

            >>> f(registrations)
            abjad.RegistrationList(
                [
                    abjad.Registration(
                        [
                            abjad.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[A0, C4)'),
                                target_octave_start_pitch=abjad.NumberedPitch(15),
                                ),
                            abjad.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[C4, C8)'),
                                target_octave_start_pitch=abjad.NumberedPitch(27),
                                ),
                            ]
                        ),
                    abjad.Registration(
                        [
                            abjad.RegistrationComponent(
                                source_pitch_range=abjad.PitchRange('[A0, C8]'),
                                target_octave_start_pitch=abjad.NumberedPitch(-18),
                                ),
                            ]
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when registration list contains `argument`.
        Otherwise false.

        ..  container:: example

            Two registrations:
            
            ::

                >>> registration_1 = abjad.Registration(
                ...     [('[A0, C4)', 15), ('[C4, C8)', 27)]
                ...     )
                >>> registration_2 = abjad.Registration(
                ...     [('[A0, C8]', -18)]
                ...     )
                >>> registrations = abjad.RegistrationList(
                ...     [registration_1, registration_2]
                ...     )

            ::

                >>> abjad.Registration([('[A0, C4)', 15)]) in registrations
                False

            ::

                >>> abjad.Registration([
                ...     ('[A0, C4)', 15),
                ...     ('[C4, C8)', 27),
                ...     ]) in registrations
                True

        '''
        return super(RegistrationList, self).__contains__(argument)

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import pitchtools
        return pitchtools.Registration
