from abjad.core.abjadcore import _Abjad
from abjad.pitch import Pitch
from abjad.tools import listtools
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
      if len(args) == 1:
         if isinstance(args[0], (tuple, list)):
            #self._init_by_cell_widths_by_row(*args)
            self._init_by_cell_token_lists(*args)
      elif len(args) == 2:
         if all([isinstance(arg, int) for arg in args]):
            self._init_by_counts(*args)

   ## OVERLOADS ##

   def __add__(self, arg):
      if not isinstance(arg, PitchArray):
         raise TypeError('must be pitch array.')
      if not self.depth == arg.depth:
         raise ValueError('array depth must match.')
      new_array = PitchArray([ ])
      for self_row, arg_row in zip(self.rows, arg.rows):
         new_row = self_row + arg_row
         new_array.append_row(new_row)
      return new_array
      
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

   def __copy__(self):
      return PitchArray(self.cell_tokens_by_row)

   def __eq__(self, arg):
      if isinstance(arg, PitchArray):
         for self_row, arg_row in zip(self.rows, arg.rows):
            if not self_row == arg_row:
               return False
            return True
      return False

   def __getitem__(self, arg):
      return self.rows[arg]

   def __iadd__(self, arg):
      if not isinstance(arg, PitchArray):
         raise TypeError('must be pitch array.')
      for self_row, arg_row in zip(self.rows, arg.rows):
         self_row += arg_row
      return self

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

   def _column_format_width_at_index(self, index):
      columns = self.columns
      column = columns[index]
      return column._column_format_width

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

#   def _init_by_cell_widths_by_row(self, width_lists):
#      if 0 < len(width_lists):
#         sum_first_list = sum(width_lists[0])
#         if not all([sum(x) == sum_first_list for x in width_lists]):
#            raise ValueError('width lists must all be of same width.')
#      for width_list in width_lists:
#         row = PitchArrayRow([ ])
#         for width in width_list:
#            cell = PitchArrayCell( )
#            cell._width = width
#            row.append(cell)
#         self.append_row(row)

   def _init_by_cell_token_lists(self, cell_token_lists):
      for cell_token_list in cell_token_lists:
         row = PitchArrayRow([ ])
         for cell_token in cell_token_list:
            cell = self._parse_cell_token(cell_token)
            row.append(cell)
         self.append_row(row)

   def _parse_cell_token(self, token):
      if isinstance(token, int):
         if 0 < token:
            cell = PitchArrayCell( )
            cell._width = token
         else:
            raise ValueError('integer tokens must be positive.')
      elif isinstance(token, Pitch):
         cell = PitchArrayCell( )
         cell.pitches.append(token)
      elif isinstance(token, tuple):
         if len(token) == 2:
            pitch_token, width = token
            cell = PitchArrayCell( )
            pitches = self._parse_pitch_token(pitch_token)
            cell.pitches.extend(pitches)
            cell._width = width
         else:
            raise ValueError('tuple tokens must be of length two.')
      else:
         raise TypeError('cell token must be integer width, pitch or pair.')
      return cell

   def _parse_pitch_token(self, pitch_token):
      pitches = [ ]
      if isinstance(pitch_token, (int, float, Pitch)):
         pitch = Pitch(pitch_token)
         pitches.append(pitch)
      elif isinstance(pitch_token, tuple):
         for element in pitch_token:
            pitch = Pitch(element)
            pitches.append(pitch)
      else:
         raise TypeError('pitch token must be number, pitch or tuple.')
      return pitches
         
   ## PUBLIC ATTRIBUTES ##

   @property
   def cell_tokens_by_row(self):
      return [row.cell_tokens for row in self.rows]

   @property
   def cell_widths_by_row(self):
      return [row.cell_widths for row in self.rows]

   @property
   def cells(self):
      cells = set([ ])
      for row in self.rows:
         cells.update(row.cells)
      return cells

   @property
   def columns(self):
      columns = [ ]
      rows = self.rows
      for i, cells in enumerate(listtools.zip_nontruncating(*self.rows)):
         column = PitchArrayColumn(cells)
         column._parent_array = self
         column._column_index = i
         columns.append(column)
      columns = tuple(columns)
      return columns

   @property
   def depth(self):
      return len(self.rows)

   @property
   def dimensions(self):
      return self.depth, self.width

   @property
   def is_rectangular(self):
      return all([not row.is_defective for row in self.rows])

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

   def extract(self, upper_left_pair, lower_right_pair):
      if not isinstance(upper_left_pair, tuple):
         raise TypeError
      if not isinstance(lower_right_pair, tuple):
         raise TypeError
      start_i, start_j = upper_left_pair
      stop_i, stop_j = lower_right_pair
      if not start_i <= stop_i:
         raise ValueError('start row must not be greater than stop row.')
      if not start_j <= stop_j:
         raise ValueError('start column must not be greater than stop column.')
      new_array = PitchArray([ ])
      rows = self.rows
      row_indices = range(start_i, stop_i)
      for row_index in row_indices:
         new_row = rows[row_index].extract(start_j, stop_j)
         new_array.append_row(new_row)
      return new_array

   def has_spanning_cell_over_index(self, index):
      rows = self.rows
      return any([row.has_spanning_cell_over_index(index) for row in rows])

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
         self.append_row(row)

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

   def pop_row(self, row_index = -1):
      row = self._rows.pop(row_index)
      row._parent_array = None
      return row
