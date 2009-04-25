from abjad.container.container import Container
from abjad.tools import iterate
from abjad.tools.fuse.measures_by_reference import measures_by_reference


def measures_by_count_cyclic(container, part_counts, mark = False):
   '''Iterate measures in 'container'.
      Fuse according to positive integer parts in 'part_counts'.'''

   assert isinstance(container, Container)
   assert isinstance(part_counts, (tuple, list))

   try:
      if not container._update._current:
         container._update._updateAll( )
      container._update._forbidUpdate( )
      len_parts = len(part_counts)
      part_index = 0
      cur_measure = iterate.measure_next(container)
      while True:
         part_count = part_counts[part_index % len_parts]
         if 1 < part_count:
            measures_to_fuse = [ ]
            measure_to_fuse = cur_measure
            for x in range(part_count):
               measures_to_fuse.append(measure_to_fuse)
               try:
                  measure_to_fuse = iterate.measure_next(measure_to_fuse)
               except StopIteration:
                  break
            meter_sum_str = ' + '.join([
               str(x.meter.effective) for x in measures_to_fuse])
            new = measures_by_reference(measures_to_fuse)
            if mark:
               new.leaves[0].markup.up.append(meter_sum_str)
            cur_measure = new
         try:
            cur_measure = iterate.measure_next(cur_measure)
         except StopIteration:
            break
         part_index += 1 
   finally:
      container._update._allowUpdate( )
