from abjad.container import Container
from abjad.tools import iterate
from abjad.tools.fuse.measures_by_reference import measures_by_reference


def measures_by_counts_cyclic(container, part_counts, mark = False):
   r'''Fuse `container` measures cyclically by `part_counts`::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 5)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 2/8
            e'8
            f'8
         }
         {
            \time 2/8
            g'8
            a'8
         }
         {
            \time 2/8
            b'8
            c''8
         }
         {
            \time 2/8
            d''8
            e''8
         }
      }
      
   ::
      
      abjad> part_counts = (2, 1)
      abjad> fuse.measures_by_counts_cyclic(staff, part_counts)
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
         }
         {
            \time 2/8
            g'8
            a'8
         }
         {
            \time 4/8
            b'8
            c''8
            d''8
            e''8
         }
      }

   Return none.

   Set `mark` to true to mark fused measures for later reference.

   .. todo:: rename `part_counts` to `counts`.
   '''

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
         #print cur_measure, part_count
         if 1 < part_count:
            measures_to_fuse = [ ]
            measure_to_fuse = cur_measure
            for x in range(part_count):
               measures_to_fuse.append(measure_to_fuse)
               measure_to_fuse = iterate.measure_next(measure_to_fuse)
               if measure_to_fuse is None:
                  break
            meter_sum_str = ' + '.join([
               str(x.meter.effective) for x in measures_to_fuse])
            meter_sum_str = '"%s"' % meter_sum_str
            new = measures_by_reference(measures_to_fuse)
            if mark:
               new.leaves[0].markup.up.append(meter_sum_str)
            cur_measure = new
         cur_measure = iterate.measure_next(cur_measure)
         if cur_measure is None:
            break
         part_index += 1 
   finally:
      container._update._allowUpdate( )
