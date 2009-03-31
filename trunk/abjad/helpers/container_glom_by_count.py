from abjad.container.container import Container
from abjad.helpers.container_partition_by_count \
   import container_partition_by_count
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tools import construct


## TODO: Implement container_glom_by_duration(container, durations, ...)

def container_glom_by_count(container, counts, target = Note(0, (1, 4)), 
   direction = 'big-endian'):
   '''Glom elements of container together rhythmically.
      Sum(counts) should equal len(countainer).
      Replace with material of class equal to target.

      Useful mostly during rhythmic construction.

      TODO: implement first* and last* tokens to allow counts like
               [2, 2, rest]
               [first, 2, 3]
      TODO: implement a cyclicity interface.'''

   ## assert input types
   assert isinstance(container, Container)
   assert sum(counts) == len(container)

   ## find preprolated durations of glommed parts of container
   tokens = container_partition_by_count(container, counts)
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
