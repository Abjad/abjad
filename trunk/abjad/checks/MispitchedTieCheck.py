from abjad.checks._Check import _Check


class MispitchedTieCheck(_Check):

   def _run(self, expr):
      '''Check for mispitched notes.
      Do not check tied rests or skips.
      Implement chord-checking later.
      '''
      from abjad.tools import componenttools
      from abjad.tools import spannertools
      from abjad.components.Note import Note
      violators = [ ]
      total = 0
      for leaf in componenttools.iterate_components_forward_in_expr(expr, Note):
         total += 1
         #if leaf.tie.spanned and not leaf.tie.last and leaf.next:
         spanners = spannertools.get_all_spanners_attached_to_component(
            leaf, spannertools.TieSpanner)
         if spanners:
            spanner = spanners.pop( )
            if not spanner._is_my_last_leaf(leaf):
               if leaf.next:
                  if leaf.pitch != leaf.next.pitch:
                     violators.append(leaf)
      return violators, total
