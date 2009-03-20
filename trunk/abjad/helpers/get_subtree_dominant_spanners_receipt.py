from abjad.component.component import _Component
from abjad.helpers.iterate import iterate


def _get_subtree_dominant_spanners_receipt(subtree):

   if not isinstance(subtree, _Component):
      raise TypeError('Must be Abjad component.')

   subtree_begin = subtree.offset.score
   subtree_end = subtree_begin + subtree.duration.prolated

   receipt = [ ]
   for component in iterate(subtree, _Component):
      if component.offset.score == subtree_begin:
         for spanner in component.spanners.attached:
            if spanner.begin <= subtree_begin:
               if subtree_end <= spanner.end:
                  index = spanner.index(component)
                  receipt.append((spanner, index))
      elif subtree_begin < component.offset.score:
         break

   return receipt
