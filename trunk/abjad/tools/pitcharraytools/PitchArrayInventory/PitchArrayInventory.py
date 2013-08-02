# -*- encoding: utf-8 -*-
from abjad.tools import measuretools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class PitchArrayInventory(ObjectInventory):
    r'''Ordered collection of pitch arrays:

        >>> array_1 = pitcharraytools.PitchArray([
        ...   [1, (2, 1), ([-2, -1.5], 2)],
        ...   [(7, 2), (6, 1), 1]])

    ::

        >>> array_2 = pitcharraytools.PitchArray([
        ...   [1, 1, 1],
        ...   [1, 1, 1]])

    ::

        >>> arrays = [array_1, array_2]
        >>> inventory = pitcharraytools.PitchArrayInventory(arrays)

    ::

        >>> z(inventory)
        pitcharraytools.PitchArrayInventory([
            pitcharraytools.PitchArray(),
            pitcharraytools.PitchArray()
            ])

    '''

    def to_score(self):
        r'''Make score from pitch arrays in inventory:

        ::

            >>> array_1 = pitcharraytools.PitchArray([
            ...   [1, (2, 1), ([-2, -1.5], 2)],
            ...   [(7, 2), (6, 1), 1]])

        ::

            >>> array_2 = pitcharraytools.PitchArray([
            ...   [1, 1, 1],
            ...   [1, 1, 1]])

        ::

            >>> arrays = [array_1, array_2]
            >>> inventory = pitcharraytools.PitchArrayInventory(arrays)

        ::

            >>> score = inventory.to_score()

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new StaffGroup <<
                    \new Staff {
                        {
                            \time 4/8
                            r8
                            d'8
                            <bf bqf>4
                        }
                        {
                            \time 3/8
                            r8
                            r8
                            r8
                        }
                    }
                    \new Staff {
                        {
                            \time 4/8
                            g'4
                            fs'8
                            r8
                        }
                        {
                            \time 3/8
                            r8
                            r8
                            r8
                        }
                    }
                >>
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Create one staff per pitch-array row.

        Return score.
        '''
        score = scoretools.Score([])
        staff_group = scoretools.StaffGroup([])
        score.append(staff_group)
        number_staves = self[0].depth
        staves = stafftools.Staff([]) * number_staves
        staff_group.extend(staves)
        for pitch_array in self:
            measures = pitch_array.to_measures()
            for staff, measure in zip(staves, measures):
                staff.append(measure)
        return score
