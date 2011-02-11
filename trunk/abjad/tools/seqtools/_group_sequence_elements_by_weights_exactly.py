from abjad.tools.seqtools.flatten_sequence import flatten_sequence
from abjad.tools.seqtools._split_sequence_by_weights import _split_sequence_by_weights


def _group_sequence_elements_by_weights_exactly(sequence, weights, cyclic, overhang):
   candidate = _split_sequence_by_weights(sequence, weights, cyclic = cyclic, overhang = overhang)
   flattened_candidate = flatten_sequence(candidate)
   if flattened_candidate == sequence[:len(flattened_candidate)]:
      return candidate
   else:
      raise PartitionError('can not group exactly.') 
