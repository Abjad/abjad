# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.pitchtools.PitchArrayCell import PitchArrayCell


class PitchArrayColumn(AbjadValueObject):
    '''Pitch array column.

    ..  container:: example

        **Example 1.** A pitch array column:

        ::

            >>> array = pitchtools.PitchArray(
            ...     [
            ...         [1, (2, 1), (-1.5, 2)],
            ...         [(7, 2), (6, 1), 1],
            ...         ]
            ...     )

        ::

            >>> print(array)
            [  ] [d'] [bqf    ]
            [g'     ] [fs'] [ ]

        ::

            >>> print(format(array.columns[0]))
            pitchtools.PitchArrayColumn(
                cells=(
                    pitchtools.PitchArrayCell(
                        width=1,
                        ),
                    pitchtools.PitchArrayCell(
                        pitches=[
                            pitchtools.NamedPitch("g'"),
                            ],
                        width=2,
                        ),
                    ),
                )

        ::

            >>> print(array.columns[0])
            [  ]
            [g'     ]

    '''

    ### INITIALIZER ###

    def __init__(self, cells=None):
        self._cells = []
        self._column_index = None
        self._parent_array = None
        cells = cells or []
        self.extend(cells)

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a pitch array column with pitch array cells
        equal to those of this pitch array column. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, PitchArrayColumn):
            for self_cell, arg_cell in zip(self.cells, arg.cells):
                if not self_cell == arg_cell:
                    return False
            return True
        return False

    def __getitem__(self, arg):
        r'''Gets item `arg` from pitch array column.

        Returns pitch arrach cell.
        '''
        return self.cells[arg]

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    def __hash__(self):
        r'''Hashes pitch array column.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(PitchArrayColumn, self).__hash__()

    def __ne__(self, arg):
        r'''Is true when pitch array column does not equal `arg`. Otherwise
        false.

        Returns true or false.
        '''
        return not self == arg

    def __str__(self):
        r'''Gets string representation of pitch array column.

        Returns string.
        '''
        result = [str(cell) for cell in self.cells]
        result = '\n'.join(result)
        return result

    ### PRIVATE METHODS ###

    def _cells_starting_at_index(self, index):
        result = []
        for cell in self.cells:
            if cell.column_indices[0] == index:
                result.append(cell)
        result = tuple(result)
        return result

    ### PUBLIC METHODS ###

    def append(self, cell):
        r'''Appends `cell` to pitch array column.

        Returns none.
        '''
        if not isinstance(cell, PitchArrayCell):
            message = 'must be cell.'
            raise TypeError(message)
        cell._row_parent = self
        self._cells.append(cell)

    def extend(self, cells):
        r'''Extends `cells` against pitch array column.

        Returns none.
        '''
        if not all(isinstance(cell, PitchArrayCell) for cell in cells):
            message = 'must be cells.'
            raise TypeError(message)
        for cell in cells:
            self.append(cell)

    def remove_pitches(self):
        r'''Removes pitches from pitch array cells in pitch array column.

        Returns none.
        '''
        for cell in self.cells:
            cell.pitch = None

    ### PRIVATE PROPERTIES ###

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
        result = []
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
    def _start_cell_conditional_pitch_strings(self):
        result = [
            cell._conditional_pitch_string for cell in self._start_cells]
        result = tuple(result)
        return result

    @property
    def _start_cells(self):
        column_index = self.column_index
        return self._cells_starting_at_index(column_index)

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens(self):
        r'''Gets cells items of pitch array column.

        Returns tuple.
        '''
        return tuple([cell.item for cell in self.cells])

    @property
    def cell_widths(self):
        r'''Gets cell widths of pitch array column.

        Returns tuple.
        '''
        return tuple([cell.width for cell in self.cells])

    @property
    def cells(self):
        r'''Gets cells of pitch array column.

        Returns tuple.
        '''
        return tuple(self._cells)

    @property
    def column_index(self):
        r'''Gets column index of pitch array column.

        Returns nonnegative integer.
        '''
        return self._column_index

    @property
    def depth(self):
        r'''Gets depth of pitch array column.

        Defined equal to number of pitch array cells in pitch array column.

        Returns nonnegative integer.
        '''
        return len(self.cells)

    @property
    def dimensions(self):
        r'''Gets dimensions of pitch array column.

        Returns pair.
        '''
        return self.depth, self.width

    @property
    def has_voice_crossing(self):
        r'''Is true when pitch array column has voice crossing. Otherwise
        false.

        Returns true or false.
        '''
        pairs = sequencetools.iterate_sequence_nwise(self.cells)
        for upper, lower in pairs:
            lower_pitches = lower.pitches or ()
            for lower_pitch in lower_pitches:
                upper_pitches = upper.pitches or ()
                for upper_pitch in upper_pitches:
                    if upper_pitch.numbered_pitch < lower_pitch.numbered_pitch:
                        return True
        return False

    @property
    def is_defective(self):
        r'''Is true when pitch array column depth does not equal depth of
        parent
        array. Otherwise false.

        Returns true or false.
        '''
        if self.parent_array is not None:
            return not self.depth == self.parent_array.depth

    @property
    def parent_array(self):
        r'''Gets parent array that houses pitch array column.

        Returns pitch array.
        '''
        return self._parent_array

    @property
    def pitches(self):
        r'''Gets pitches in pitch array column.

        Returns tuple.
        '''
        pitches = []
        for cell in self.cells:
            pitches.extend(cell.pitches)
        return tuple(pitches)

    @property
    def start_cells(self):
        r'''Gets start cells in pitch array column.

        Returns tuple.
        '''
        start_cells = []
        column_index = self.column_index
        for cell in self.cells:
            if cell.column_indices[0] == column_index:
                start_cells.append(cell)
        return tuple(start_cells)

    @property
    def start_pitches(self):
        r'''Gets start pitches in pitch array column.

        Returns tuple.
        '''
        start_pitches = []
        for cell in self.start_cells:
            if cell.pitches is not None:
                start_pitches.extend(cell.pitches)
        return tuple(start_pitches)

    @property
    def stop_cells(self):
        r'''Gets stop cells in pitch array column.

        Returns tuple.
        '''
        start_cells = []
        column_index = self.column_index
        for cell in self.cells:
            if cell.column_indices[-1] == column_index:
                start_cells.append(cell)
        return tuple(start_cells)

    @property
    def stop_pitches(self):
        r'''Gets stop pitches in pitch array column.

        Returns tuple.
        '''
        stop_pitches = []
        for cell in self.stop_cells:
            stop_pitches.extend(cell.pitches)
        return tuple(stop_pitches)

    @property
    def weight(self):
        r'''Gets weight of pitch array column.

        Defined equal to the sum of the weight of pitch array cells in pitch
        array column.

        Returns nonnegative integer.
        '''
        return sum([cell.weight for cell in self.cells])

    @property
    def width(self):
        r'''Gets width of pitch array column.

        Defined equal to 1 when pitch array column contains cells.

        Defined equal to 0 when pitch array column contains no cells.

        Returns 1 or 0.
        '''
        if 1 <= len(self.cells):
            return 1
        else:
            return 0
