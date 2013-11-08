# -*- encoding: utf-8 -*-


class PersistenceAgent(object):
    r'''A wrapper around Abjad's object persistence mechanisms.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_pdf('~/example.pdf') # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Interpreter representation of persistence agent.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 e'4 d'4 f'4")
                >>> persist(staff)
                PersistenceAgent(Staff{4})

        Returns string.
        '''
        return '{}({!s})'.format(
            type(self).__name__,
            self._client,
            )

    ### PUBLIC METHODS ###

    def as_ly(self, filename):
        r'''Persist client as LilyPond file.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_ly('~/example.ly') # doctest: +SKIP

        '''
        from abjad.tools import iotools
        iotools.write_expr_to_ly(self._client, filename)

    def as_pdf(self, filename):
        r'''Persist client as PDF.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_pdf('~/example.pdf') # doctest: +SKIP

        '''
        from abjad.tools import iotools
        iotools.write_expr_to_pdf(self._client, filename)
