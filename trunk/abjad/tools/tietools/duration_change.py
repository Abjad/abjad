from abjad.rational import Rational
from abjad.spanners.tie import Tie
from abjad.tools import componenttools
from abjad.tools import construct
from abjad.tools import durtools
from abjad.tools.spannertools.withdraw_from_attached import \
   _withdraw_from_attached
from abjad.tools.tietools.get_duration_preprolated import \
   get_duration_preprolated as tietools_get_duration_preprolated
from abjad.tools.tietools.get_leaves import get_leaves as tietools_get_leaves
from abjad.tools.tietools.is_chain import is_chain as tietools_is_chain
from abjad.tools.tietools.truncate import truncate
from abjad.tuplet import FixedMultiplierTuplet


## TODO: Inspect tietools.duration_change( ) carefully. ##
##       Determine whether behavior is correct with LilyPond multipliers. ##

def duration_change(tie_chain, new_written_duration):
   '''Change the written duration of tie chain,
      adding and subtracting notes as necessary.

      Return newly modified tie chain.'''

   assert tietools_is_chain(tie_chain)
   assert isinstance(new_written_duration, Rational)

   if durtools.is_assignable(new_written_duration):
      tie_chain[0].duration.written = new_written_duration
      truncate(tie_chain)
   elif durtools.is_binary_rational(new_written_duration):
      duration_tokens = construct.notes(0, [new_written_duration])
      for leaf, token in zip(tie_chain, duration_tokens):
         leaf.duration.written = token.duration.written
      if len(tie_chain) == len(duration_tokens):
         pass
      elif len(tie_chain) > len(duration_tokens):
         for leaf in tie_chain[len(duration_tokens):]:
            componenttools.detach([leaf])
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
      duration_tokens = construct.notes(0, new_written_duration)
      assert isinstance(duration_tokens[0], FixedMultiplierTuplet)
      fmtuplet = duration_tokens[0]
      new_chain_written = tietools_get_duration_preprolated(
         fmtuplet[0].tie.chain)
      duration_change(tie_chain, new_chain_written)
      multiplier = fmtuplet.duration.multiplier
      FixedMultiplierTuplet(multiplier, tietools_get_leaves(tie_chain))
      
   return tie_chain[0].tie.chain         
