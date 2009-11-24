from abjad.core.abjadcore import _Abjad
from abjad.pitch import Pitch
import types


class PitchArrayCell(_Abjad):
   '''.. versionadded 1.1.2

   '''

   def __init__(self, pitch = None):
      self._parent_row = None
      self.pitch = pitch
      self.width = 1

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, PitchArrayCell):
         if self.width == arg.width:
            if self.pitch == arg.pitch:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      pitch_string = self._pitch_string
      if pitch_string == '':
         pitch_string = ' '
      width = self.width
      if width == 1:
         width_string = ''
      else:
         width_string = ' x %s' % width
      return '%s(%s%s)' % (self.__class__.__name__, pitch_string, width_string)

   def __str__(self):
      if self.parent_row is None:
         return self._format_string_orphan
      else:
         return self._format_string_total
       
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string_head(self):
      pitch = self.pitch
      if pitch is not None:
         return str(pitch)
      else:
         return ' '

   @property
   def _format_string_orphan(self):
      self_width = self.width
      if self_width == 1:
         width_string = ''
      else:
         width_string = ' x %s' % self_width
      return '%s%s' % (self._format_string_head, width_string)

   @property
   def _format_string_total(self):
      ## TODO ##
      head = self._format_string_head
      return '[%s]' % head.ljust(2 * self.width)

   @property
   def _pitch_count_string(self):
      if self.width == 1:
         return self._pitch_string
      else:
         return 

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
      cell_prev_index = self.column_index - 1
      if cell_prev_index < 0:
         raise ValueError
      return self.parent_row[cell_prev_index]

   @property
   def column_indices(self):
      '''Read-only integer pair.'''
      parent_row = self.parent_row
      if parent_row is not None:
         cumulative_width = 0
         for cell in parent_row.cells:
            if cell is self:
               return cumulative_width, cumulative_width + self.width
            cumulative_width += cell.width
      return None

   @property
   def indices(self):
      return self.row_index, self.column_index
      
#   @apply
#   def is_tied( ):
#      def fget(self):
#         return self._is_tied
#      def fset(self, arg):
#         if not isinstance(arg, (bool, types.NoneType)):
#            raise TypeError
#         self._is_tied = arg
#      return property(**locals( ))

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

   @property
   def pitch_effective(self):
      pitch = self.pitch
      if pitch is not None:
         return pitch
      try:
         cell_prev = self.cell_prev
      except IndexError:
         return None
      if cell_prev.is_tied:
         return cell_prev.pitch_effective
      else:
         return None

   @property
   def row_index(self):
      parent_row = self.parent_row
      if parent_row is not None:
         return parent_row.index(self)
      return None

   @apply
   def width( ):
      def fget(self):
         return self._width
      def fset(self, arg):
         if not isinstance(arg, int):
            raise TypeError
         if not 0 < arg:
            raise ValueError
         self._width = arg
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def withdraw(self):
      parent_row = self.parent_row
      parent_row.remove(self)
      return self
