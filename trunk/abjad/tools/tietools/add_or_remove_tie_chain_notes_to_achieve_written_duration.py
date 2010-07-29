from abjad.rational import Rational
from abjad.spanners import Tie
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools.spannertools._withdraw_from_attached import _withdraw_from_attached
from abjad.tools.tietools.get_tie_chain_preprolated_duration import get_tie_chain_preprolated_duration
from abjad.tools.tietools.get_leaves_in_tie_chain import get_leaves_in_tie_chain
from abjad.tools.tietools.is_tie_chain import is_tie_chain
from abjad.tools.tietools.remove_all_leaves_in_tie_chain_except_first import remove_all_leaves_in_tie_chain_except_first
from abjad.tuplet import FixedMultiplierTuplet


## TODO: Inspect tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration( ) carefully. ##
##       Determine whether behavior is correct with LilyPond multipliers. ##

def add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_written_duration):
   '''Change the written duration of tie chain,
   adding and subtracting notes as necessary.

   Return newly modified tie chain.

   .. versionchanged:: 1.1.2
      renamed ``tietools.duration_change( )`` to
      ``tietools.add_or_remove_tie_chain_notes_to_achieve_written_duration( )``.
   '''

   assert is_tie_chain(tie_chain)
   assert isinstance(new_written_duration, Rational)

   if durtools.is_assignable_rational(new_written_duration):
      tie_chain[0].duration.written = new_written_duration
      remove_all_leaves_in_tie_chain_except_first(tie_chain)
   elif durtools.is_binary_rational(new_written_duration):
      duration_tokens = leaftools.make_notes(0, [new_written_duration])
      for leaf, token in zip(tie_chain, duration_tokens):
         leaf.duration.written = token.duration.written
      if len(tie_chain) == len(duration_tokens):
         pass
      elif len(tie_chain) > len(duration_tokens):
         for leaf in tie_chain[len(duration_tokens):]:
            componenttools.remove_component_subtree_from_score_and_spanners([leaf])
      elif len(tie_chain) < len(duration_tokens):
         tie_chain[0].tie.unspan( )
         difference = len(duration_tokens) - len(tie_chain)
         extra_leaves = tie_chain[0] * difference
         _withdraw_from_attached(extra_leaves)
         extra_tokens = duration_tokens[len(tie_chain):]
         for leaf, token in zip(extra_leaves, extra_tokens):
            leaf.duration.written = token.duration.written
         if not tie_chain[-1].tie.spanned:
            Tie(list(tie_chain))
         tie_chain[-1].splice(extra_leaves)
   else:
      duration_tokens = leaftools.make_notes(0, new_written_duration)
      assert isinstance(duration_tokens[0], FixedMultiplierTuplet)
      fmtuplet = duration_tokens[0]
      new_chain_written = get_tie_chain_preprolated_duration(
         fmtuplet[0].tie.chain)
      add_or_remove_tie_chain_notes_to_achieve_written_duration(tie_chain, new_chain_written)
      multiplier = fmtuplet.duration.multiplier
      FixedMultiplierTuplet(multiplier, get_leaves_in_tie_chain(tie_chain))
      
   return tie_chain[0].tie.chain         
