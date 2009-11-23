from abjad.core.abjadcore import _Abjad
from abjad.tools.pitchtools.PitchArray.PitchArrayColumn.PitchArrayColumn \
   import PitchArrayColumn
from abjad.tools.pitchtools.PitchArray.PitchArrayRow.PitchArrayRow \
   import PitchArrayRow


class PitchArray(_Abjad):
   '''.. versionadded:: 1.1.2

   Two-dimensional array of pitches.
   '''

   def __init__(self, row_count, column_count):
      self._rows = [ ]
      for i in range(row_count):
         row = PitchArrayRow(self, column_count)
         self._rows.append(row)

   ## OVERLOADS ##

   def __getitem__(self, i):
      if not isinstance(i, int):
         raise TypeError
      if not 0 <= i:
         raise ValueError
      return self.rows[i]

   def __len__(self):
      return len(self.rows)

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

   ## PUBLIC ATTRIBUTES ##

   @property
   def columns(self):
      columns = [ ]
      rows = self.rows
      for cells in zip(*self.rows):
         column = PitchArrayColumn(self, cells)
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
