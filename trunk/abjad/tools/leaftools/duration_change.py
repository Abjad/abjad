from abjad.exceptions import AssignabilityError
from abjad.leaf.leaf import _Leaf
from abjad.rational import Rational
from abjad.spanners.tie import Tie
from abjad.tools import clone
from abjad.tools import construct
from abjad.tuplet import FixedMultiplierTuplet

   
def duration_change(leaf, new_preprolated_duration):
   '''Change preprolated duration of 'leaf' to 'new_preprolated_duration'.
      It 'leaf' carries LilyPond multiplier, change only LilyPond multiplier.
      For durations like 3/16, change note_head.
      For durations like 5/16, splice tied notes to right.
      For durations like 3/14, enclose in tuplet, change note_head.
      For durations like 5/14, enclose in tuplet, splice tied notes.
      Return list modified original leaf and any additional new leaves.'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(new_preprolated_duration, Rational)

   ## If leaf carries LilyPond multiplier, change only LilyPond multiplier.
   if leaf.duration.multiplier is not None:
      leaf.duration.multiplier = \
         new_preprolated_duration / leaf.duration.written
      return [leaf]

   ## If leaf does not carry LilyPond multiplier, change other values.
   try:
      leaf.duration.written = new_preprolated_duration  
      all_leaves = [leaf]
   except AssignabilityError:
      duration_tokens = construct.notes(0, new_preprolated_duration)
      if isinstance(duration_tokens[0], _Leaf):
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = clone.unspan([leaf], num_tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         leaf.splice(tied_leaves)
         if not leaf.tie.parented:
            Tie(all_leaves)
      elif isinstance(duration_tokens[0], FixedMultiplierTuplet):
         print 'debug duration_tokens %s' % duration_tokens
         fmtuplet = duration_tokens[0]
         duration_tokens = fmtuplet[:]
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = clone.unspan([leaf], num_tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         leaf.splice(tied_leaves)
         if not leaf.tie.spanned:
            Tie(all_leaves) 
         tuplet_multiplier = fmtuplet.duration.multiplier
         FixedMultiplierTuplet(tuplet_multiplier, all_leaves)
      else:
         raise ValueError('unexpected output from construct.notes.')

   return all_leaves
