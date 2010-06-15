from abjad.exceptions import PartitionError
from abjad.rational import Rational


def _group_components_by_durations(duration_type,
   components, durations, fill = 'exact', cyclic = False, overhang = False):
   '''Group *components* according to succesive *durations*.

   ``duration_type`` may be ``prolated`` or ``seconds``.
   When fill == `exact`, then parts must equal durations exactly.
   When fill == `less`, then parts must be less or equal to durations.
   When fill == `greater`, then parts must be greater or equal to durations.
   If *cyclic* is true, read *durations* cyclically.
   If *overhang* is True and components remain, append as final part.
   If *overhang* is False and components remain, do not append final part.
   '''

   assert isinstance(durations, list)
   assert all([isinstance(x, (int, float, Rational)) for x in durations])

   len_durations = len(durations)
   result = [ ]
   part = [ ]
   cur_duration_idx = 0
   target_duration = durations[cur_duration_idx]
   cum_duration = Rational(0)

   components_copy = list(components[:])
   while True:
      #print part
      try:
         component = components_copy.pop(0)
      except IndexError:
         break
      component_duration = getattr(component.duration, duration_type)
      candidate_duration = cum_duration + component_duration
      if candidate_duration < target_duration:
         #print 'not there yet'
         part.append(component)
         cum_duration = candidate_duration
      elif candidate_duration == target_duration:
         part.append(component)
         result.append(part)
         part = [ ]
         cum_duration = Rational(0)
         cur_duration_idx += 1
         target_duration = _get_next(durations, cur_duration_idx, cyclic)
      elif target_duration < candidate_duration:
         #print 'greater!'
         if fill == 'exact':
            raise PartitionError
         elif fill == 'less':
            result.append(part)
            part = [component]
            cum_duration = sum([
               getattr(x.duration, duration_type) for x in part])
            cur_duration_idx += 1
            target_duration = _get_next(durations, cur_duration_idx, cyclic)
            if target_duration is None:
               break
            if target_duration < cum_duration:
               raise PartitionError
         elif fill == 'greater':
            part.append(component)
            result.append(part)
            part = [ ]
            cum_duration = Rational(0)
            cur_duration_idx += 1
            target_duration = _get_next(durations, cur_duration_idx, cyclic)
      if target_duration is None:
         break

   if len(part):
      if overhang:
         result.append(part)

   if len(components_copy):
      if overhang:
         result.append(components_copy)

   return result
            

def _get_next(durations, cur_duration_idx, cyclic):
   try:
      if cyclic:
         return durations[cur_duration_idx % len(durations)]
      else:
         return durations[cur_duration_idx]
   except IndexError:
      return None
