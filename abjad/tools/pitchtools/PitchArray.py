# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate


class PitchArray(AbjadObject):
    r'''Pitch array.

    ..  container:: example

        **Example 1.** A two-by-three pitch array:

        ::

            >>> pitch_array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(pitch_array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

        ::

            >>> print(format(pitch_array))
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

    '''

    ### INITIALIZER ###

    def __init__(self, rows=None):
        from abjad.tools import pitchtools
        self._rows = []
        self._columns = []
        if not rows:
            return
        for row in rows:
            row_ = pitchtools.PitchArrayRow([])
            for cell in row:
                if isinstance(cell, int):
                    cell = pitchtools.PitchArrayCell(width=cell)
                elif isinstance(cell, tuple):
                    assert len(cell) == 2, repr(cell)
                    pitches, width = cell
                    if isinstance(pitches, int):
                        pitches = [pitches]
                    cell = pitchtools.PitchArrayCell(
                        pitches=pitches,
                        width=width,
                        )
                row_.append(cell)
            self.append_row(row_)

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        r'''Concatenates `arg` to pitch array.

        Returns new pitch array.
        '''
        from abjad.tools import pitchtools
        if not isinstance(arg, pitchtools.PitchArray):
            message = 'must be pitch array.'
            raise TypeError(message)
        if not self.depth == arg.depth:
            message = 'array depth must match.'
            raise ValueError(message)
        new_array = pitchtools.PitchArray([])
        for self_row, arg_row in zip(self.rows, arg.rows):
            new_row = self_row + arg_row
            new_array.append_row(new_row)
        return new_array

    def __contains__(self, arg):
        r'''Is true when pitch array contains `arg`. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if isinstance(arg, pitchtools.PitchArrayRow):
            return arg in self.rows
        elif isinstance(arg, pitchtools.PitchArrayColumn):
            return arg in self.columns
        elif isinstance(arg, pitchtools.PitchArrayCell):
            return arg in self.cells
        elif isinstance(arg, pitchtools.NamedPitch):
            for pitch in self.pitches:
                if arg == pitch:
                    return True
            return False
        else:
            message = 'must be row, column, pitch or pitch cell.'
            raise ValueError(message)

    def __copy__(self):
        r'''Copies pitch array.

        Returns new pitch array.
        '''
        return type(self)(self.cell_tokens_by_row)

    def __eq__(self, arg):
        r'''Is true when `arg` is a pitch aarray with contents equal to that of
        this pitch array. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            for self_row, arg_row in zip(self.rows, arg.rows):
                if not self_row == arg_row:
                    return False
                return True
        return False

    def __getitem__(self, arg):
        r'''Gets row `arg` from pitch array.

        Returns pitch array row.
        '''
        return self.rows[arg]

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    def __hash__(self):
        r'''Hashes pitch array.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(type(self), self).__hash__()

    def __iadd__(self, arg):
        r'''Adds `arg` to pitch array in place.

            >>> array_1 = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(array_1)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

        ::

            >>> array_2 = pitchtools.PitchArray([[3, 4], [4, 3]])
            >>> print(array_2)
            [     ] [           ]
            [           ] [     ]

        ::

            >>> array_3 = pitchtools.PitchArray([[1, 1], [1, 1]])
            >>> print(array_3)
            [ ] [ ]
            [ ] [ ]

        ::

            >>> array_1 += array_2
            >>> print(array_1)
            [ ] [     ] [ ] [     ] [         ]
            [     ] [ ] [ ] [         ] [     ]

        ::

            >>> array_1 += array_3
            >>> print(array_1)
            [ ] [     ] [ ] [     ] [         ] [ ] [ ]
            [     ] [ ] [ ] [         ] [     ] [ ] [ ]

        Returns pitch array.
        '''
        if not isinstance(arg, type(self)):
            message = 'must be pitch array.'
            raise TypeError(message)
        for self_row, arg_row in zip(self.rows, arg.rows):
            self_row += arg_row
        return self

    def __ne__(self, arg):
        r'''Is true when pitch array does not equal `arg`. Otherwise false.

        Returns true or false.
        '''
        return not self == arg

    def __setitem__(self, i, arg):
        r'''Sets pitch array row `i` to `arg`.

        Retunrs none.
        '''
        from abjad.tools import pitchtools
        if isinstance(i, int):
            if not isinstance(arg, pitchtools.PitchArrayRow):
                message = 'can assign only pitch array row to pitch array.'
                raise TypeError(message)
            self._rows[i]._parent_array = None
            arg._parent_array = self
            self._rows[i] = arg
        else:
            message = 'must be integer index.'
            raise ValueError(message)

    def __str__(self):
        r'''String representation of pitch array.

        Returns string.
        '''
        return self._two_by_two_format_string

    ### PRIVATE METHODS ###

    def _column_format_width_at_index(self, index):
        columns = self.columns
        column = columns[index]
        return column._column_format_width

    def _format_cells(self, cells):
        result = [str(cell) for cell in cells]
        result = ' '.join(result)
        return result

    @staticmethod
    def _get_leaf_offsets(expr):
        from abjad.tools import scoretools
        offsets = []
        for leaf in iterate(expr).by_class(scoretools.Leaf):
            start_offset = leaf._get_timespan().start_offset
            if start_offset not in offsets:
                offsets.append(start_offset)
            stop_offset = leaf._get_timespan().stop_offset
            if stop_offset not in offsets:
                offsets.append(stop_offset)
        offsets.sort()
        return list(mathtools.difference_series(offsets))

    ### PUBLIC METHODS ###

    def append_column(self, column):
        r'''Appends `column` to pitch array.

        Returns none.
        '''
        from abjad.tools import pitchtools
        if not isinstance(column, pitchtools.PitchArrayColumn):
            message = 'must be column.'
            raise TypeError(message)
        column._parent_array = self
        column_depth = column.depth
        if self.depth < column_depth:
            self.pad_to_depth(column_depth)
        self.pad_to_width(self.width)
        for row, cell in zip(self.rows, column):
            row.append(cell)

    def append_row(self, row):
        r'''Appends `row` to pitch array.

        Returns none.
        '''
        from abjad.tools import pitchtools
        if not isinstance(row, pitchtools.PitchArrayRow):
            message = 'must be row.'
            raise TypeError(message)
        row._parent_array = self
        self._rows.append(row)

    def apply_pitches_by_row(self, pitch_lists):
        r'''Applies `pitch_lists` to pitch array by row.

        Returns none.
        '''
        for row, pitch_list in zip(self.rows, pitch_lists):
            row.apply_pitches(pitch_list)

    def copy_subarray(self, upper_left_pair, lower_right_pair):
        r'''Copies subarray of pitch array.

        Returns new pitch array.
        '''
        if not isinstance(upper_left_pair, tuple):
            raise TypeError
        if not isinstance(lower_right_pair, tuple):
            raise TypeError
        start_i, start_j = upper_left_pair
        stop_i, stop_j = lower_right_pair
        if not start_i <= stop_i:
            message = 'start row must not be greater than stop row.'
            raise ValueError(message)
        if not start_j <= stop_j:
            message = 'start column must not be greater than stop column.'
            raise ValueError(message)
        new_array = type(self)([])
        rows = self.rows
        row_indices = range(start_i, stop_i)
        for row_index in row_indices:
            new_row = rows[row_index].copy_subrow(start_j, stop_j)
            new_array.append_row(new_row)
        return new_array

    @classmethod
    def from_counts(class_, row_count, column_count):
        r'''Makes pitch array from row and column counts.

        Returns pitch array.
        '''
        from abjad.tools import pitchtools
        array = class_()
        for i in range(row_count):
            row = pitchtools.PitchArrayRow([])
            for j in range(column_count):
                cell = pitchtools.PitchArrayCell()
                row.append(cell)
            array.append_row(row)
        return array

    @classmethod
    def from_score(class_, score, populate=True):
        r'''Makes pitch array from `score`.

        ..  container:: example

            **Example 1.** Makes empty pitch array from score:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'8 d'8 e'8 f'8"))
                >>> score.append(Staff("c'4 d'4"))
                >>> score.append(
                ...     Staff(
                ...     scoretools.FixedDurationTuplet(
                ...     Duration(2, 8), "c'8 d'8 e'8") * 2))

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Staff {
                        c'4
                        d'4
                    }
                    \new Staff {
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            ::

                >>> show(score) # doctest: +SKIP

            ::

                >>> array = pitchtools.PitchArray.from_score(
                ...     score, populate=False)

            ::

                >>> print(array)
                [     ] [     ] [     ] [     ]
                [                 ] [                 ]
                [ ] [     ] [ ] [ ] [     ] [ ]

        ..  container:: example

            **Example 2.** Makes populated pitch array from `score`:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'8 d'8 e'8 f'8"))
                >>> score.append(Staff("c'4 d'4"))
                >>> score.append(
                ...     Staff(
                ...     scoretools.FixedDurationTuplet(
                ...     Duration(2, 8), "c'8 d'8 e'8") * 2))

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Staff {
                        c'4
                        d'4
                    }
                    \new Staff {
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            ::

                >>> show(score) # doctest: +SKIP

            ::

                >>> array = pitchtools.PitchArray.from_score(
                ...     score, populate=True)

            ::

                >>> print(array)
                [c'     ] [d'     ] [e'     ] [f'     ]
                [c'                   ] [d'                   ]
                [c'] [d'     ] [e'] [c'] [d'     ] [e']

        Returns pitch array.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        time_intervals = class_._get_leaf_offsets(score)
        array_width = len(time_intervals)
        array_depth = len(score)
        pitch_array = class_.from_counts(array_depth, array_width)
        items = scoretools.make_multiplied_quarter_notes([0], time_intervals)
        for leaf_iterable, pitch_array_row in zip(score, pitch_array.rows):
            durations = []
            leaves = iterate(leaf_iterable).by_class(scoretools.Leaf)
            for leaf in leaves:
                durations.append(leaf._get_duration())
            parts = mutate(items).split(
                durations,
                cyclic=False,
                fracture_spanners=False,
                )
            part_lengths = [len(part) for part in parts]
            cells = pitch_array_row.cells
            grouped_cells = sequencetools.partition_sequence_by_counts(
                cells,
                part_lengths,
                cyclic=False,
                overhang=False,
                )
            for group in grouped_cells:
                pitch_array_row.merge(group)
            leaves = iterate(leaf_iterable).by_class(scoretools.Leaf)
            if populate:
                for cell, leaf in zip(pitch_array_row.cells, leaves):
                    cell.pitches.extend(
                        pitchtools.list_named_pitches_in_expr(leaf))
        return pitch_array

    def has_spanning_cell_over_index(self, index):
        r'''Is true when pitch array has one or more spanning cells over
        `index`. Otherwise false.

        Returns true or false.
        '''
        rows = self.rows
        return any(row.has_spanning_cell_over_index(index) for row in rows)

    def list_nonspanning_subarrays(self):
        r'''Lists nonspanning subarrays of pitch array.

        ..  container:: example

            **Example 1.** Lists three nonspanning subarrays:

            ::

                >>> array = pitchtools.PitchArray([
                ...     [2, 2, 3, 1],
                ...     [1, 2, 1, 1, 2, 1],
                ...     [1, 1, 1, 1, 1, 1, 1, 1]])
                >>> print(array)
                [     ] [     ] [         ] [ ]
                [ ] [     ] [ ] [ ] [     ] [ ]
                [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

            ::

                >>> subarrays = array.list_nonspanning_subarrays()
                >>> len(subarrays)
                3

            ::

                >>> print(subarrays[0])
                [     ] [     ]
                [ ] [     ] [ ]
                [ ] [ ] [ ] [ ]

            ::

                >>> print(subarrays[1])
                [         ]
                [ ] [     ]
                [ ] [ ] [ ]

            ::

                >>> print(subarrays[2])
                [ ]
                [ ]
                [ ]

        Returns list.
        '''
        unspanned_indices = []
        for i in range(self.width + 1):
            if not self.has_spanning_cell_over_index(i):
                unspanned_indices.append(i)
        array_depth = self.depth
        subarrays = []
        for start_column, stop_column in \
            sequencetools.iterate_sequence_nwise(unspanned_indices):
            upper_left_pair = (0, start_column)
            lower_right_pair = (array_depth, stop_column)
            subarray = self.copy_subarray(upper_left_pair, lower_right_pair)
            subarrays.append(subarray)
        return subarrays

    def pad_to_depth(self, depth):
        r'''Pads pitch array to `depth`.

        Returns none.
        '''
        from abjad.tools import pitchtools
        self_depth = self.depth
        if depth < self_depth:
            message = 'pad depth must be not less than array depth.'
            raise ValueError(message)
        self_width = self.width
        missing_rows = depth - self_depth
        for i in range(missing_rows):
            row = pitchtools.PitchArrayRow([])
            row.pad_to_width(self_width)
            self.append_row(row)

    def pad_to_width(self, width):
        r'''Pads pitch array to `width`.

        Returns none.
        '''
        self_width = self.width
        if width < self_width:
            message = 'pad width must not be less than array width.'
            raise ValueError(message)
        for row in self.rows:
            row.pad_to_width(width)

    def pop_column(self, column_index):
        r'''Pops column `column_index` from pitch array.

        Returns pitch array column.
        '''
        column = self.columns[column_index]
        column._parent_array = None
        for cell in column.cells:
            cell.withdraw()
        return column

    def pop_row(self, row_index=-1):
        r'''Pops row `row_index` from pitch array.

        Returns pitch array row.
        '''
        row = self._rows.pop(row_index)
        row._parent_array = None
        return row

    def remove_row(self, row):
        r'''Removes `row` from pitch array.

        Returns none.
        '''
        if row not in self.rows:
            message = 'row not in array.'
            raise ValueError(message)
        self._rows.remove(row)
        row._parent_array = None

    def to_measures(self, cell_duration_denominator=8):
        r'''Changes pitch array  to measures.

        Makes time signatures with numerators equal to row width and
        denominators equal to `cell_duration_denominator` for each row in pitch
        array.

        ..  container:: example

            **Example 1.** Changes two-by-three pitch array to measures:

            ::

                >>> array = pitchtools.PitchArray([
                ...     [1, (2, 1), ([-2, -1.5], 2)],
                ...     [(7, 2), (6, 1), 1],
                ...     ])

            ::

                >>> print(array)
                [  ] [d'] [bf bqf    ]
                [g'     ] [fs'   ] [ ]

            ::

                >>> measures = array.to_measures()
                >>> staff = Staff(measures)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 4/8
                        r8
                        d'8
                        <bf bqf>4
                    }
                    {
                        g'4
                        fs'8
                        r8
                    }
                }

        Returns list of measures.
        '''
        measures = []
        for row in self.rows:
            measure = row.to_measure(cell_duration_denominator)
            measures.append(measure)
        return measures

    ### PRIVATE PROPERTIES ###

    @property
    def _two_by_two_format_string(self):
        return '\n'.join([str(x) for x in self.rows])

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens_by_row(self):
        r'''Gets cells tokens of pitch array by row.

        Returns tuple.
        '''
        return tuple([row.cell_tokens for row in self.rows])

    @property
    def cell_widths_by_row(self):
        r'''Gets cell widths of pitch array by row.

        Returns tuple.
        '''
        return tuple([row.cell_widths for row in self.rows])

    @property
    def cells(self):
        r'''Gets cells of pitch array.

        Returns set.
        '''
        cells = set([])
        for row in self.rows:
            cells.update(row.cells)
        return cells

    @property
    def columns(self):
        r'''Gets columns of pitch array.

        Returns tuple.
        '''
        from abjad.tools import pitchtools
        columns = []
        for i, cells in enumerate(
            sequencetools.zip_sequences(self.rows, truncate=False)):
            column = pitchtools.PitchArrayColumn(cells)
            column._parent_array = self
            column._column_index = i
            columns.append(column)
        return tuple(columns)

    @property
    def depth(self):
        r'''Gets depth of pitch array.

        Defined equal to number of pitch array rows in pitch array.

        Returns nonnegative integer.
        '''
        return len(self.rows)

    @property
    def dimensions(self):
        r'''Gets dimensions of pitch array.

        Returns pair.
        '''
        return self.depth, self.width

    @property
    def has_voice_crossing(self):
        r'''Is true when pitch array has voice crossing. Otherwise false.

        Returns true or false.
        '''
        for column in self.columns:
            if column.has_voice_crossing:
                return True
        return False

    @property
    def is_rectangular(self):
        r'''Is true when no rows in pitch array are defective. Otherwise false.

        Returns true or false.
        '''
        return all(not row.is_defective for row in self.rows)

    @property
    def pitches(self):
        r'''Gets pitches in pitch array.

        Returns tuple.
        '''
        return sequencetools.flatten_sequence(self.pitches_by_row)

    @property
    def pitches_by_row(self):
        r'''Gets pitches in pitch array by row.

        Returns tuple.
        '''
        pitches = []
        for row in self.rows:
            pitches.append(row.pitches)
        return tuple(pitches)

    @property
    def rows(self):
        r'''Gets rows in pitch array.

        Returns tuple.
        '''
        return tuple(self._rows)

    @property
    def size(self):
        r'''Gets size of pitch array.

        Defined equal to the product of depth and width.

        Returns nonnegative integer.
        '''
        return self.depth * self.width

    @property
    def voice_crossing_count(self):
        r'''Gets voice crossing count of pitch array.

        Returns nonnegative integer.
        '''
        count = 0
        for column in self.columns:
            if column.has_voice_crossing:
                count += 1
        return count

    @property
    def weight(self):
        r'''Gets weight of pitch array.

        Defined equal to the sum of the weight of the rows in pitch array.

        Returns nonnegative integer.
        '''
        return sum([row.weight for row in self.rows])

    @property
    def width(self):
        r'''Gets width of pitch array.

        Defined equal to the width of the widest row in pitch array.

        Returns nonnegative integer.
        '''
        try:
            return max([row.width for row in self.rows])
        except ValueError:
            return 0
