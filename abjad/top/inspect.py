def inspect(client):
    r"""
    Makes inspection agent.

    ..  container:: example

        Example staff:

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

    ..  container:: example

        Gets duration of first note in staff:

        >>> abjad.inspect(staff[0]).duration()
        Duration(1, 4)

    ..  container:: example

        Returns inspection agent:

        >>> abjad.inspect(staff)
        Inspection(client=Staff("c'4 e'4 d'4 f'4"))

    """
    import abjad
    return abjad.Inspection(client=client)
