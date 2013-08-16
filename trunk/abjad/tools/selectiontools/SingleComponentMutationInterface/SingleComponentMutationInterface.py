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

    def copy(self, n=1):
        r'''Copies component and fractures crossing spanners.

        Returns new component.
        '''
        from abjad.tools import selectiontools
        selection = selectiontools.ContiguousSelection(self)
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

    def split_leaf_by_duration(
        self, 
        offset, 
        fracture_spanners=False,
        tie_split_notes=True, 
        tie_split_rests=False,
        ):
        r'''Splits `leaf` at `offset`.

        ..  container:: example
        
            **Example 1.** Split note at assignable offset. Two notes result. 
            Do not tie notes:

            ::

                >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
                >>> select(staff[:]).attach_spanners(spannertools.BeamSpanner)
                (BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|))
                >>> contexttools.DynamicMark('f')(staff.select_leaves()[0])
                DynamicMark('f')(c'8)
                >>> marktools.Articulation('accent')(staff.select_leaves()[0])
                Articulation('accent')(c'8)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'8 -\accent \f [ (
                        d'8 ]
                    }
                    {
                        e'8 [
                        f'8 ] )
                    }
                }

            ::

                >>> mutate(staff.select_leaves()[0]).split_leaf_by_duration(
                ...     Duration(1, 32),
                ...     tie_split_notes=False,
                ...     )
                ([Note("c'32")], [Note("c'16.")])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        c'32 -\accent \f [ (
                        c'16.
                        d'8 ]
                    }
                    {
                        e'8 [
                        f'8 ] )
                    }
                }

        ..  container:: example
        
            **Example 2.** Handle grace and after grace containers correctly.

            ::

                >>> staff = Staff(r"abj: | 2/8 c'8 ( d'8 || 2/8 e'8 f'8 ) |")
                >>> select(staff[:]).attach_spanners(spannertools.BeamSpanner)
                (BeamSpanner(|2/8(2)|), BeamSpanner(|2/8(2)|))
                >>> leaftools.GraceContainer("cs'16")(staff.select_leaves()[0])
                Note("c'8")
                >>> leaftools.GraceContainer("ds'16", kind='after')(staff.select_leaves()[0])
                Note("c'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \grace {
                            cs'16
                        }
                        \afterGrace
                        c'8 [ (
                        {
                            ds'16
                        }
                        d'8 ]
                    }
                    {
                        e'8 [
                        f'8 ] )
                    }
                }

            ::

                >>> mutate(staff.select_leaves()[0]).split_leaf_by_duration(
                ...     Duration(1, 32),
                ...     tie_split_notes=False,
                ...     )
                ([Note("c'32")], [Note("c'16.")])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        \grace {
                            cs'16
                        }
                        c'32 [ (
                        \afterGrace
                        c'16.
                        {
                            ds'16
                        }
                        d'8 ]
                    }
                    {
                        e'8 [
                        f'8 ] )
                    }
                }

        Returns pair.
        '''
        from abjad.tools import leaftools
        assert isinstance(self[0], leaftools.Leaf)
        return self[0]._split_by_duration(
            offset, 
            fracture_spanners=fracture_spanners,
            tie_split_notes=tie_split_notes, 
            tie_split_rests=tie_split_rests,
            )

    def split_leaf_by_durations(
        self,
        offsets,
        cyclic=False,
        fracture_spanners=False,
        tie_split_notes=True,
        tie_split_rests=False,
        ):
        r'''Splits `leaf` at `offsets`.

        ..  container:: example
        
            **Example 1.** Split note once at `offsets` and tie split notes:

            ::

                >>> staff = Staff("c'1 ( d'1 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'1 (
                    d'1 )
                }

            ::

                >>> mutate(staff[0]).split_leaf_by_durations(
                ...     [(3, 8)],
                ...     tie_split_notes=True,
                ...     )
                [[Note("c'4.")], [Note("c'2"), Note("c'8")]]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4. ( ~
                    c'2 ~
                    c'8
                    d'1 )
                }

        ..  container:: example
        
            **Example 2.** Split note cyclically at `offsets` and tie split notes:

            ::

                >>> staff = Staff("c'1 ( d'1 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'1 (
                    d'1 )
                }

            ::

                >>> mutate(staff[0]).split_leaf_by_durations(
                ...     [(3, 8)], 
                ...     cyclic=True,
                ...     tie_split_notes=True,
                ...     )
                [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4. ( ~
                    c'4. ~
                    c'4
                    d'1 )
                }

        ..  container:: example
        
            **Example 3.** Split note once at `offsets` and do no tie split notes:

            ::

                >>> staff = Staff("c'1 ( d'1 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'1 (
                    d'1 )
                }

            ::

                >>> mutate(staff[0]).split_leaf_by_durations(
                ...     [(3, 8)],
                ...     tie_split_notes=False,
                ...     )
                [[Note("c'4.")], [Note("c'2"), Note("c'8")]]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4. (
                    c'2 ~
                    c'8
                    d'1 )
                }

        ..  container:: example
        
            **Example 4.** Split note cyclically at `offsets` and do not 
            tie split notes:

            ::

                >>> staff = Staff("c'1 ( d'1 )")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'1 (
                    d'1 )
                }

            ::

                >>> mutate(staff[0]).split_leaf_by_durations(
                ...     [(3, 8)], 
                ...     cyclic=True,
                ...     tie_split_notes=False,
                ...     )
                [[Note("c'4.")], [Note("c'4.")], [Note("c'4")]]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'4. (
                    c'4.
                    c'4
                    d'1 )
                }

        ..  container:: example
        
            **Example 5.** Split tupletted note once at `offsets` 
            and tie split notes:

            ::

                >>> staff = Staff(r"\times 2/3 { c'2 ( d'2 e'2 ) }")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'2 (
                        d'2
                        e'2 )
                    }
                }

            ::

                >>> mutate(staff.select_leaves()[1]).split_leaf_by_durations(
                ...     [(1, 6)], 
                ...     cyclic=False,
                ...     tie_split_notes=True,
                ...     )
                [[Note("d'4")], [Note("d'4")]]
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'2 (
                        d'4 ~
                        d'4
                        e'2 )
                    }
                }

        .. note:: Add examples showing mark and context mark handling.

        Returns list of shards.
        '''
        from abjad.tools import leaftools
        assert isinstance(self[0], leaftools.Leaf)
        return self[0]._split_by_durations(
            offsets,
            cyclic=cyclic,
            fracture_spanners=fracture_spanners,
            tie_split_notes=tie_split_notes,
            tie_split_rests=tie_split_rests,
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
