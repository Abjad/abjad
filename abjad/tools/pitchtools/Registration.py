# -*- coding: utf-8 -*-
import copy
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TypedList import TypedList


class Registration(TypedList):
    '''Registration.

    ::

        >>> import abjad

    ..  container:: example

        Registration in two parts:

        ::

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = abjad.Registration(components)

        ::

            >>> f(registration)
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
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        r"""Calls registration on `pitches`.

        ..  container:: example

            Transposes four pitches:

            ::

                >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
                >>> registration = abjad.Registration(components)
                >>> pitches = registration([-24, -22, -23, -21])
                >>> for pitch in pitches:
                ...     pitch
                ...
                NamedPitch("c'''")
                NamedPitch("d'''")
                NamedPitch("cs'''")
                NamedPitch("ef''")

        ..  container:: example

            Transposes four other pitches:

            ::

                >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
                >>> registration = abjad.Registration(components)
                >>> pitches = registration([0, 2, 1, 3])
                >>> for pitch in pitches:
                ...     pitch
                ...
                NamedPitch("c''''")
                NamedPitch("d''''")
                NamedPitch("cs''''")
                NamedPitch("ef'''")

        ..  container:: example

            Transposes four quartertones:

            ::

                >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
                >>> registration = abjad.Registration(components)
                >>> pitches = registration([0.5, 2.5, 1.5, 3.5])
                >>> for pitch in pitches:
                ...     pitch
                ...
                NamedPitch("cqs''''")
                NamedPitch("dqs''''")
                NamedPitch("dqf''''")
                NamedPitch("eqf'''")

        Returns list of new pitches.
        """
        transposed_pitches = [self._transpose_pitch(x) for x in pitches]
        return transposed_pitches

    def __format__(self, format_specification=''):
        r'''Formats registration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            Gets storage format of registration:

            ::

                >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
                >>> registration = abjad.Registration(components)

            ::

                >>> f(registration)
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
                    )

        Returns string.
        '''
        superclass = super(Registration, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import pitchtools
        def coerce_(argument):
            if isinstance(argument, tuple):
                component = pitchtools.RegistrationComponent(*argument)
            elif isinstance(argument, pitchtools.RegistrationComponent):
                component = copy.copy(argument)
            else:
                raise TypeError(repr(argument))
            return component
        return coerce_

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = []
        for registration_component in self:
            item = (
                registration_component.source_pitch_range.range_string,
                registration_component.target_octave_start_pitch.number
                )
            values.append(item)
        return systemtools.FormatSpecification(
            client=self,
            repr_args_values=[values],
            repr_is_indented=False,
            repr_kwargs_names=[],
            storage_format_args_values=[self._collection],
            storage_format_kwargs_names=[],
            )

    def _transpose_pitch(self, pitch):
        from abjad.tools import pitchtools
        pitch = pitchtools.NamedPitch(pitch)
        for component in self:
            if pitch in component.source_pitch_range:
                start_pitch = component.target_octave_start_pitch
                stop_pitch = start_pitch + 12
                if start_pitch <= pitch < stop_pitch:
                    return pitch
                elif pitch < start_pitch:
                    while pitch < start_pitch:
                        pitch += 12
                    return pitch
                elif stop_pitch <= pitch:
                    while stop_pitch <= pitch:
                        pitch -= 12
                    return pitch
                else:
                    raise ValueError(pitch, self)
        else:
            message = 'pitch {} not in {}.'
            message = message.format(pitch, self)
            raise ValueError(message)
