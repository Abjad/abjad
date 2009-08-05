from abjad.tools import check


def give_attached_to_children(donor):
   '''Give spanners attaching directly to donor to recipients.
      Usual use is to give attached spanners from parent to children,
      which is a composer-safe operation.'''

   children = donor[:]

   for spanner in list(donor.spanners.attached):
      i = spanner.index(donor)
      spanner._components[i:i+1] = children
      for child in children:
         child.spanners._add(spanner)
      donor.spanners._spanners.discard(spanner)

   return donor
