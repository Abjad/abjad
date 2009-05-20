from abjad.container.container import Container
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tools import clonewp
from abjad.tools import construct


## TODO: Implement fuse.contents_by_duration(container, durations, ...)
## TODO: Implement fuse.components_by_duration(container, durations, ...)
## TODO: Implement fuse.comopnents_by_count(container, durations, ...)

def contents_by_count(container, counts, target = Note(0, (1, 4)), 
   direction = 'big-endian'):
   '''Glom elements of `container` together rhythmically.

      ``sum(counts)`` should equal ``len(countainer)``.
      Replace with material of class equal to ``target``.

      Useful mostly during rhythmic construction.'''

   ## assert input types
   assert isinstance(container, Container)
   assert sum(counts) == len(container)

   ## find preprolated durations of glommed parts of container
   tokens = clonewp.by_leaf_counts_with_parentage(container, counts)
   durations = [sum([x.duration.preprolated for x in part]) for part in tokens]

   ## construct new notes or rests
   if isinstance(target, Note):
      new_material = construct.notes(
         0, durations, direction = direction)
   elif isinstance(target, Rest):
      new_material = construct.rests(
         durations, direction = direction)
   else:
      raise ValueError('unknown type of material to construct.')

   ## insert new material in container
   container[:] = new_material

   ## return container
   return container
