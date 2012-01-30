from abjad.core import _StrictComparator
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


class PitchArrayCell(_StrictComparator):
    '''.. versionadded 1.1.2

    One cell in a pitch array. ::

        abjad> from abjad.tools import pitcharraytools

    ::

        abjad> array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
        abjad> print array
        [ ] [     ] [ ]
        [     ] [ ] [ ]
        abjad> cell = array[0][1]
        abjad> cell
        PitchArrayCell(x2)

    ::

        abjad> cell.column_indices
        (1, 2)

    ::

        abjad> cell.indices
        (0, (1, 2))

    ::

        abjad> cell.is_first_in_row
        False

    ::

        abjad> cell.is_last_in_row
        False

    ::

        abjad> cell.next
        PitchArrayCell(x1)

    ::

        abjad> cell.parent_array
        PitchArray(PitchArrayRow(x1, x2, x1), PitchArrayRow(x2, x1, x1))

    ::

        abjad> cell.parent_column
        PitchArrayColumn(x2, x2)

    ::

        abjad> cell.parent_row
        PitchArrayRow(x1, x2, x1)

    ::

        abjad> cell.pitches
        []

    ::

        abjad> cell.prev
        PitchArrayCell(x1)

    ::

        abjad> cell.row_index
        0

    ::

        abjad> cell.token
        2

    ::

        abjad> cell.width
        2

    Return pitch array cell.
    '''

    def __init__(self, cell_token = None):
        self._parent_row = None
        self._pitches = []
        pitches, width = self._parse_cell_token(cell_token)
        self._pitches.extend(pitches)
        self._width = width

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__, self._format_pitch_width_string)

    def __str__(self):
        return self._format_string

    ### PRIVATE ATTRIBUTES ###

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
                raise ValueError('integer width token must be positive.')
        elif isinstance(cell_token, NamedChromaticPitch):
            pitches, width = [cell_token], 1
        elif isinstance(cell_token, list):
            pitch_token, width = cell_token, 1
            pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, tuple):
            if not len(cell_token) == 2:
                raise ValueError('tuple token must be of length two.')
            if isinstance(cell_token[0], str):
                pitches = self._parse_pitch_token(cell_token)
                width = 1
            else:
                pitch_token, width = cell_token
                pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, PitchArrayCell):
            pitches, width = cell_token.pitches, cell_token.width
        else:
            raise TypeError('cell token must be integer width, pitch or pair.')
        return pitches, width

    def _parse_pitch_token(self, pitch_token):
        pitches = []
        if isinstance(pitch_token, (int, float, NamedChromaticPitch)):
            pitch = NamedChromaticPitch(pitch_token)
            pitches.append(pitch)
        elif isinstance(pitch_token, tuple):
            pitches.append(NamedChromaticPitch(*pitch_token))
        elif isinstance(pitch_token, list):
            for element in pitch_token:
                pitch = NamedChromaticPitch(element)
                pitches.append(pitch)
        else:
            raise TypeError('pitch token must be number, pitch or list.')
        return pitches

    def _withdraw(self):
        parent_row = self.parent_row
        parent_row.remove(self)
        return self

    ### PUBLIC ATTRIBUTES ###

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
        raise IndexError('cell has no parent row.')

    @property
    def indices(self):
        return self.row_index, self.column_indices

    @property
    def is_first_in_row(self):
        if self.parent_row is not None:
            if self.column_indices[0] == 0:
                return True
        return False

    @property
    def is_last_in_row(self):
        if self.parent_row is not None:
            if self.column_indices[-1] == self.parent_row.width - 1:
                return True
        return False

    @property
    def next(self):
        if self.parent_row is not None:
            if self.is_last_in_row:
                raise IndexError('cell is last in row.')
            return self.parent_row[self.column_indices[-1] + 1]
        raise IndexError('cell has no parent row.')

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
    def pitches():
        def fget(self):
            for i, pitch in enumerate(self._pitches):
                if not isinstance(pitch, NamedChromaticPitch):
                    self._pitches[i] = NamedChromaticPitch(pitch)
            return self._pitches
        def fset(self, arg):
            if not isinstance(arg, (list, tuple)):
                raise TypeError('must be list or tuple of pitches.')
            self._pitches = arg
        return property(**locals())

    @property
    def prev(self):
        if self.parent_row is not None:
            if self.is_first_in_row:
                raise IndexError('cell is first in row.')
            return self.parent_row[self.column_indices[0] - 1]
        raise IndexError('cell has no parent row.')

    @property
    def row_index(self):
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.row_index
        return None

    @property
    def token(self):
        if not self.pitches:
            return self.width
        elif len(self.pitches) == 1:
            if self.width == 1:
                return str(self.pitches[0].named_chromatic_pitch_class), self.pitches[0].octave_number
            else:
                return (str(self.pitches[0].named_chromatic_pitch_class), self.pitches[0].octave_number), \
                    self.width
        else:
            if self.width == 1:
                return [(str(pitch.named_chromatic_pitch_class), pitch.octave_number) for pitch in self.pitches]
            else:
                return [
                    (str(pitch.named_chromatic_pitch_class), pitch.octave_number) for pitch in self.pitches], \
                    self.width

    @property
    def weight(self):
        return len(self.pitches)

    @property
    def width(self):
        return self._width

    ### PUBLIC METHODS ###

    def matches_cell(self, arg):
        if isinstance(arg, PitchArrayCell):
            if self.pitches == arg.pitches:
                if self.width == arg.width:
                    return True
        return False
