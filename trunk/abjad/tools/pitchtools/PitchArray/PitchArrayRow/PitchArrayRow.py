from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell import \
   PitchArrayCell


class PitchArrayRow(_Abjad):
   '''.. versionadded:: 1.1.2

   Docs.
   '''

   def __init__(self, cells):
      self._cells = [ ]
      self.extend(cells)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, PitchArrayRow):
         for self_cell, arg_cell in zip(self.cells, arg.cells):
            if not self_cell == arg_cell:
               return False
            return True
      return False

   def __getitem__(self, arg):
      if isinstance(arg, int):
         if 0 <= arg:
            accumulated_width = 0
            for cell in self.cells:
               total_width = accumulated_width + cell.width
               if accumulated_width <= arg < total_width:
                  return cell
               accumulated_width = total_width
         else:
            accumulated_width = 0
            abs_arg = abs(arg)
            for cell in reversed(self.cells):
               total_width = accumulated_width + cell.width
               if accumulated_width < abs_arg <= total_width:
                  return cell
               accumulated_width = total_width
      elif isinstance(arg, slice):
         cells = [ ]
         start, stop, step = arg.start, arg.stop, step
         for cell_index in range(start, stop, step):
            cell = self[cell_index]
            if cell not in cells:
               cells.append(cell)
         cells = tuple(cells)
         return cells
      else:
         raise ValueError('must be int or slice.')

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._contents_string)

   def __str__(self):
      result = [str(x) for x in self]
      result = ' '.join(result)
      return result

   ## PRIVATE ATTRIBUTES ##

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
      return 1

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

   @property
   def row_index(self):
      parent_array = self.parent_array
      if parent_array is not None:
         return parent_array._rows.index(self)
      return None

   @property
   def width(self):
      return sum([cell.width for cell in self.cells])

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

   def index(self, cell):
      return self._cells.index(cell)

   def pad_to_width(self, width):
      self_width = self.width
      if width < self_width:
         message = 'pad width must not be less than row width.'
         raise ValueError(message)
      missing_width = width = self_width
      for i in range(missing_width):
         cell = PitchArrayCell( )
         self.append(cell)
      return self

   def pop(self, cell_index):
      cell = self.pop(cell_index)
      cell._parent_row = None
      return cell
  
   def remove(self, cell):
      self._cells.remove(cell)
      cell._parent_row = None

   def set_pitches_to_none(self):
      for cell in self.cells:
         cell.pitch = None

   def untie_cells(self):
      for cell in self.cells:
         cell.is_tied = None
