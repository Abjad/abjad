# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class SingleComponentMutationInterface(Selection):
    r'''The Abjad mutators defined against a single component.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import componenttools
        assert isinstance(music, componenttools.Component), expr(music)
        Selection.__init__(self, music=music)

    ### PUBLIC METHODS ###

    def copy_and_fracture_crossing_spanners(self, n=1):
        r'''Copies component and fractures crossing spanners.

        Returns new component.
        '''
        from abjad.tools import selectiontools
        selection = selectiontools.ContiguousSelection(self)
        result = selection.copy_and_fracture_crossing_spanners(n=n)
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

    def split_in_halves(self, n=2):
        r'''Splits notes, rests and chords in halves.

        ::

            >>> staff = Staff("c'4 ( e'4 d'4 f'4 )")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 (
                e'4
                d'4
                f'4 )
            }

        ::

            >>> mutate(staff[0]).split_in_halves(n=4)
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'16 (
                c'16
                c'16
                c'16
                e'4
                d'4
                f'4 )
            }

        Set `n` to  ``1, 2, 4, 8, 16, ...`` or some other
        nonnegative integer power of ``2``.

        Replaces note, rest or chord with `n` new notes, rests or chords.

        Preserves spanners.

        Produces only notes, rests or chords and 
        never tuplets or other containers.

        Returns none.
        '''
        return self[0]._split_in_halves(
            n=n,
            )
