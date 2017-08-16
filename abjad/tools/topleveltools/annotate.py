def annotate(component, name, indicator):
    r'''Annotates `component` with `indicator`.

    ..  container:: example

        Annotates first note in staff:

        ::

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.annotate(staff[0], 'bow_direction', Down)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> abjad.inspect(staff[0]).get_annotation('bow_direction')
            Down

        ::

            >>> abjad.inspect(staff[0]).get_annotation('bow_fraction') is None
            True

        ::

            >>> abjad.inspect(staff[0]).get_annotation('bow_fraction', 99)
            99

    Returns none.
    '''
    import abjad
    assert isinstance(name, str), repr(name)
    wrapper = abjad.IndicatorWrapper(
        component=component,
        indicator=indicator,
        is_annotation=True,
        name=name,
        )
    wrapper._bind_to_component(component)
