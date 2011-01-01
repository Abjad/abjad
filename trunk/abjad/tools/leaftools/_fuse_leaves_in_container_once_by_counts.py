from abjad.components.Container import Container
from abjad.components import Note
from abjad.components import Rest


def _fuse_leaves_in_container_once_by_counts(container, counts, target_type = Note, 
   direction = 'big-endian'):
   '''Fuse leaves in `container` once by `counts` into `direction`-oriented
   instances of `target_type`.
   '''
   from abjad.tools import componenttools
   from abjad.tools import notetools
   from abjad.tools import resttools

   ## assert input types
   assert isinstance(container, Container)

   ## assert input values
   if not sum(counts) == len(container):
      raise ValueError('sum of counts must equal length of container.')

   ## find preprolated durations of glommed parts of container
   tokens = componenttools.clone_and_partition_governed_component_subtree_by_leaf_counts(
      container, counts)
   durations = [sum([x.duration.preprolated for x in part]) for part in tokens]

   ## construct new notes or rests
   if target_type == Note:
      new_material = notetools.make_notes(0, durations, direction = direction)
   elif target_type == Rest:
      new_material = resttools.make_rests(durations, direction = direction)
   else:
      raise ValueError('unknown type of material to construct.')

   ## insert new material in container
   container[:] = new_material

   ## return container
   return container
