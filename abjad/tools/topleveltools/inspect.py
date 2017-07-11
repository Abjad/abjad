# -*- coding: utf-8 -*-


def inspect(client):
    r'''Makes inspection agent.

    ::

        >>> import abjad

    ..  container:: example

        Example staff:

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

    ..  container:: example

        Gets duration of first note in staff:

        ::

            >>> abjad.inspect(staff[0]).get_duration()
            Duration(1, 4)

    ..  container:: example

        Gets lineage of first note in staff:

        ::

            >>> abjad.inspect(staff[0]).get_lineage()
            Lineage([Staff("c'4 e'4 d'4 f'4"), Note("c'4")])

    ..  container:: example

        Returns inspection agent:

        ::

            >>> abjad.inspect(staff)
            InspectionAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''
    from abjad.tools import agenttools
    return agenttools.InspectionAgent(client=client)
