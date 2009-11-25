from abjad.core.abjadcore import _Abjad
from abjad.pitch import Pitch
import types


class PitchArrayCell(_Abjad):
   '''.. versionadded 1.1.2

   '''

   def __init__(self, pitches = None):
      self._parent_row = None
      self._pitches = [ ]
      if pitches is not None:
         self.pitches.extend(pitches)
      self._width = 1

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, PitchArrayCell):
         if self.width == arg.width:
            if self.pitches == arg.pitches:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (
         self.__class__.__name__, self._format_pitch_width_string)

   def __str__(self):
      return self._format_string
       
   ## PRIVATE ATTRIBUTES ##

   @property
   def _composite_column_width(self):
      composite_column_width = 0
      columns = self.parent_array.columns
      for column_index in self.column_indices:
         composite_column_width += columns[column_index]._column_format_width
      return composite_column_width

   @property
   def _conditional_pitch_string(self):
      if self.pitches:
         return self._pitch_string
      else:
         return ' '

   @property
   def _format_row_column_repr_string(self):
      return self._format_pitch_width_string

   @property
   def _format_pitch_width_string(self):
      if self.pitches:
         if self.width == 1:
            return self._pitch_string
         else:
            return '%s %s' % (self._pitch_string, self._width_string)
      else:
         return self._width_string

   @property
   def _format_string(self):
      if self.parent_column is not None:
         if self._is_last_cell_in_row:
            cell_width = self._composite_column_width - 2
         else:
            cell_width = self._composite_column_width - 3
         return '[%s]' % self._conditional_pitch_string.ljust(cell_width)
      else:
         return '[%s]' % self._conditional_pitch_string

   @property
   def _is_last_cell_in_row(self):
      if self.parent_row is not None:
         if self.column_indices[-1] == (self.parent_row.width - 1):
            return True
         return False
      return True

   @property
   def _width_string(self):
      return 'x%s' % self.width

   @property
   def _pitch_string(self):
      if self.pitches:
         return ' '.join([str(pitch) for pitch in self.pitches])
      else:
         return ''

   ## PUBLIC ATTRIBUTES ##

   @property
   def next(self):
      return self.parent_row[self.column_indices[-1] + 1]

   @property
   def prev(self):
      prev_index = self.column_indices[0] - 1
      if prev_index < 0:
         raise ValueError
      return self.parent_row[prev_index]

   @property
   def column_indices(self):
      '''Read-only tuple of one or more nonnegative integer indices.'''
      parent_row = self.parent_row
      if parent_row is not None:
         cumulative_width = 0
         for cell in parent_row.cells:
            if cell is self:
               start = cumulative_width
               stop = start + self.width
               indices = range(start, stop)
               indices = tuple(indices)
               return indices
            cumulative_width += cell.width
      return None

   @property
   def indices(self):
      return self.row_index, self.column_indices
      
   @property
   def parent_array(self):
      parent_row = self.parent_row
      if parent_row is not None:
         return parent_row.parent_array
      return None

   @property
   def parent_column(self):
      parent_array = self.parent_array
      if parent_array is not None:
         start_column_index = self.column_indices[0]
         return parent_array.columns[start_column_index]
      return None

   @property
   def parent_row(self):
      return self._parent_row

   @apply
   def pitches( ):
      def fget(self):
         return self._pitches
      def fset(self, arg):
         if not isinstance(arg, (list, tuple)):
            raise TypeError('must be list or tuple of pitches.')
         self._pitches = arg
      return property(**locals( ))

   @property
   def row_index(self):
      parent_row = self.parent_row
      if parent_row is not None:
         return parent_row.row_index
      return None

   @property
   def width(self):
      return self._width

   ## PUBLIC METHODS ##

   def withdraw(self):
      parent_row = self.parent_row
      parent_row.remove(self)
      return self
