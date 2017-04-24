# -*- coding: utf-8 -*-


def persist(client):
    r'''Makes persistence agent.

    ..  container:: example

        Persists staff as LilyPond file:

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4
                f'4
            }

        ::

            >>> persist(staff).as_ly() # doctest: +SKIP

    ..  container:: example

        Returns persistence agent:

        ::

            >>> persist(staff)
            PersistenceAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''
    from abjad.tools import agenttools
    return agenttools.PersistenceAgent(client)
