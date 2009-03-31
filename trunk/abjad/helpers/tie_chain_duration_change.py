from abjad.helpers.is_assignable import is_assignable
from abjad.helpers.is_binary_rational import _is_binary_rational
from abjad.helpers.is_tie_chain import _is_tie_chain
from abjad.helpers.tie_chain_truncate import tie_chain_truncate
from abjad.helpers.splice_after import splice_after
from abjad.helpers.tie_chain_written import tie_chain_written
from abjad.helpers.tie_chain_get_leaves import tie_chain_get_leaves
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners
from abjad.rational.rational import Rational
from abjad.tie.spanner import Tie
from abjad.tools import construct
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


def tie_chain_duration_change(tie_chain, new_written_duration):
   '''Change the written duration of tie chain,
      adding and subtracting notes as necessary.

      Return newly modified tie chain.'''

   assert _is_tie_chain(tie_chain)
   assert isinstance(new_written_duration, Rational)

   if is_assignable(new_written_duration):
      tie_chain[0].duration.written = new_written_duration
      tie_chain_truncate(tie_chain)
   elif _is_binary_rational(new_written_duration):
      duration_tokens = construct.notes(0, [new_written_duration])
      for leaf, token in zip(tie_chain, duration_tokens):
         leaf.duration.written = token.duration.written
      if len(tie_chain) == len(duration_tokens):
         pass
      elif len(tie_chain) > len(duration_tokens):
         for leaf in tie_chain[len(duration_tokens):]:
            leaf.detach( )
      elif len(tie_chain) < len(duration_tokens):
         tie_chain[0].tie.unspan( )
         difference = len(duration_tokens) - len(tie_chain)
         extra_leaves = tie_chain[0] * difference
         _withdraw_from_attached_spanners(extra_leaves)
         extra_tokens = duration_tokens[len(tie_chain):]
         for leaf, token in zip(extra_leaves, extra_tokens):
            leaf.duration.written = token.duration.written
         if not tie_chain[-1].tie.spanned:
            Tie(list(tie_chain))
         splice_after(tie_chain[-1], extra_leaves)
   else:
      duration_tokens = construct.notes(0, new_written_duration)
      assert isinstance(duration_tokens[0], FixedMultiplierTuplet)
      fmtuplet = duration_tokens[0]
      new_chain_written = tie_chain_written(fmtuplet[0].tie.chain)
      tie_chain_duration_change(tie_chain, new_chain_written)
      multiplier = fmtuplet.duration.multiplier
      #FixedMultiplierTuplet(multiplier, tie_chain[0].tie.spanner.leaves)
      FixedMultiplierTuplet(multiplier, tie_chain_get_leaves(tie_chain))
      
   return tie_chain[0].tie.chain         
