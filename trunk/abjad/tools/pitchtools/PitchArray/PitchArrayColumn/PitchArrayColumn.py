from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell import \
   PitchArrayCell


class PitchArrayColumn(_Abjad):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   def __init__(self, parent_array, cells):
      self._parent_array = parent_array
      self._cells = cells

   ## OVERLOADS ##

   def __repr__(self):
      pitches = self.pitches
      if self.pitches:
         result = ', '.join([str(pitch) for pitch in pitches])
      else:
         result = ' '
      return '%s(%s)' % (self.__class__.__name__, result)

   def __str__(self):
      result = [str(cell) for cell in self.cells]
      result = '\n'.join(result)
      return result

   ## PRIVATE ATTRIBUTES ##

   @property
   def _column_width(self):
      cells = self.cells
      if cells:
         return max([cell._cell_width for cell in cells])
      else:
         return 0

   ## PUBLIC ATTRIBUTES ##

   @property
   def cells(self):
      return self._cells

   @property
   def parent_array(self):
      return self._parent_array

   @property
   def pitches(self):
      pitches = [ ]
      for cell in self.cells:
         pitch = cell.pitch
         if pitch is not None:
            pitches.append(pitch)
      return pitches
