def iterate(client=None):
    r"""
    Makes iteration agent.

    ..  container:: example

        Iterates leaves:

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

        >>> for leaf in abjad.iterate(staff).leaves():
        ...     leaf
        ...
        Note("c'4")
        Note("e'4")
        Note("d'4")
        Note("f'4")

    """
    import abjad
    if client is not None:
        return abjad.Iteration(client=client)
    expression = abjad.Expression()
    expression = expression.iterate()
    return expression
