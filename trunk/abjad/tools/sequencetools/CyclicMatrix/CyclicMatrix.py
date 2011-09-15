from abjad.tools.sequencetools.CyclicTuple import CyclicTuple
from abjad.tools.sequencetools.Matrix import Matrix


class CyclicMatrix(Matrix):
    '''.. versionadded:: 2.0

    Abjad model of cyclic matrix.

    Initialize from rows::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    ::

        abjad> cyclic_matrix
        CyclicMatrix(3x4)

    ::

        abjad> cyclic_matrix[2]
        CyclicTuple([20, 21, 22, 23])

    ::

        abjad> cyclic_matrix[2][2]
        22

    ::

        abjad> cyclic_matrix[99]
        CyclicTuple([0, 1, 2, 3])

    ::

        abjad> cyclic_matrix[99][99]
        3

    Initialize from columns::

        abjad> cyclic_matrix = sequencetools.CyclicMatrix(columns = [[0, 10, 20], [1, 11, 21], [2, 12, 22], [3, 13, 23]])

    ::

        abjad> cyclic_matrix
        CyclicMatrix(3x4)

    ::

        abjad> cyclic_matrix[2]
        CyclicTuple([20, 21, 22, 23])

    ::

        abjad> cyclic_matrix[2][2]
        22

    ::

        abjad> cyclic_matrix[99]
        CyclicTuple([0, 1, 2, 3])

    ::

        abjad> cyclic_matrix[99][99]
        3

    CyclicMatrix implements only item retrieval in this revision.

    Concatenation and division remain to be implemented.

    Standard transforms of linear algebra remain to be implemented.
    '''

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            assert not kwargs
            rows, columns = self._init_from_rows(args[0])
        elif 'columns' in kwargs:
            assert not args
            rows, columns = self._init_from_columns(kwargs['columns'])
        else:
            raise ValueError('can not initialize matrix.')
        self._rows = rows
        self._columns = columns
        self._n_rows = len(rows)
        self._n_columns = len(columns)

    ### OVERLOADS ###

    def __getitem__(self, expr):
        return self.rows[expr]

    def __repr__(self):
        return '%s(%sx%s)' % (type(self).__name__, self._n_rows, self._n_columns)

    ### PRIVATE METHODS ###

    def _init_from_columns(self, columns):
        columns = CyclicTuple([CyclicTuple(column) for column in columns])
        rows = []
        for row_index in range(len(columns[0])):
            row = CyclicTuple([column[row_index] for column in columns])
            rows.append(row)
        rows = CyclicTuple(rows)
        return rows, columns

    def _init_from_rows(self, rows):
        rows = CyclicTuple([CyclicTuple(row) for row in rows])
        columns = []
        for column_index in range(len(rows[0])):
            column = CyclicTuple([row[column_index] for row in rows])
            columns.append(column)
        columns = CyclicTuple(columns)
        return rows, columns

    ### PUBLIC ATTRIBUTES ###

    @property
    def columns(self):
        '''Read-only columns::

            abjad> cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

        ::

            abjad> cyclic_matrix.columns
            CyclicTuple([[0, 10, 20], [1, 11, 21], [2, 12, 22], [3, 13, 23]])

        Return cyclic tuple.
        '''
        return self._columns

    @property
    def rows(self):
        '''Read-only rows::

            abjad> cyclic_matrix = sequencetools.CyclicMatrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

        ::

            abjad> cyclic_matrix.rows
            CyclicTuple([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

        Return cyclic tuple.
        '''
        return self._rows
