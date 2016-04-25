# -*- coding: utf-8 -*-


def persist(expr):
    r'''Persists `expr`.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> persist(staff)
            PersistenceAgent(client=Staff("c'4 e'4 d'4 f'4"))

    Returns score mutation agent.
    '''
    from abjad.tools import agenttools
    return agenttools.PersistenceAgent(expr)
