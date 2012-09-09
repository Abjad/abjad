def get_component_in_expr_with_name(expr, name):
    r""".. versionadded:: 2.10

    Get component in `expr` with `name`:

    ::

        >>> voice_1 = Voice("c'4 d'4 e'4 f'4")
        >>> voice_1.name = 'Top Voice'
        >>> voice_2 = Voice(r'\clef "bass" c4 d4 e4 f4')
        >>> voice_2.name = 'Bottom Voice'
        >>> staff = Staff([voice_1, voice_2])
        >>> f(staff)
        \new Staff {
            \context Voice = "Top Voice" {
                c'4
                d'4
                e'4
                f'4
            }
            \context Voice = "Bottom Voice" {
                \clef "bass"
                c4
                d4
                e4
                f4
            }
        }

    ::

        >>> voice = componenttools.get_component_in_expr_with_name(staff, 'Top Voice')
        >>> f(voice)
        \context Voice = "Top Voice" {
            c'4
            d'4
            e'4
            f'4
        }    

    Return one component.

    Raise missing component error when no named component is found.

    Raise extra component error when more than one component with `name` is found.
    """
    from abjad.tools import componenttools

    components = componenttools.get_components_in_expr_with_name(expr, name)
    if not components:
        raise MissingNamedComponentError
    elif 1 < len(components):
        raise ExtraNamedComponentError
    else:
        return components[0]

