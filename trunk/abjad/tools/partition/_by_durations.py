from abjad.rational.rational import Rational
from abjad.tools import check
from abjad.tools import split
from abjad.tools.split._at_duration import _at_duration as split__at_duration


def _by_durations(
   components, durations, spanners = 'unfractured', cyclic = False):
   '''Partition Python list of components according to durations.
      Interpret durations as prolated durations.
      Return list of newly split parts.'''

   check.assert_components(components)
   assert isinstance(durations, list)
   assert all([isinstance(x, (int, float, Rational)) for x in durations])

   result = [ ]

   duration_index = 0 
   len_durations = len(durations)
   part = [ ]
   cum_duration = Rational(0)

   xx = components[:]
   while True:
      #print 'xx are now %s' % xx
      try:
         if cyclic:
            next_split_point = durations[duration_index % len_durations]
         else:
            next_split_point = durations[duration_index]
      except IndexError:
         break
      try:
         x = xx.pop(0)
      except IndexError:
         break
      next_cum_duration = cum_duration + x.duration.prolated
      #print x, duration_index, cum_duration, next_split_point, next_cum_duration
      if next_cum_duration == next_split_point:
         #print 'exactly equal %s' % x
         part.append(x)
         result.append(part)
         part = [ ]
         cum_duration = Rational(0)
         duration_index += 1
      elif next_split_point < next_cum_duration:
         #print 'must split %s' % x
         local_split_duration = next_split_point - cum_duration
         #print cum_duration, next_split_point, x, part, local_split_duration
         left_list, right_list = split__at_duration(
            x, local_split_duration, spanners = spanners)
         #print 'left_list, right_list %s, %s' % (left_list, right_list)
         part.extend(left_list)
         result.append(part)
         part = [ ]
         xx[0:0] = right_list
         duration_index += 1
         cum_duration = Rational(0)
      else:
         #print 'simple append %s' % x
         part.append(x)
         cum_duration += x.duration.prolated
      #print ''

   if len(part):
      result.append(part)
   if len(xx):
      result.append(xx)
      
   return result
