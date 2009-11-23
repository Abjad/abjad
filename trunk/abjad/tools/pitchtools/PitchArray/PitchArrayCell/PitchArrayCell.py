from abjad.core.abjadcore import _Abjad
from abjad.pitch import Pitch
import types


class PitchArrayCell(_Abjad):
   '''.. versionadded 1.1.2

   '''

   def __init__(self, parent_row):
      self._parent_row = parent_row
      self.pitch = None
      self.is_tied = False

   ## OVERLOADS ##

   def __repr__(self):
      try:
         cell_prev = self.cell_prev
         if cell_prev.is_tied:
            result = ' '
         else:
            result = '['
      except ValueError:
         result = '['
      result += self._pitch_string.center(self._column_width - 2)
      if self.is_tied:
         result += ' '
      else:
         result += ']'
      return result
       
   ## PRIVATE ATTRIBUTES ##

   @property
   def _cell_width(self):
      pitch = self.pitch
      if pitch is not None:
         return len(str(pitch)) + 2
      else:
         return 1 + 2

   @property
   def _column_width(self):
      parent_column = self.parent_column
      if parent_column is not None:
         return parent_column._column_width
      return 0

   @property
   def _format_width(self):
      return max(self._column_width, self._cell_width)

   @property
   def _is_tied_string(self):
      if self.is_tied:
         return '~'
      else:
         return ''

   @property
   def _pitch_string(self):
      pitch = self.pitch
      if pitch is not None:
         return str(pitch)
      else:
         return ''

   ## PUBLIC ATTRIBUTES ##

   @property
   def cell_above(self):
      row_index, column_index = self.indices
      return self.parent_array[row_index - 1][column_index]

   @property
   def cell_below(self):
      row_index, column_index = self.indices
      return self.parent_array[row_index + 1][column_index]

   @property
   def cell_next(self):
      return self.parent_row[self.column_index + 1]

   @property
   def cell_prev(self):
      return self.parent_row[self.column_index - 1]

   @property
   def row_index(self):
      parent_row = self.parent_row
      if parent_row is not None:
         return parent_row.row_index
      return None

   @property
   def column_index(self):
      parent_row = self.parent_row
      if parent_row is not None:
         return parent_row.index(self)
      return None

   @property
   def indices(self):
      return self.row_index, self.column_index
      
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
         return parent_array.columns[self.column_index]
      return None

   @property
   def parent_row(self):
      return self._parent_row

   @apply
   def pitch( ):
      def fget(self):
         return self._pitch
      def fset(self, arg):
         if not isinstance(arg, (Pitch, types.NoneType)):
            raise TypeError
         self._pitch = arg
      return property(**locals( ))

   @apply
   def is_tied( ):
      def fget(self):
         return self._is_tied
      def fset(self, arg):
         if not isinstance(arg, bool):
            raise TypeError
         self._is_tied = arg
      return property(**locals( ))
