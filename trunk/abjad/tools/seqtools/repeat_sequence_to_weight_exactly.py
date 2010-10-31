from abjad.tools.seqtools.repeat_sequence_to_weight import repeat_sequence_to_weight


def repeat_sequence_to_weight_exactly(sequence, weight):
   '''Repeat `sequence` to `weight` exactly::

      abjad> seqtools.repeat_sequence_to_weight_exactly((5, -5, -5), 23)
      (5, -5, -5, 5, -3)

   Return newly constructed `sequence` type.
   '''

   return repeat_sequence_to_weight(sequence, weight, remainder = 'chop')
