# -*- coding: utf-8 -*-


def mutate(client):
    r'''Makes mutation agent.

    ::

        >>> import abjad

    ..  container:: example

        Scales duration of last note notes in staff:

        ::

            >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4
                f'4
            }

        ::

            >>> abjad.mutate(staff[-2:]).scale(abjad.Multiplier(3, 2))
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                e'4
                d'4.
                f'4.
            }

    ..  container:: example

        Returns mutation agent:

        ::

            >>> abjad.mutate(staff[-2:])
            MutationAgent(client=Selection([Note("d'4."), Note("f'4.")]))

    '''
    from abjad.tools import agenttools
    return agenttools.MutationAgent(client)
