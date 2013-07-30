from abjad.tools.selectiontools.FreeSelection import FreeSelection


class TupletSelection(FreeSelection):
    '''Free selection of tuplets.
    '''

    ### PUBLIC METHODS ###

    def remove(self):
        r'''Remove tuplets in selection.

        Example 1. Remove trivial tuplets in selection:

        ::

            >>> tuplet_1 = Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = Tuplet((1, 1), "g'4 fs'4")
            >>> staff = Staff([tuplet_1, tuplet_2])

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }
                {
                    g'4
                    fs'4
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> selection = selectiontools.select_tuplets(
            ...     staff,
            ...     include_augmented_tuplets=False,
            ...     include_diminished_tuplets=False,
            ...     include_trivial_tuplets=True,
            ...     )

        ::

            >>> selection
            TupletSelection(Tuplet(1, [g'4, fs'4]),)

        ::

            >>> selection.remove()

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }
                g'4
                fs'4
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import componenttools
        for tuplet in self:
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])
