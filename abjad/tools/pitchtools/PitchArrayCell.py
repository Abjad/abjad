# -*- coding: utf-8 -*-
import numbers
from abjad.tools.abctools import AbjadObject


class PitchArrayCell(AbjadObject):
    '''Pitch array cell.

    ..  container:: example

        **Example 1.** A pitch array cell:

        ::

            >>> array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

        ::

            >>> cell = array[0][1]

        ::

            >>> cell
            PitchArrayCell(width=2)

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
            PitchArrayCell(width=1)

        ::

            >>> print(format(cell.parent_array))
            pitchtools.PitchArray(
                rows=(
                    pitchtools.PitchArrayRow(
                        cells=(
                            pitchtools.PitchArrayCell(
                                width=1,
                                ),
                            pitchtools.PitchArrayCell(
                                width=2,
                                ),
                            pitchtools.PitchArrayCell(
                                width=1,
                                ),
                            ),
                        ),
                    pitchtools.PitchArrayRow(
                        cells=(
                            pitchtools.PitchArrayCell(
                                width=2,
                                ),
                            pitchtools.PitchArrayCell(
                                width=1,
                                ),
                            pitchtools.PitchArrayCell(
                                width=1,
                                ),
                            ),
                        ),
                    ),
                )

        ::

            >>> print(format(cell.parent_column))
            pitchtools.PitchArrayColumn(
                cells=(
                    pitchtools.PitchArrayCell(
                        width=2,
                        ),
                    pitchtools.PitchArrayCell(
                        width=2,
                        ),
                    ),
                )

        ::

            >>> print(format(cell.parent_row))
            pitchtools.PitchArrayRow(
                cells=(
                    pitchtools.PitchArrayCell(
                        width=1,
                        ),
                    pitchtools.PitchArrayCell(
                        width=2,
                        ),
                    pitchtools.PitchArrayCell(
                        width=1,
                        ),
                    ),
                )

        ::

            >>> cell.pitches is None
            True

        ::

            >>> cell.previous
            PitchArrayCell(width=1)

        ::

            >>> cell.row_index
            0

        ::

            >>> cell.item
            2

        ::

            >>> cell.width
            2

    '''

    ### INTIALIZER ###

    def __init__(self, pitches=None, width=1):
        from abjad.tools import pitchtools
        self._pitches = None
        if pitches is not None:
            if isinstance(pitches, str):
                pitches = pitches.split()
            if isinstance(pitches, numbers.Number):
                pitches = [pitches]
            assert isinstance(pitches, (tuple, list)), repr(pitches)
            pitches = [pitchtools.NamedPitch(_) for _ in pitches]
            self._pitches = pitches
        assert isinstance(width, int), repr(width)
        assert 1 <= width, repr(width)
        self._width = width
        self._parent_row = None

    ### SPECIAL METHODS ###

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    def __str__(self):
        r'''Gets string representation of pitch array cell.

        Returns string.
        '''
        return self._format_string

    ### PRIVATE METHODS ###

    def _parse_cell_token(self, cell_token):
        from abjad.tools import pitchtools
        if cell_token is None:
            pitches, width = [], 1
        elif isinstance(cell_token, int):
            if 0 < cell_token:
                pitches, width = [], cell_token
            else:
                message = 'integer width item must be positive.'
                raise ValueError(message)
        elif isinstance(cell_token, pitchtools.NamedPitch):
            pitches, width = [cell_token], 1
        elif isinstance(cell_token, list):
            pitch_token, width = cell_token, 1
            pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, tuple):
            if not len(cell_token) == 2:
                message = 'tuple item must be of length two.'
                raise ValueError(message)
            if isinstance(cell_token[0], str):
                pitches = self._parse_pitch_token(cell_token)
                width = 1
            else:
                pitch_token, width = cell_token
                pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, type(self)):
            pitches, width = cell_token.pitches, cell_token.width
        else:
            message = 'cell item must be integer width, pitch or pair.'
            raise TypeError(message)
        return pitches, width

    def _parse_pitch_token(self, pitch_token):
        from abjad.tools import pitchtools
        pitches = []
        if isinstance(pitch_token, (int, float, pitchtools.NamedPitch)):
            pitch = pitchtools.NamedPitch(pitch_token)
            pitches.append(pitch)
        elif isinstance(pitch_token, tuple):
            pitches.append(pitchtools.NamedPitch(*pitch_token))
        elif isinstance(pitch_token, list):
            for element in pitch_token:
                pitch = pitchtools.NamedPitch(element)
                pitches.append(pitch)
        else:
            message = 'pitch item must be number, pitch or list.'
            raise TypeError(message)
        return pitches

    def _withdraw(self):
        parent_row = self.parent_row
        parent_row.remove(self)
        return self

    ### PUBLIC METHODS ###

    def append_pitch(self, pitch):
        r'''Appends `pitch` to cell.

        Returns none.
        '''
        from abjad.tools import pitchtools
        if self.pitches is None:
            self._pitches = []
        pitch = pitchtools.NamedPitch(pitch)
        self._pitches.append(pitch)

    def matches_cell(self, arg):
        r'''Is true when pitch array cell matches `arg`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            if self.pitches == arg.pitches:
                if self.width == arg.width:
                    return True
        return False

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

    ### PUBLIC PROPERTIES ###

    @property
    def column_indices(self):
        r'''Gets column start and stop indices.

        ..  container:: example

            **Example 1.** Gets column start and stop indices of cell in array:

            ::

                >>> array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> cell = array[0][1]
                >>> cell.column_indices
                (1, 2)

        ..  container:: example

            **Example 2.** Gets column start and stop indices of cell outside
            array:

            ::

                >>> cell = pitchtools.PitchArrayCell()
                >>> cell.column_indices is None
                True

        Returns tuple or none.
        '''
        if self.parent_row is not None:
            if self.width == 1:
                return (self.column_start_index,)
            elif 1 < self.width:
                return self.column_start_index, self.column_stop_index

    @property
    def column_start_index(self):
        r'''Gets column start index.

        ..  container:: example

            **Example 1.** Gets column start index of cell in array:

            ::

                >>> array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> cell = array[0][1]
                >>> cell.column_start_index
                1

        ..  container:: example

            **Example 2.** Gets column start index of cell outside array:

            ::

                >>> cell = pitchtools.PitchArrayCell()
                >>> cell.column_start_index is None
                True

        Returns nonnegative integer or none.
        '''
        if self.parent_row is None:
            return
        start_index = 0
        for cell in self.parent_row.cells:
            if cell is self:
                return start_index
            start_index += cell.width

    @property
    def column_stop_index(self):
        r'''Gets column stop index.

        ..  container:: example

            **Example 1.** Gets column stop index of cell in array:

            ::

                >>> array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> cell = array[0][1]
                >>> cell.column_stop_index
                2

        ..  container:: example

            **Example 2.** Gets column stop index of cell outside array:

            ::

                >>> cell = pitchtools.PitchArrayCell()
                >>> cell.column_stop_index is None
                True

        Returns nonnegative integer or none.
        '''
        if self.parent_row is not None:
            return self.column_start_index + self.width - 1

    @property
    def indices(self):
        r'''Gets indices.

        Returns pair.
        '''
        return self.row_index, self.column_indices

    @property
    def is_first_in_row(self):
        r'''Is true when pitch array cell is first in row. Otherwise false.

        Returns true or false.
        '''
        if self.parent_row is not None:
            if self.column_indices[0] == 0:
                return True
        return False

    @property
    def is_last_in_row(self):
        r'''Is true when pitch array cell is last in row. Otherwise false.

        Returns true or false.
        '''
        if self.parent_row is not None:
            if self.column_indices[-1] == self.parent_row.width - 1:
                return True
        return False

    @property
    def item(self):
        r'''Gets item.

        Complicated return type.
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
        r'''Gets parent array.

        Return pitch array.
        '''
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.parent_array
        return None

    @property
    def parent_column(self):
        r'''Gets parent column.

        Returns pitch array column.
        '''
        parent_array = self.parent_array
        if parent_array is not None:
            start_column_index = self.column_indices[0]
            return parent_array.columns[start_column_index]
        return None

    @property
    def parent_row(self):
        r'''Gets parent row.

        Returns pitch array row.
        '''
        return self._parent_row

    @property
    def pitches(self):
        r'''Gets and sets pitches of pitch array cell.

        Returns list.
        '''
        return self._pitches

    @pitches.setter
    def pitches(self, pitches):
        from abjad.tools import pitchtools
        if pitches is None:
            self._pitches = None
            return
        if isinstance(pitches, str):
            pitches = pitches.split()
        assert isinstance(pitches, (tuple, list)), repr(pitches)
        pitches = [pitchtools.NamedPitch(_) for _ in pitches]
        self._pitches = pitches

    @property
    def previous(self):
        r'''Gets pitch array cell in row prior to this pitch array cell.

        Returns pitch array cell.
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
        r'''Gets row index.

        Returns nonnegative integer or none.
        '''
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.row_index
        return None

    @property
    def weight(self):
        r'''Gets weight.

        Weight defined equal to number of pitches in cell.

        Returns nonnegative integer.
        '''
        return len(self.pitches)

    @property
    def width(self):
        r'''Gets width.

        Width defined equal to number of columns spanned by cell.

        Returns positive integer.
        '''
        return self._width
