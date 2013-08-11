# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class MutationInterface(Selection):
    r'''The Abjad mutators defined against a single component.
    '''

    ### PUBLIC METHODS ###

    def divide(self, pitch=None):
        r'''Divides leaf at `pitch`.

        ..  container:: example

            **Example.** Divide chord at ``Eb4``:

                >>> chord = Chord("<d' ef' e'>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> pitch = pitchtools.NamedChromaticPitch('Eb4')
                >>> upper, lower = mutate(chord).divide(pitch=pitch)
                >>> staff = Staff([upper, lower])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <ef' e'>4
                    d'4
                }

        Set `pitch` to pitch, pitch name, pitch number or none.

        Sets `pitch` equal to ``B3`` when `pitch` is none.

        Defined against leaves only; not defined against containers.

        Returns pair of newly created leaves.
        '''
        return self[0]._divide(
            pitch=pitch,
            )

    def shorten(self, duration):
        r'''Shortens component by `duration`.

        Returns none.
        '''
        return self[0]._shorten(duration)

    def splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        r'''Splices `components` to the right or left of selection.

        Returns list of components.
        '''
        if direction == Right:
            reference_component = self[-1]
        else:
            reference_component = self[0]
        return reference_component._splice(
            components,
            direction=direction, 
            grow_spanners=grow_spanners,
            )
