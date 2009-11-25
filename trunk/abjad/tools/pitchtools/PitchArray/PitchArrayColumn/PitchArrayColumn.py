from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell import \
   PitchArrayCell


class PitchArrayColumn(_Abjad):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   def __init__(self, cells):
      self._cells = [ ]
      self._column_index = None
      self._parent_array = None
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
      return '%s(%s)' % (self.__class__.__name__, self._format_contents_string)

   def __str__(self):
      result = [str(cell) for cell in self.cells]
      result = '\n'.join(result)
      return result

   ## PRIVATE ATTRIBUTES ##

   @property
   def _column_format_max_string_width(self):
      strings = self._start_cell_conditional_pitch_strings
      if strings:
         return max([len(string) for string in strings])
      else:
         return 0

   @property
   def _column_format_width(self):
      format_width = 0
      if self._has_closed_cell_on_left:
         format_width += 1
      max_string_width = self._column_format_max_string_width
      format_width += max_string_width
      if self._has_closed_cell_on_right:
         format_width += 1
      if not self._is_last_column_in_array:
         format_width += 1 
      return format_width

   @property
   def _format_contents_string(self):
      result = [ ]
      for cell in self.cells:
         result.append(cell._format_row_column_repr_string)
      result = ', '.join(result)
      return result

   @property
   def _has_closed_cell_on_left(self):
      if self.column_index is not None:
         for cell in self.cells:
            if cell.column_indices[0] == self.column_index:
               return True
         return False
      return True

   @property
   def _has_closed_cell_on_right(self):
      if self.column_index is not None:
         for cell in self.cells:
            if cell.column_indices[-1] == self.column_index:
               return True
         return True
      return True

   @property
   def _is_last_column_in_array(self):
      if self.parent_array is not None:
         if self.column_index == (self.parent_array.width - 1):
            return True
      return False

   @property
   def _start_cells(self):
      column_index = self.column_index
      return self._cells_starting_at_index(column_index)

   @property
   def _start_cell_conditional_pitch_strings(self):
      result = [
         cell._conditional_pitch_string for cell in self._start_cells]
      result = tuple(result)
      return result


   ## PRIVATE METHODS ##
   
   def _cells_starting_at_index(self, index):
      result = [ ]
      for cell in self.cells:
         if cell.column_indices[0] == index:
            result.append(cell)
      result = tuple(result)
      return result


   ## PUBLIC ATTRIBUTES ##

   @property
   def cells(self):
      return tuple(self._cells)

   @property
   def column_index(self):
      return self._column_index

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
      pitches = tuple(pitches)
      return pitches

   @property
   def width(self):
      if 1 <= len(self.cells):
         return 1
      else:
         return 0

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
