from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell import \
   PitchArrayCell


class PitchArrayColumn(_Abjad):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   def __init__(self, cells):
      self._cells = [ ]
      self.extend(cells)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, PitchArrayColumn):
         for self_cell, arg_cell in zip(self.cells, arg.cells):
            if not self_cell == arg_cell:
               return False
         return True
      return False

   def __getitem__(self, arg):
      return self.cells[arg]

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

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

   @property
   def _contents_string(self):
      result = [ ]
      for cell in self.cells:
         if cell.pitch is not None:
            result.append(str(cell.pitch))
         else:
            result.append(' ')
      result = ', '.join(result)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def cells(self):
      return tuple(self._cells)

   @property
   def depth(self):
      return len(self.cells)

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

   @property
   def width(self):
      return 0 < len(self.cells)

   ## PUBLIC METHODS ##

   def append(self, cell):
      if not isinstance(cell, PitchArrayCell):
         raise TypeError('must be cell.')
      cell._row_parent = self
      self._cells.append(cell)

   def extend(self, cells):
      if not all([isinstance(cell, PitchArrayCell) for cell in cells]):
         raise TypeError('must be cells.')
      for cell in cells:
         self.append(cell)
      
   def remove_pitches(self):
      for cell in self.cells:
         cell.pitch = None

   def untie_cells(self):
      for cell in self.cells:
         cell.is_tied = None
