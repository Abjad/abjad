from abjad.tools import mathtools


def split_sequence_by_weights(sequence, weights, cyclic=False, overhang=False):
    '''.. versionadded:: 2.0

    Split sequence by weights.
    
    Example 1. Split sequence cyclically by weights with overhang::

        >>> sequencetools.split_sequence_by_weights(
        ...     (10, -10, 10, -10), [3, 15, 3], cyclic=True, overhang=True)
        [(3,), (7, -8), (-2, 1), (3,), (6, -9), (-1,)]

    Example 2. Split sequence cyclically by weights without overhang::

        >>> sequencetools.split_sequence_by_weights(
        ...         (10, -10, 10, -10), [3, 15, 3], cyclic=True, overhang=False)
        [(3,), (7, -8), (-2, 1), (3,), (6, -9)]

    Example 3. Split sequence once by weights with overhang::

        >>> sequencetools.split_sequence_by_weights(
        ...     (10, -10, 10, -10), [3, 15, 3], cyclic=False, overhang=True)
        [(3,), (7, -8), (-2, 1), (9, -10)]

    Example 4. Split sequence once by weights without overhang::

        >>> sequencetools.split_sequence_by_weights(
        ...     (10, -10, 10, -10), [3, 15, 3], cyclic=False, overhang=False)
        [(3,), (7, -8), (-2, 1)]

    Return list of sequence types.
    '''
    from abjad.tools import sequencetools

    result = []
    current_index = 0
    current_piece = []

    if cyclic:
        weights = sequencetools.repeat_sequence_to_weight_at_most(weights, mathtools.weight(sequence))

    for weight in weights:
        current_piece_weight = mathtools.weight(current_piece)
        while current_piece_weight < weight:
            current_piece.append(sequence[current_index])
            current_index += 1
            current_piece_weight = mathtools.weight(current_piece)
        if current_piece_weight == weight:
            current_piece = type(sequence)(current_piece)
            result.append(current_piece)
            current_piece = []
        elif weight < current_piece_weight:
            overage = current_piece_weight - weight
            current_last_element = current_piece.pop(-1)
            needed = abs(current_last_element) - overage
            needed *= mathtools.sign(current_last_element)
            current_piece.append(needed)
            current_piece = type(sequence)(current_piece)
            result.append(current_piece)
            overage *= mathtools.sign(current_last_element)
            current_piece = [overage]

    if overhang:
        last_piece = current_piece
        last_piece.extend(sequence[current_index:])
        if last_piece:
            last_piece = type(sequence)(last_piece)
            result.append(last_piece)

    return result
