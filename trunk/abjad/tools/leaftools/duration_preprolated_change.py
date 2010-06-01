from abjad.exceptions import AssignabilityError
from abjad.leaf import _Leaf
from abjad.rational import Rational
from abjad.spanners import Tie
from abjad.tools import clone
from abjad.tools import construct
from abjad.tuplet import FixedMultiplierTuplet

   
def duration_preprolated_change(leaf, new_preprolated_duration):
   r'''Change `leaf` to dotted `preprolated_duration`::

      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.duration_preprolated_change(staff[1], Rational(3, 16))
      [Note(d', 8.)]
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8.
         e'8
         f'8 ]
      }
      
   Change `leaf` to tied `preprolated_duration`::
      
      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.duration_preprolated_change(staff[1], Rational(5, 32))
      [Note(d', 8), Note(d', 32)]
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8 ~
         d'32
         e'8
         f'8 ]
      }
      
   Change `leaf` to nonbinary `preprolated_duration`::
      
      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.duration_preprolated_change(staff[1], Rational(1, 12))
      [Note(d', 8)]
      abjad> f(staff)
      \new Staff {
         c'8 [
         \times 2/3 {
            d'8
         }
         e'8
         f'8 ]
      }
      
   Change `leaf` to tied nonbinary `preprolated_duration`::
      
      abjad> staff = Staff(construct.scale(4))
      abjad> Beam(staff.leaves)
      abjad> leaftools.duration_preprolated_change(staff[1], Rational(5, 48))
      [Note(d', 8), Note(d', 32)]
      abjad> f(staff)
      \new Staff {
         c'8 [
         \times 2/3 {
            d'8 ~
            d'32
         }
         e'8
         f'8 ]
      }
      
   Change `preprolated_duration` of `leaf` with LilyPond multiplier::
      
      abjad> note = Note(0, (1, 8))
      abjad> note.duration.multiplier = Rational(1, 2)
      abjad> leaftools.duration_preprolated_change(note, Rational(5, 48))
      [Note(c', 8 * 5/6)]
      abjad> f(note)
      c'8 * 5/6

   Return list of `leaf` and leaves newly tied to `leaf`.
   '''

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
         #print 'debug duration_tokens %s' % duration_tokens
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
