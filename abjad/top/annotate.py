def annotate(component, annotation, indicator):
    r"""
    Annotates ``component`` with ``indicator``.

    ..  container:: example

        Annotates first note in staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.annotate(staff[0], 'bow_direction', abjad.Down)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

        >>> abjad.inspect(staff[0]).annotation('bow_direction')
        Down

        >>> abjad.inspect(staff[0]).annotation('bow_fraction') is None
        True

        >>> abjad.inspect(staff[0]).annotation('bow_fraction', 99)
        99

    Returns none.
    """
    import abjad
    assert isinstance(annotation, str), repr(annotation)
    wrapper = abjad.Wrapper(
        annotation=annotation,
        component=component,
        indicator=indicator,
        )
    wrapper._bind_to_component(component)
