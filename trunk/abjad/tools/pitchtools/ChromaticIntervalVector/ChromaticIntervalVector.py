from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.get_chromatic_intervals_in import \
   get_chromatic_intervals_in


class ChromaticIntervalVector(dict):
   '''.. versionadded:: 1.1.2

   Chromatic interval vector. ::

      abjad> staff = Staff(construct.scale(5))
      abjad> CIV = pitchtools.ChromaticIntervalVector(staff)
      abjad> CIV
      ChromaticIntervalVector(0: 0, 1: 1, 2: 3, 3: 2, 4: 1, 5: 2, 6: 0, 7: 1, 8: 0, 9: 0, 10: 0, 11: 0)
      abjad> print CIV
      0 1 3 2 1 2 0 1 0 0 0 0

   Vector is quartertone-aware. ::

      abjad> staff.append(Note(1.5, (1, 4)))
      abjad> CIV = pitchtools.ChromaticIntervalVector(staff)
      abjad> CIV
      ChromaticIntervalVector(0: 0, 0.5: 1, 1: 1, 1.5: 1, 2: 3, 2.5: 1, 3: 2, 3.5: 1, 4: 1, 4.5: 0, 5: 2, 5.5: 1, 6: 0, 6.5: 0, 7: 1, 7.5: 0, 8: 0, 8.5: 0, 9: 0, 9.5: 0, 10: 0, 10.5: 0, 11: 0, 11.5: 0)
      abjad> print CIV
      0 1 3 2 1 2 0 1 0 0 0 0
      1 1 1 1 0 1 0 0 0 0 0 0
   '''

   def __init__(self, expr):
      for interval_number in range(12):
         self[interval_number] = 0
         self[interval_number + 0.5] = 0
      for chromatic_interval in get_chromatic_intervals_in(expr):
         self[chromatic_interval.interval_number] += 1

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

   def __str__(self):
      items = self.items( )
      twelve_tone_counts = [
         item for item in items if isinstance(item[0], int)]
      twelve_tone_counts.sort( )
      twelve_tone_string = ' '.join([str(x[1]) for x in twelve_tone_counts])
      if self._has_quartertones:
         items = [item for item in items if isinstance(item[0], float)]
         items.sort( )
         quartertone_string = ' '.join([str(item[1]) for item in items])
         return '%s\n%s' % (twelve_tone_string, quartertone_string)
      return twelve_tone_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents_string(self):
      items = self.items( )
      if not self._has_quartertones:
         items = [item for item in items if isinstance(item[0], int)]
      items.sort( )
      contents_string = ['%s: %s' % item for item in items]
      contents_string = ', '.join(contents_string)
      return contents_string

   @property
   def _has_quartertones(self):
      for interval_number in range(12):
         if self[interval_number + 0.5]:
            return True
      return False
