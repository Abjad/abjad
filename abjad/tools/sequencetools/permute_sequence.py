# -*- coding: utf-8 -*-


def permute_sequence(sequence, permutation):
    '''Permutes `sequence`.

    ..  note:: Deprecated. Use ``sequencetools.Permutation`` instead.

    ..  container:: example

        **Example 1.** Permutes length-6 sequence:
        
        ::

            >>> sequence_ = [10, 11, 12, 13, 14, 15]
            >>> permutation = [5, 4, 0, 1, 2, 3]
            >>> sequencetools.permute_sequence(sequence_, permutation)
            [15, 14, 10, 11, 12, 13]

    ..  container:: example

        **Example 2.** Permutes length-6 sequence:
        
        ::

            >>> sequence_ = [10, 11, 12, 13, 14, 15]
            >>> permutation = sequencetools.Permutation([5, 4, 0, 1, 2, 3])
            >>> sequencetools.permute_sequence(sequence_, permutation)
            [15, 14, 10, 11, 12, 13]

    Copies references.
    
    Does not copy items.

    Returns new object of `sequence` type.
    '''
    from abjad.tools import sequencetools
    permutation = sequencetools.Permutation(permutation)
    result = permutation(sequence)
    return result
