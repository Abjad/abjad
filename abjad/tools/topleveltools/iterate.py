# -*- coding: utf-8 -*-


def iterate(client=None):
    r'''Makes iteration agent.

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

        Iterates staff by leaf pair:

            >>> for pair in abjad.iterate(staff).by_leaf_pair():
            ...     pair
            ...
            Selection([Note("c'4"), Note("e'4")])
            Selection([Note("e'4"), Note("d'4")])
            Selection([Note("d'4"), Note("f'4")])

    ..  container:: example

        Iterates staff by pitch:

            >>> for pitch in abjad.iterate(staff).by_pitch():
            ...     pitch
            ...
            NamedPitch("c'")
            NamedPitch("e'")
            NamedPitch("d'")
            NamedPitch("f'")

    ..  container:: example

        Returns iteration agent:

        ::

            >>> abjad.iterate(staff)
            IterationAgent(client=Staff("c'4 e'4 d'4 f'4"))

    '''
    import abjad
    if client is not None:
        return abjad.IterationAgent(client=client)
    expression = abjad.Expression()
    expression = expression.iterate()
    return expression
