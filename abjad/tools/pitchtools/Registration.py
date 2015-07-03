# -*- encoding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class Registration(TypedList):
    '''A registration.

    ..  container:: example

        ::

        
            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = pitchtools.Registration(components)

        ::

            >>> print(format(registration))
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
                )

    Registrations model
    ``pitchtools.transpose_pitch_number_by_octave_transposition_mapping``
    input.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        r'''Calls registration on `pitches`.

        ..  container:: example

            **Example 1.** Transposes four pitches:

            ::

                >>> registration([-24, -22, -23, -21])
                [24, 26, 25, 15]

        ..  container:: example

            **Example 2.** Transposes four other pitches:

            ::

                >>> registration([0, 2, 1, 3])
                [36, 38, 37, 27]

        Returns list of new pitches.
        '''
        transposed_pitches = [self._transpose_pitch(x) for x in pitches]
        return transposed_pitches

    def __format__(self, format_specification=''):
        r'''Formats registration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            Gets storage format of registration:

            ::

                >>> print(format(registration))
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
                    )

        Returns string.
        '''
        superclass = super(Registration, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import pitchtools
        def coerce_(expr):
            if isinstance(expr, tuple):
                component = pitchtools.RegistrationComponent(*expr)
            elif isinstance(expr, pitchtools.RegistrationComponent):
                component = copy.copy(expr)
            else:
                raise TypeError(repr(expr))
            return component
        return coerce_

    @property
    def _one_line_menu_summary(self):
        name = 'registration'
        contents = []
        for registration_component in self:
            contents.append(registration_component._one_line_menu_summary)
        contents_string = ', '.join(contents)
        return '{}: {}'.format(name, contents_string)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        input_argument_tokens = []
        for registration_component in self:
            item = (
                registration_component.source_pitch_range.one_line_named_pitch_repr,
                registration_component.target_octave_start_pitch.pitch_number
                )
            input_argument_tokens.append(item)
        keyword_argument_names = []
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=(
                input_argument_tokens,
                ),
            )

    ### PRIVATE METHODS ###

    def _transpose_pitch(self, pitch):
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedPitch(pitch)
        target_pitch_class_number = pitch.pitch_class_number
        for component in self:
            if pitch in component.source_pitch_range:
                target_octave = range(
                    component.target_octave_start_pitch.pitch_number,
                    component.target_octave_start_pitch.pitch_number + 12
                    )
                for candidate_pitch in target_octave:
                    if candidate_pitch % 12 == pitch.pitch_class_number:
                        return candidate_pitch
        return pitch