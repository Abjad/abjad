def persist(client):
    r"""
    Makes persistence manager.

    ..  container:: example

        Persists staff as LilyPond file:

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

        >>> abjad.persist(staff).as_ly() # doctest: +SKIP

    ..  container:: example

        Returns persistence agent:

        >>> abjad.persist(staff)
        PersistenceManager(client=Staff("c'4 e'4 d'4 f'4"))

    """
    import abjad
    return abjad.PersistenceManager(client)
