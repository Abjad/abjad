from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell import \
   PitchArrayCell


class PitchArrayRow(list):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   def __init__(self, parent_array, length):
      self._parent_array = parent_array
      for i in range(length):
         self.append(PitchArrayCell(self))

   ## OVERLOADS ##

   def __repr__(self):
      pitches = ', '.join([str(x) for x in self.pitches])
      return '%s(%s)' % (self.__class__.__name__, pitches)

   def __str__(self):
      result = [str(x) for x in self]
      result = ' '.join(result)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def row_index(self):
      parent_array = self.parent_array
      if parent_array is not None:
         return parent_array._rows.index(self)
      return None

   @property
   def parent_array(self):
      return self._parent_array

   @property
   def pitches(self):
      pitches = [ ]
      for cell in self:
         pitch = cell.pitch
         if pitch is not None:
            pitches.append(pitch)
      return tuple(pitches)
