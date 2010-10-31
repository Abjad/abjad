from abjad.tools.seqtools._repeat_sequence_to_weight import _repeat_sequence_to_weight


def repeat_sequence_to_weight_at_least(sequence, weight):
   '''Repeat `sequence` to `weight` at least::

      abjad> seqtools.repeat_sequence_to_weight_at_least((5, -5, -5), 23)
      (5, -5, -5, 5, -5)

   Return newly constructed `sequence` type.
   '''

   return _repeat_sequence_to_weight(sequence, weight, remainder = 'more')
