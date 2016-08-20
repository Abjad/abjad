# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class PitchArrayInventory(TypedList):
    r'''Pitch array inventory.

    ..  container:: example

        **Example 1.** A pitch array inventory:

        ::

            >>> array_1 = pitchtools.PitchArray([
            ...   [1, (2, 1), ([-2, -1.5], 2)],
            ...   [(7, 2), (6, 1), 1]])

        ::

            >>> array_2 = pitchtools.PitchArray([
            ...   [1, 1, 1],
            ...   [1, 1, 1]])

        ::

            >>> arrays = [array_1, array_2]
            >>> inventory = pitchtools.PitchArrayInventory(arrays)

        ::

            >>> print(format(inventory))
            pitchtools.PitchArrayInventory(
                [
                    pitchtools.PitchArray(
                        rows=(
                            pitchtools.PitchArrayRow(
                                cells=(
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("d'"),
                                            ],
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch('bf'),
                                            pitchtools.NamedPitch('bqf'),
                                            ],
                                        width=2,
                                        ),
                                    ),
                                ),
                            pitchtools.PitchArrayRow(
                                cells=(
                                    pitchtools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("g'"),
                                            ],
                                        width=2,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("fs'"),
                                            ],
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    pitchtools.PitchArray(
                        rows=(
                            pitchtools.PitchArrayRow(
                                cells=(
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            pitchtools.PitchArrayRow(
                                cells=(
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    pitchtools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def to_score(self):
        r'''Makes score from pitch arrays in inventory.

        ::

            >>> array_1 = pitchtools.PitchArray([
            ...   [1, (2, 1), ([-2, -1.5], 2)],
            ...   [(7, 2), (6, 1), 1]])

        ::

            >>> array_2 = pitchtools.PitchArray([
            ...   [1, 1, 1],
            ...   [1, 1, 1]])

        ::

            >>> arrays = [array_1, array_2]
            >>> inventory = pitchtools.PitchArrayInventory(arrays)

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

        Returns score.
        '''
        from abjad.tools import scoretools
        score = scoretools.Score([])
        staff_group = scoretools.StaffGroup([])
        score.append(staff_group)
        number_staves = self[0].depth
        staves = scoretools.Staff([]) * number_staves
        staff_group.extend(staves)
        for pitch_array in self:
            measures = pitch_array.to_measures()
            for staff, measure in zip(staves, measures):
                staff.append(measure)
        return score
