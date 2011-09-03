from abjad.core import _StrictComparator
from abjad.tools.pitcharraytools.PitchArrayCell.PitchArrayCell import PitchArrayCell
from abjad.tools.pitchtools.PitchRange.PitchRange import PitchRange
import copy


class PitchArrayRow(_StrictComparator):
    '''.. versionadded:: 2.0

    One row in pitch array. ::

        abjad> from abjad.tools import pitcharraytools

    ::

        abjad> array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
        abjad> array[0].cells[0].pitches.append(0)
        abjad> array[0].cells[1].pitches.append(2)
        abjad> array[1].cells[2].pitches.append(4)
        abjad> print array
        [c'] [d'    ] [  ]
        [         ] [ ] [e']

    ::

        abjad> array[0]
        PitchArrayRow(c', d' x2, x1)

    ::

        abjad> array[0].cell_widths
        (1, 2, 1)

    ::

        abjad> array[0].dimensions
        (1, 4)

    ::

        abjad> array[0].pitches
        (NamedChromaticPitch("c'"), NamedChromaticPitch("d'"))

    Return pitch array row.
    '''

    def __init__(self, cells):
        self._parent_array = None
        self._pitch_range = PitchRange(None, None)
        self._cells = []
        self.extend(cells)

    ### OVERLOADS ###

    def __add__(self, arg):
        if not isinstance(arg, PitchArrayRow):
            raise TypeError('must be pitch array row.')
        self_copy = copy.copy(self)
        arg_copy = copy.copy(arg)
        new_row = PitchArrayRow([])
        new_row.extend(self_copy.cells)
        new_row.extend(arg_copy.cells)
        return new_row

    def __copy__(self):
        new_cells = []
        for cell in self.cells:
            new_cell = copy.copy(cell)
            new_cells.append(new_cell)
        return PitchArrayRow(new_cells)

    def __eq__(self, arg):
        if isinstance(arg, PitchArrayRow):
            for self_cell, arg_cell in zip(self.cells, arg.cells):
                if not self_cell.matches_cell(arg_cell):
                    return False
                return True
        return False

    def __getitem__(self, arg):
        if isinstance(arg, int):
            if 0 <= arg < self.width:
                accumulated_width = 0
                for cell in self.cells:
                    total_width = accumulated_width + cell.width
                    if accumulated_width <= arg < total_width:
                        return cell
                    accumulated_width = total_width
            elif 0 < abs(arg) < self.width:
                accumulated_width = 0
                abs_arg = abs(arg)
                for cell in reversed(self.cells):
                    total_width = accumulated_width + cell.width
                    if accumulated_width < abs_arg <= total_width:
                        return cell
                    accumulated_width = total_width
            else:
                raise IndexError('no such cell in row.')
        elif isinstance(arg, slice):
            cells = []
            start, stop, step = arg.indices(self.width)
            for cell_index in range(start, stop, step):
                cell = self[cell_index]
                if len(cells) == 0:
                    cells.append(cell)
                else:
                    if cells[-1] is not cell:
                        cells.append(cell)
            cells = tuple(cells)
            return cells
        else:
            raise ValueError('must be int or slice.')

    def __iadd__(self, arg):
        if not isinstance(arg, PitchArrayRow):
            raise TypeError('must be pitch array row.')
        copy_arg = copy.copy(arg)
        self.extend(copy_arg.cells)
        return self

    def __len__(self):
        return self.width

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        #return '%s(%s)' % (type(self).__name__, self._format_contents_string)
        return '%s(%s)' % (type(self).__name__, self._compact_summary)

    def __str__(self):
        result = [str(cell) for cell in self.cells]
        result = ' '.join(result)
        return result

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_summary(self):
        len_self = len(self.cells)
        if not len_self:
            return ' '
        elif 0 < len_self <= 8:
            result = [cell._format_row_column_repr_string for cell in self.cells]
            return ', '.join(result)
        else:
            left = ', '.join(
                [x._format_row_column_repr_string for x in self.cells[:2]])
            right = ', '.join(
                [x._format_row_column_repr_string for x in self.cells[-2:]])
            number_in_middle = len_self - 4
            middle = ', ... [%s] ..., '% number_in_middle
            return left + middle + right

    @property
    def _format_contents_string(self):
        result = []
        for cell in self.cells:
            result.append(cell._format_row_column_repr_string)
        result = ', '.join(result)
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def cell_tokens(self):
        return tuple([cell.token for cell in self.cells])

    @property
    def cell_widths(self):
        return tuple([cell.width for cell in self.cells])

    @property
    def cells(self):
        return tuple(self._cells)

    @property
    def depth(self):
        return 1

    @property
    def dimensions(self):
        return self.depth, self.width

    @property
    def is_defective(self):
        if self.parent_array is not None:
            return not self.width == self.parent_array.width
        return False

    @property
    def is_in_range(self):
        return all([pitch in self.pitch_range for pitch in self.pitches])

    @property
    def parent_array(self):
        return self._parent_array

    @apply
    def pitch_range():
        def fget(self):
            return self._pitch_range
        def fset(self, arg):
            if not isinstance(arg, PitchRange):
                raise TypeError('must be pitch range.')
            self._pitch_range = arg
        return property(**locals())

    @property
    def pitches(self):
        pitches = []
        for cell in self.cells:
            pitches.extend(cell.pitches)
        return tuple(pitches)

    @property
    def row_index(self):
        parent_array = self.parent_array
        if parent_array is not None:
            return parent_array._rows.index(self)
        raise IndexError('row has no parent array.')

    @property
    def weight(self):
        return sum([cell.weight for cell in self.cells])

    @property
    def width(self):
        return sum([cell.width for cell in self.cells])

    ### PUBLIC METHODS ###

    def append(self, cell_token):
        cell = PitchArrayCell(cell_token)
        cell._parent_row = self
        self._cells.append(cell)

    def apply_pitches(self, pitch_tokens):
        pitch_tokens = pitch_tokens[:]
        if pitch_tokens:
            for cell in self.cells:
                if cell.pitches:
                    cell.pitches = [pitch_tokens.pop(0)]
        else:
            self.empty_pitches()

    def copy_subrow(self, start = None, stop = None):
        arg = slice(start, stop)
        start, stop, step = arg.indices(self.width)
        if not step == 1:
            raise NotImplementedError('step not implemented.')
        column_indices = set(range(start, stop, step))
        row = PitchArrayRow([])
        cells = self[arg]
        new_cells = []
        for cell in cells:
            if not cell in new_cells:
                trim = [x for x in cell.column_indices if x not in column_indices]
                new_width = cell.width - len(trim)
                new_cell = copy.copy(cell)
                new_cell._width = new_width
                new_cells.append(new_cell)
        row.extend(new_cells)
        return row

    def empty_pitches(self):
        for cell in self.cells:
            cell.pitches = []

    def extend(self, cell_tokens):
        for cell_token in cell_tokens:
            self.append(cell_token)

    def has_spanning_cell_over_index(self, i):
        try:
            cell = self[i]
            return cell.column_indices[0] < i
        except IndexError:
            return False

    def index(self, cell):
        return self._cells.index(cell)

    def merge(self, cells):
        column_indices = []
        pitches = []
        width = 0
        for cell in cells:
            if not isinstance(cell, PitchArrayCell):
                raise TypeError
            if not cell.parent_row is self:
                raise ValueError('cells must belong to row.')
            column_indices.extend(cell.column_indices)
            pitches.extend(cell.pitches)
            width += cell.width
        start = min(column_indices)
        stop = start + len(column_indices)
        strict_series = range(start, stop)
        if not column_indices == strict_series:
            raise ValueError('cells must be contiguous.')
        first_cell = cells[0]
        for cell in cells[1:]:
            self.remove(cell)
        first_cell._pitches = pitches
        first_cell._width = width
        return first_cell

    def pad_to_width(self, width):
        self_width = self.width
        if width < self_width:
            message = 'pad width must not be less than row width.'
            raise ValueError(message)
        missing_width = width - self_width
        for i in range(missing_width):
            cell = PitchArrayCell()
            self.append(cell)

    def pop(self, cell_index):
        cell = self.pop(cell_index)
        cell._parent_row = None
        return cell

    def remove(self, cell):
        for i, x in enumerate(self.cells):
            if x is cell:
                self._cells.pop(i)
                break
        cell._parent_row = None

    def withdraw(self):
        if self.parent_array is not None:
            self.parent_array.remove_row(self)
        return self
