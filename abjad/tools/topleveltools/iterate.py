# -*- coding: utf-8 -*-


def iterate(expr):
    r'''iterates `expr`.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> notes = staff[-2:]
            >>> iterate(notes)
            IterationAgent(client=Selection([Note("d'4"), Note("f'4")]))

    Returns score iteration agent.
    '''
    from abjad.tools import agenttools
    return agenttools.IterationAgent(expr)
