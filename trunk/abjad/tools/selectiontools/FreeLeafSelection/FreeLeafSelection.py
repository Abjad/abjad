# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.FreeSelection import FreeSelection


class FreeLeafSelection(FreeSelection):
    r'''Free selection of leaves.
    '''

    ### PUBLIC METHODS ###

    def to_tuplets_with_ratio(self, proportions, is_diminution=True):
        r'''Change leaves in selection to tuplets with `proportions`.

        ::

            >>> note = Note("c'8.")
            >>> selection = selectiontools.select_leaves(note)

        Example 1. Change leaves in selection to augmented tuplets with 
        `proportions`:

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            {
                c'8.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            {
                c'16
                c'8
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 8/5 {
                c'64.
                c'32.
                c'32.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/2 {
                c'64
                c'32
                c'32
                c'32.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3, 3], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 12/11 {
                c'64
                c'32
                c'32
                c'32.
                c'32.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3, 3, 4], 
            ...     is_diminution=False,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 8/5 {
                c'128
                c'64
                c'64
                c'64.
                c'64.
                c'32
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        Example 2. Change leaves in selection to diminished tuplets:

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1], 
            ...     is_diminution=True,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            {
                c'8.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2], 
            ...     is_diminution=True,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            {
                c'16
                c'8
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2], is_diminution=True)

        ..  doctest::

            >>> f(tuplets[0]) 
            \times 4/5 {
                c'32.
                c'16.
                c'16.
            }
            
        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3], is_diminution=True,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'32
                c'16
                c'16
                c'16.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3, 3], 
            ...     is_diminution=True,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 6/11 {
                c'32
                c'16
                c'16
                c'16.
                c'16.
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        ::

            >>> tuplets = selection.to_tuplets_with_ratio(
            ...     [1, 2, 2, 3, 3, 4], 
            ...     is_diminution=True,
            ...     )

        ..  doctest::

            >>> f(tuplets[0]) 
            \times 4/5 {
                c'64
                c'32
                c'32
                c'32.
                c'32.
                c'16
            }

        ::

            >>> show(stafftools.RhythmicStaff(tuplets)) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import selectiontools
        result = []
        for leaf in self:
            tuplet = leaf._to_tuplet_with_ratio(
                proportions, 
                is_diminution=is_diminution,
                )
            result.append(tuplet)
        return selectiontools.FreeTupletSelection(result)
