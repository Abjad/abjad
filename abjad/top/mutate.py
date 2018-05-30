def mutate(client):
    r"""
    Makes mutation agent.

    ..  container:: example

        Scales duration of last note notes in staff:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                e'4
                d'4
                f'4
            }

        >>> abjad.mutate(staff[-2:]).scale(abjad.Multiplier(3, 2))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                e'4
                d'4.
                f'4.
            }

    ..  container:: example

        Returns mutation agent:

        >>> abjad.mutate(staff[-2:])
        Mutation(client=Selection([Note("d'4."), Note("f'4.")]))

    """
    import abjad
    return abjad.Mutation(client=client)
