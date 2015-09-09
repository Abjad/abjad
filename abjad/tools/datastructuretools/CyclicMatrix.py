# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.Matrix import Matrix


# TODO: change CyclicMatrix(columns=[...]) to CyclicMatrix.from_columns(...)
class CyclicMatrix(Matrix):
    '''A cyclic matrix.

    Initializes from rows:

    ::

        >>> cyclic_matrix = datastructuretools.CyclicMatrix([
        ...     [0, 1, 2, 3],
        ...     [10, 11, 12, 13],
        ...     [20, 21, 22, 23],
        ...     ])

    ::

        >>> cyclic_matrix
        CyclicMatrix(3x4)

    ::

        >>> cyclic_matrix[2]
        CyclicTuple([20, 21, 22, 23])

    ::

        >>> cyclic_matrix[2][2]
        22

    ::

        >>> cyclic_matrix[99]
        CyclicTuple([0, 1, 2, 3])

    ::

        >>> cyclic_matrix[99][99]
        3

    Initializes from columns:

    ::

        >>> cyclic_matrix = datastructuretools.CyclicMatrix(columns=[
        ...     [0, 10, 20],
        ...     [1, 11, 21],
        ...     [2, 12, 22],
        ...     [3, 13, 23],
        ...     ])

    ::

        >>> cyclic_matrix
        CyclicMatrix(3x4)

    ::

        >>> cyclic_matrix[2]
        CyclicTuple([20, 21, 22, 23])

    ::

        >>> cyclic_matrix[2][2]
        22

    ::

        >>> cyclic_matrix[99]
        CyclicTuple([0, 1, 2, 3])

    ::

        >>> cyclic_matrix[99][99]
        3

    Only item retrieval is currently implemented.

    Concatenation and division remain to be implemented.

    Standard transforms of linear algebra remain to be implemented.
    '''

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            assert not kwargs
            rows, columns = self._initialize_from_rows(args[0])
        elif 'columns' in kwargs:
            assert not args
            rows, columns = self._initialize_from_columns(kwargs['columns'])
        elif len(args) == 0:
            rows, columns = self._initialize_from_rows([[0],[0]])
        else:
            message = 'can not initialize {}: {!r}.'
            message = message(type(self).__name__, args)
            raise ValueError(message)
        self._rows = rows
        self._columns = columns
        self._n_rows = len(rows)
        self._n_columns = len(columns)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r'''Gets row `i` from cyclic matrix.

        Returns row.
        '''
        return self.rows[i]

    def __repr__(self):
        r'''Gets interpreter representation of cyclic matrix.

        Returns string.
        '''
        return '{}({}x{})'.format(
            type(self).__name__,
            self._n_rows,
            self._n_columns,
            )

    ### PRIVATE METHODS ###

    def _initialize_from_columns(self, columns):
        from abjad.tools import datastructuretools
        columns = datastructuretools.CyclicTuple([
            datastructuretools.CyclicTuple(column)
            for column in columns
            ])
        rows = []
        for row_index in range(len(columns[0])):
            row = datastructuretools.CyclicTuple([
                column[row_index] for column in columns
                ])
            rows.append(row)
        rows = datastructuretools.CyclicTuple(rows)
        return rows, columns

    def _initialize_from_rows(self, rows):
        from abjad.tools import datastructuretools
        rows = datastructuretools.CyclicTuple([
            datastructuretools.CyclicTuple(row) for row in rows
            ])
        columns = []
        for column_index in range(len(rows[0])):
            column = datastructuretools.CyclicTuple([
                row[column_index] for row in rows
                ])
            columns.append(column)
        columns = datastructuretools.CyclicTuple(columns)
        return rows, columns

    ### PUBLIC PROPERTIES ###

    @property
    def columns(self):
        r'''Columns of cyclic matrix.

        ::

            >>> cyclic_matrix = datastructuretools.CyclicMatrix([
            ...     [0, 1, 2, 3],
            ...     [10, 11, 12, 13],
            ...     [20, 21, 22, 23],
            ...     ])

        ::

            >>> print(format(cyclic_matrix.columns))
            datastructuretools.CyclicTuple(
                [
                    datastructuretools.CyclicTuple(
                        [0, 10, 20]
                        ),
                    datastructuretools.CyclicTuple(
                        [1, 11, 21]
                        ),
                    datastructuretools.CyclicTuple(
                        [2, 12, 22]
                        ),
                    datastructuretools.CyclicTuple(
                        [3, 13, 23]
                        ),
                    ]
                )

        Returns cyclic tuple.
        '''
        return self._columns

    @property
    def rows(self):
        r'''Rows of cyclic matrix.

        ::

            >>> cyclic_matrix = datastructuretools.CyclicMatrix([
            ...     [0, 1, 2, 3],
            ...     [10, 11, 12, 13],
            ...     [20, 21, 22, 23],
            ...     ])

        ::

            >>> print(format(cyclic_matrix.rows))
            datastructuretools.CyclicTuple(
                [
                    datastructuretools.CyclicTuple(
                        [0, 1, 2, 3]
                        ),
                    datastructuretools.CyclicTuple(
                        [10, 11, 12, 13]
                        ),
                    datastructuretools.CyclicTuple(
                        [20, 21, 22, 23]
                        ),
                    ]
                )

        Returns cyclic tuple.
        '''
        return self._rows
