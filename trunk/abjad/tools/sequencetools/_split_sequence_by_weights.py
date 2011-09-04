from abjad.tools import mathtools
from abjad.tools.sequencetools.repeat_sequence_to_weight_at_most import repeat_sequence_to_weight_at_most


def _split_sequence_by_weights(sequence, weights, cyclic = False, overhang = False):
    '''.. versionadded:: 2.0

    Split sequence by weights.

    Return list of sequence types.
    '''

    result = []
    cur_index = 0
    cur_piece = []
    if cyclic:
        weights = repeat_sequence_to_weight_at_most(weights, mathtools.weight(sequence))
    for weight in weights:
        cur_piece_weight = mathtools.weight(cur_piece)
        while cur_piece_weight < weight:
            cur_piece.append(sequence[cur_index])
            cur_index += 1
            cur_piece_weight = mathtools.weight(cur_piece)
        if cur_piece_weight == weight:
            cur_piece = type(sequence)(cur_piece)
            result.append(cur_piece)
            cur_piece = []
        elif weight < cur_piece_weight:
            overage = cur_piece_weight - weight
            cur_last_element = cur_piece.pop(-1)
            needed = abs(cur_last_element) - overage
            needed *= mathtools.sign(cur_last_element)
            cur_piece.append(needed)
            cur_piece = type(sequence)(cur_piece)
            result.append(cur_piece)
            overage *= mathtools.sign(cur_last_element)
            cur_piece = [overage]

    if overhang:
        last_piece = cur_piece
        last_piece.extend(sequence[cur_index:])
        if last_piece:
            last_piece = type(sequence)(last_piece)
            result.append(last_piece)

    return result
