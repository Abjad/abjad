from abjad.core.abjadcore import _Abjad
from abjad.pitch import Pitch
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell \
   import PitchArrayCell
from abjad.tools.pitchtools.PitchArray.PitchArrayColumn.PitchArrayColumn \
   import PitchArrayColumn
from abjad.tools.pitchtools.PitchArray.PitchArrayRow.PitchArrayRow \
   import PitchArrayRow


class PitchArray(_Abjad):
   '''.. versionadded:: 1.1.2

   Two-dimensional array of pitches.
   '''

   def __init__(self, *args):
      self._rows = [ ]
      self._columns = [ ]
      if len(args) == 2:
         if all([isinstance(arg, int) for arg in args]):
            self._init_by_counts(*args)

   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, PitchArrayRow):
         return arg in self.rows  
      elif isinstance(arg, PitchArrayColumn):
         return arg in self.columns
      elif isinstance(arg, PitchArrayCell):
         return arg in self.cells
      elif isinstance(arg, Pitch):
         for pitch in self.pitches:
            if arg == pitch:
               return True
         return False
      else:
         raise ValueError('must be row, column, pitch or pitch cell.')

   def __eq__(self, arg):
      if isinstance(arg, PitchArray):
         for self_row, arg_row in zip(self.rows, arg.rows):
            if not self_row == arg_row:
                  return False
            return True
      return False

   def __getitem__(self, arg):
      return self.rows[arg]

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      rows = self.rows
      rows = [repr(row) for row in rows]
      rows = ', '.join(rows)
      return '%s(%s)' % (self.__class__.__name__, rows)

   def __str__(self):
      return self._two_by_two_format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _two_by_two_format_string(self):
      return '\n'.join([str(x) for x in self.rows])

   ## PRIVATE METHODS ##

   def _format_cells(self, cells):
      result = [str(cell) for cell in cells]
      result = ' '.join(result)
      return result

   def _init_by_counts(self, row_count, column_count):
      for i in range(row_count):
         row = PitchArrayRow([ ])
         for j in range(column_count):
            cell = PitchArrayCell( )
            row.append(cell)
         self.append_row(row)

   ## PUBLIC ATTRIBUTES ##

   @property
   def cells(self):
      cells = set([ ])
      for row in self.rows:
         cells.update(row.cells)
      return cells

   @property
   def depth(self):
      return len(self.rows)

   @property
   def columns(self):
      columns = [ ]
      rows = self.rows
      for cells in zip(*self.rows):
         column = PitchArrayColumn(cells)
         columns.append(column)
      columns = tuple(columns)
      return columns

   @property
   def pitches(self):
      pitches = set([ ])
      for row in self.rows:
         pitches.update(row.pitches)
      return pitches

   @property
   def rows(self):
      return tuple(self._rows)

   @property
   def size(self):
      return self.depth * self.width

   @property
   def width(self):
      try:
         return max([row.width for row in self.rows])
      except ValueError:
         return 0

   ## PUBLIC METHODS ##

   def append_row(self, row):
      if not isinstance(row, PitchArrayRow):
         raise TypeError('must be row.')
      row._parent_array = self
      self._rows.append(row)

   def append_column(self, column):
      if not isinstance(column, PitchArrayColumn):
         raise TypeError('must be column.')
      column._parent_array = self
      column_depth = column.depth
      if self.depth < column_depth:
         self.pad_to_depth(column_depth)
      self.pad_to_width(self.width)
      for row, cell in zip(self.rows, column):
         row.append(cell)

   def pad_to_depth(self, depth):
      self_depth = self.depth
      if depth < self_depth:
         message = 'pad depth must be not less than array depth.'
         raise ValueError(message)
      self_width = self.width
      missing_rows = depth - self_depth
      for i in range(missing_rows):
         row = PitchArrayRow([ ])
         row.pad_to_width(self_width)
         self.append(row)

   def pad_to_width(self, width):
      self_width = self.width
      if width < self_width:
         message = 'pad width must not be less than array width.'
         raise ValueError(message)
      for row in self.rows:
         row.pad_to_width(width)

   def pop_column(self, column_index):
      column = self.columns[column_index]
      column._parent_array = None
      for cell in column.cells:
         cell.withdraw( )
      return column

   def pop_row(self, row_index):
      row = self._rows.pop(row_index)
      row._parent_array = None
      return row

#   def untie_cells(self):
#      for cell in self.cells:
#         cell.is_tied = None
