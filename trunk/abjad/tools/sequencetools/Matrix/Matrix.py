class Matrix(object):
    '''.. versionadded:: 2.0

    Abjad model of matrix.

    Initialize from rows::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> matrix = sequencetools.Matrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

    ::

        abjad> matrix
        Matrix(3x4)

    ::

        abjad> matrix[:]
        ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))

    ::

        abjad> matrix[2]
        (20, 21, 22, 23)

    ::

        abjad> matrix[2][0]
        20

    Initialize from columns::

        abjad> matrix = sequencetools.Matrix(columns = [[0, 10, 20], [1, 11, 21], [2, 12, 22], [3, 13, 23]])

    ::

        abjad> matrix
        Matrix(3x4)

    ::

        abjad> matrix[:]
        ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))

    ::

        abjad> matrix[2]
        (20, 21, 22, 23)

    ::

        abjad> matrix[2][0]
        20

    Matrix implements only item retrieval in this revision.

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
        columns = tuple([tuple(column) for column in columns])
        assert len(set([len(column) for column in columns])) in (0, 1)
        rows = []
        for row_index in range(len(columns[0])):
            row = tuple([column[row_index] for column in columns])
            rows.append(row)
        rows = tuple(rows)
        return rows, columns

    def _init_from_rows(self, rows):
        rows = tuple([tuple(row) for row in rows])
        assert len(set([len(row) for row in rows])) in (0, 1)
        columns = []
        for column_index in range(len(rows[0])):
            column = tuple([row[column_index] for row in rows])
            columns.append(column)
        columns = tuple(columns)
        return rows, columns

    ### PUBLIC ATTRIBUTES ###

    @property
    def columns(self):
        '''Read-only columns::

            abjad> matrix = sequencetools.Matrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

        ::

            abjad> matrix.columns
            ((0, 10, 20), (1, 11, 21), (2, 12, 22), (3, 13, 23))

        Return tuple.
        '''
        return self._columns

    @property
    def rows(self):
        '''Read-only rows::

            abjad> matrix = sequencetools.Matrix([[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]])

        ::

            abjad> matrix.rows
            ((0, 1, 2, 3), (10, 11, 12, 13), (20, 21, 22, 23))

        Return tuple.
        '''
        return self._rows
