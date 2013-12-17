# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
from abjad.tools.pitchtools.NamedPitch import NamedPitch


class PitchArrayCell(AbjadObject):
    '''One cell in a pitch array.

    ::

        >>> array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
        >>> print array
        [ ] [     ] [ ]
        [     ] [ ] [ ]
        >>> cell = array[0][1]
        >>> cell
        PitchArrayCell(x2)

    ::

        >>> cell.column_indices
        (1, 2)

    ::

        >>> cell.indices
        (0, (1, 2))

    ::

        >>> cell.is_first_in_row
        False

    ::

        >>> cell.is_last_in_row
        False

    ::

        >>> cell.next
        PitchArrayCell(x1)

    ::

        >>> cell.parent_array
        PitchArray(PitchArrayRow(x1, x2, x1), PitchArrayRow(x2, x1, x1))

    ::

        >>> cell.parent_column
        PitchArrayColumn(x2, x2)

    ::

        >>> cell.parent_row
        PitchArrayRow(x1, x2, x1)

    ::

        >>> cell.pitches
        []

    ::

        >>> cell.previous
        PitchArrayCell(x1)

    ::

        >>> cell.row_index
        0

    ::

        >>> cell.token
        2

    ::

        >>> cell.width
        2

    '''

    ### INTIALIZER ###

    def __init__(self, cell_token=None):
        self._parent_row = None
        self._pitches = []
        pitches, width = self._parse_cell_token(cell_token)
        self._pitches.extend(pitches)
        self._width = width

    ### SPECIAL METHODS ###

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    def __repr__(self):
        r'''Gets interpreter representation of pitch array cell.

        Returns string.
        '''
        return '{}({})'.format(
            type(self).__name__, 
            self._format_pitch_width_string,
            )

    def __str__(self):
        r'''String representation of pitch array cell.

        Returns string.
        '''
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _composite_column_width(self):
        composite_column_width = 0
        columns = self.parent_array.columns
        for column_index in self.column_indices:
            composite_column_width += \
                columns[column_index]._column_format_width
        return composite_column_width

    @property
    def _conditional_pitch_string(self):
        if self.pitches:
            return self._pitch_string
        else:
            return ' '

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
    def _format_row_column_repr_string(self):
        return self._format_pitch_width_string

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
    def _pitch_string(self):
        if self.pitches:
            return ' '.join([str(pitch) for pitch in self.pitches])
        else:
            return ''

    @property
    def _width_string(self):
        return 'x%s' % self.width

    ### PRIVATE METHODS ###

    def _parse_cell_token(self, cell_token):
        if cell_token is None:
            pitches, width = [], 1
        elif isinstance(cell_token, int):
            if 0 < cell_token:
                pitches, width = [], cell_token
            else:
                message = 'integer width token must be positive.'
                raise ValueError(message)
        elif isinstance(cell_token, NamedPitch):
            pitches, width = [cell_token], 1
        elif isinstance(cell_token, list):
            pitch_token, width = cell_token, 1
            pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, tuple):
            if not len(cell_token) == 2:
                message = 'tuple token must be of length two.'
                raise ValueError(message)
            if isinstance(cell_token[0], str):
                pitches = self._parse_pitch_token(cell_token)
                width = 1
            else:
                pitch_token, width = cell_token
                pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, PitchArrayCell):
            pitches, width = cell_token.pitches, cell_token.width
        else:
            message = 'cell token must be integer width, pitch or pair.'
            raise TypeError(message)
        return pitches, width

    def _parse_pitch_token(self, pitch_token):
        pitches = []
        if isinstance(pitch_token, (int, float, NamedPitch)):
            pitch = NamedPitch(pitch_token)
            pitches.append(pitch)
        elif isinstance(pitch_token, tuple):
            pitches.append(NamedPitch(*pitch_token))
        elif isinstance(pitch_token, list):
            for element in pitch_token:
                pitch = NamedPitch(element)
                pitches.append(pitch)
        else:
            message = 'pitch token must be number, pitch or list.'
            raise TypeError(message)
        return pitches

    def _withdraw(self):
        parent_row = self.parent_row
        parent_row.remove(self)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def column_indices(self):
        r'''Tuple of one or more nonnegative integer indices.

        Returns tuple.
        '''
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
        message = 'cell has no parent row.'
        raise IndexError(message)

    @property
    def indices(self):
        r'''Indices of pitch array cell.

        Returns pair.
        '''
        return self.row_index, self.column_indices

    @property
    def is_first_in_row(self):
        r'''True when pitch array cell is first in row. Otherwise false.

        Returns boolean.
        '''
        if self.parent_row is not None:
            if self.column_indices[0] == 0:
                return True
        return False

    @property
    def is_last_in_row(self):
        r'''True when pitch array cell is last in row. Otherwise false.

        Returns boolean.
        '''
        if self.parent_row is not None:
            if self.column_indices[-1] == self.parent_row.width - 1:
                return True
        return False

    @property
    def next(self):
        r'''Gets next pitch array cell in row after this pitch array cell.

        Returns pitch array cell.
        '''
        if self.parent_row is not None:
            if self.is_last_in_row:
                message = 'cell is last in row.'
                raise IndexError(message)
            return self.parent_row[self.column_indices[-1] + 1]
        message = 'cell has no parent row.'
        raise IndexError(message)

    @property
    def parent_array(self):
        r'''Gets pitch array that houses pitch array cell.

        Return pitch array.
        '''
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.parent_array
        return None

    @property
    def parent_column(self):
        r'''Gets column that houses pitch array cell.

        Returns pitch array column.
        '''
        parent_array = self.parent_array
        if parent_array is not None:
            start_column_index = self.column_indices[0]
            return parent_array.columns[start_column_index]
        return None

    @property
    def parent_row(self):
        r'''Gets pitch array rown that houses pitch array cell.

        Returns pitch array row.
        '''
        return self._parent_row

    @property
    def pitches(self):
        r'''Gets and sets pitches of pitch array cell.

        Returns list.
        '''
        for i, pitch in enumerate(self._pitches):
            if not isinstance(pitch, NamedPitch):
                self._pitches[i] = NamedPitch(pitch)
        return self._pitches

    @pitches.setter
    def pitches(self, arg):
        if not isinstance(arg, (list, tuple)):
            message = 'must be list or tuple of pitches.'
            raise TypeError(message)
        self._pitches = arg

    @property
    def previous(self):
        r'''Gets pitch array cell in row prior to this pitch array cell.

        Returns pitch arracy cell.
        '''
        if self.parent_row is not None:
            if self.is_first_in_row:
                message = 'cell is first in row.'
                raise IndexError(message)
            return self.parent_row[self.column_indices[0] - 1]
        message = 'cell has no parent row.'
        raise IndexError(message)

    @property
    def row_index(self):
        r'''Row index of pitch array cell.

        Returns nonnegative integer or none.
        '''
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.row_index
        return None

    @property
    def token(self):
        r'''Token of pitch array cell.
        '''
        if not self.pitches:
            return self.width
        elif len(self.pitches) == 1:
            if self.width == 1:
                return (
                    str(self.pitches[0].named_pitch_class), 
                    self.pitches[0].octave_number,
                    )
            else:
                return (
                    str(self.pitches[0].named_pitch_class), 
                    self.pitches[0].octave_number,
                    self.width,
                    )
        else:
            if self.width == 1:
                return [(str(pitch.named_pitch_class), 
                    pitch.octave_number) 
                    for pitch in self.pitches]
            else:
                return (
                    [(str(pitch.named_pitch_class), 
                    pitch.octave_number) for pitch in self.pitches],
                    self.width
                    )

    @property
    def weight(self):
        r'''Weight of pitch array cell.

        Defined equal to number of pitches in pitch array cell.

        Returns nonnegative integer.
        '''
        return len(self.pitches)

    @property
    def width(self):
        r'''Width of pitch array cell.

        Returns positive integer.
        '''
        return self._width

    ### PUBLIC METHODS ###

    def matches_cell(self, arg):
        r'''True when pitch array cell matches `arg`. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, PitchArrayCell):
            if self.pitches == arg.pitches:
                if self.width == arg.width:
                    return True
        return False
