# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class ScoreMutationAgent(AbjadObject):
    r'''The Abjad mutators defined against a single component.
    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PUBLIC METHODS ###

    def copy(self, n=1):
        r'''Copies component and fractures crossing spanners.

        Returns new component.
        '''
        from abjad.tools import selectiontools
        selection = selectiontools.ContiguousSelection(self._client)
        result = selection.copy(n=n)
        if len(result) == 1:
            result = result[0]
        return result

    def divide(self, pitch=None):
        r'''Divides leaf at `pitch`.

        ..  container:: example

            **Example.** Divide chord at ``Eb4``:

                >>> chord = Chord("<d' ef' e'>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> pitch = pitchtools.NamedPitch('Eb4')
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
        return self._client._divide(
            pitch=pitch,
            )

    def shorten(self, duration):
        r'''Shortens component by `duration`.

        Returns none.
        '''
        return self._client._shorten(duration)

    def splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        r'''Splices `components` to the right or left of selection.

        Returns list of components.
        '''
        return self._client._splice(
            components,
            direction=direction, 
            grow_spanners=grow_spanners,
            )
