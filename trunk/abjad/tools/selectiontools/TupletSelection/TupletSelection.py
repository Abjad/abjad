from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.selectiontools.FreeSelection import FreeSelection


class TupletSelection(FreeSelection):
    '''Free selection of tuplets.
    '''

    ### PUBLIC METHODS ###

    # TODO: reimplement as a keyword variation on self.remove()
    def move_prolation_to_contents_and_remove(self):
        r'''Move prolation of tupets in selection to contents of 
        of tuplets in selection and then remove tuplets in selection.

        Example 1.

        ::

            >>> staff = Staff(
            ...     r"\times 3/2 { c'8 [ d'8 } \times 3/2 { c'8 d'8 ] }"
            ...     )

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8 [
                    d'8
                }
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8
                    d'8 ]
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> selection = selectiontools.select_tuplets(staff[0])
            >>> selection.move_prolation_to_contents_and_remove()

        ::

            >>> f(staff)
            \new Staff {
                c'8. [
                d'8.
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8
                    d'8 ]
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        for tuplet in self:
            containertools.scale_contents_of_container(
                tuplet, tuplet.multiplier)
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [tuplet], tuplet[:])
        
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

    def scale_contents(self, multiplier):
        r'''Scale contents of fixed-duration tuplets in selection
        by `multiplier`.

        Example 1. Double duration of tuplets in selection:
        ::

            >>> tuplet = tuplettools.FixedDurationTuplet((3, 8), [])
            >>> tuplet.extend("c'8 d'8 e'8 f'8 g'8")

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'8
                d'8
                e'8
                f'8
                g'8
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        ::

            >>> selection = selectiontools.select_tuplets(tuplet)
            >>> selection.scale_contents(Multiplier(2))

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'4
                d'4
                e'4
                f'4
                g'4
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        Preserve tuplet multipliers.

        Return none.
        '''
        from abjad.tools import leaftools
        from abjad.tools import tuplettools
        multiplier = durationtools.Multiplier(multiplier)
        for tuplet in self:
            if isinstance(tuplet, tuplettools.FixedDurationTuplet):
                # find new target duration
                old_target_duration = tuplet.target_duration
                new_target_duration = multiplier * old_target_duration
                # change tuplet target duration
                tuplet.target_duration = new_target_duration
                # if multiplier is note head assignable, 
                # scale contents graphically
                if multiplier.is_assignable:
                    for component in tuplet[:]:
                        if isinstance(component, leaftools.Leaf):
                            leaftools.scale_preprolated_leaf_duration(
                                component, multiplier)
                # otherwise doctor up tuplet multiplier, if necessary
                elif not tuplet.multiplier.is_proper_tuplet_multiplier:
                    tuplettools.fix_contents_of_tuplets_in_expr(tuplet)
            else:
                for component in tuplet[:]:
                    if isinstance(component, leaftools.Leaf):
                        leaftools.scale_preprolated_leaf_duration(
                            component, multiplier)

    def set_denominator_to_at_least(self, n):
        r'''Set denominator of tuplets in selection to at least `n`.

        Example 1. Set denominator of tuplets to at least ``8``:

        ::

            >>> tuplet = Tuplet(Fraction(3, 5), "c'4 d'8 e'8 f'4 g'2")

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/5 {
                c'4
                d'8
                e'8
                f'4
                g'2
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        ::

            >>> tuplets = selectiontools.select_tuplets(tuplet)
            >>> tuplets.set_denominator_to_at_least(8)

        ..  doctest::

            >>> f(tuplet)
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 6/10 {
                c'4
                d'8
                e'8
                f'4
                g'2
            }

        ::

            >>> show(tuplet) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import tuplettools

        assert mathtools.is_nonnegative_integer_power_of_two(n)
        Duration = durationtools.Duration
        #for tuplet in iterationtools.iterate_tuplets_in_expr(expr):
        for tuplet in self:
            tuplet.force_fraction = True
            durations = [
                tuplet.contents_duration, 
                tuplet._preprolated_duration, 
                (1, n),
                ]
            duration_pairs = Duration.durations_to_nonreduced_fractions_with_common_denominator(
                durations)
            tuplet.preferred_denominator = duration_pairs[1].numerator
