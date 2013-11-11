# -*- encoding: utf-8 -*-
import os
import re


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
        r'''Persists client as LilyPond file.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_ly('~/example.ly') # doctest: +SKIP

        '''
        from abjad.tools import systemtools
        systemtools.IOManager.write_expr_to_ly(self._client, filename)

    def as_module(self, filename, object_name):
        r'''Persists client as Python module.

        ::

            >>> inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 1),
            ...     timespantools.Timespan(2, 4),
            ...     timespantools.Timespan(6, 8),
            ...     ])
            >>> persist(inventory).as_module( # doctest: +SKIP
            ...     '~/example.py', 'inventory')

        '''
        result = ['# -*- encoding: utf-8 -*-']
        storage_pieces = format(self._client, 'storage').splitlines()
        pattern = re.compile(r'\b[a-z]+tools\b')
        tools_package_names = set()
        for line in storage_pieces:
            match = pattern.search(line)
            while match is not None:
                group = match.group()
                tools_package_names.add(group)
                end = match.end()
                match = pattern.search(line, pos=end)
        for name in sorted(tools_package_names):
            result.append('from abjad.tools import {}'.format(name))
        result.append('')
        result.append('')
        result.append('{} = {}'.format(object_name, storage_pieces[0]))
        result.extend(storage_pieces[1:])
        result = '\n'.join(result)
        with open(os.path.expanduser(filename), 'w') as f:
            f.write(result)

    def as_pdf(self, filename):
        r'''Persists client as PDF.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_pdf('~/example.pdf') # doctest: +SKIP

        '''
        from abjad.tools import systemtools
        systemtools.IOManager.write_expr_to_pdf(self._client, filename)
