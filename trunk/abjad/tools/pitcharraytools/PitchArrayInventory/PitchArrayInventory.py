from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class PitchArrayInventory(ObjectInventory):
    '''Ordered collection of pitch arrays:

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

    pass
