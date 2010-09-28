from abjad.components._Leaf import _Leaf
from abjad.components.Tuplet import Tuplet
from abjad.exceptions import AssignabilityError
from abjad.tools import componenttools
from abjad.tools import spannertools
from abjad.tools.notetools.make_notes import make_notes
from fractions import Fraction

   
def set_preprolated_leaf_duration(leaf, new_preprolated_duration):
   r'''Change `leaf` to dotted `preprolated_duration`::

      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.set_preprolated_leaf_duration(staff[1], Fraction(3, 16))
      [Note(d', 8.)]
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8.
         e'8
         f'8 ]
      }
      
   Change `leaf` to tied `preprolated_duration`::
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.set_preprolated_leaf_duration(staff[1], Fraction(5, 32))
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
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.set_preprolated_leaf_duration(staff[1], Fraction(1, 12))
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
      
      abjad> staff = Staff(macros.scale(4))
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> leaftools.set_preprolated_leaf_duration(staff[1], Fraction(5, 48))
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
      abjad> note.duration.multiplier = Fraction(1, 2)
      abjad> leaftools.set_preprolated_leaf_duration(note, Fraction(5, 48))
      [Note(c', 8 * 5/6)]
      abjad> f(note)
      c'8 * 5/6

   Return list of `leaf` and leaves newly tied to `leaf`.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.change_leaf_preprolated_duration( )`` to
      ``leaftools.set_preprolated_leaf_duration( )``.
   '''
   from abjad.tools import componenttools

   assert isinstance(leaf, _Leaf)
   assert isinstance(new_preprolated_duration, Fraction)

   ## If leaf carries LilyPond multiplier, change only LilyPond multiplier.
   if leaf.duration.multiplier is not None:
      leaf.duration.multiplier = new_preprolated_duration / leaf.duration.written
      return [leaf]

   ## If leaf does not carry LilyPond multiplier, change other values.
   try:
      leaf.duration.written = new_preprolated_duration  
      all_leaves = [leaf]
   except AssignabilityError:
      duration_tokens = make_notes(0, new_preprolated_duration)
      if isinstance(duration_tokens[0], _Leaf):
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = componenttools.clone_components_and_remove_all_spanners(
            [leaf], num_tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, tied_leaves)
         if not spannertools.get_all_spanners_attached_to_any_improper_parent_of_component(
            leaf, spannertools.TieSpanner):
            spannertools.TieSpanner(all_leaves)
      elif isinstance(duration_tokens[0], Tuplet):
         #print 'debug duration_tokens %s' % duration_tokens
         fmtuplet = duration_tokens[0]
         duration_tokens = fmtuplet[:]
         num_tied_leaves = len(duration_tokens) - 1
         tied_leaves = componenttools.clone_components_and_remove_all_spanners(
            [leaf], num_tied_leaves)
         all_leaves = [leaf] + tied_leaves
         for x, token in zip(all_leaves, duration_tokens):
            x.duration.written = token.duration.written
         componenttools.extend_in_parent_of_component_and_grow_spanners(leaf, tied_leaves)
         if not spannertools.is_component_with_spanner_attached(leaf, spannertools.TieSpanner):
            spannertools.TieSpanner(all_leaves) 
         tuplet_multiplier = fmtuplet.duration.multiplier
         Tuplet(tuplet_multiplier, all_leaves)
      else:
         raise ValueError('unexpected output from notetools.make_notes.')

   return all_leaves
