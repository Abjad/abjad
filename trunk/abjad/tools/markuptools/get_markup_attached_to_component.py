def get_markup_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get markup attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff[:])

    ::

        >>> markuptools.Markup('foo')(staff[0])
        Markup(('foo',))(c'8)

    ::

        >>> markuptools.Markup('bar')(staff[0])
        Markup(('bar',))(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
                - \markup {
                    \column
                        {
                            foo
                            bar
                        }
                    }
            d'8
            e'8
            f'8 )
        }

    ::

        >>> markuptools.get_markup_attached_to_component(staff[0])
        (Markup(('foo',))(c'8), Markup(('bar',))(c'8))

    Return tuple of zero or more markup objects.
    '''
    from abjad.tools import markuptools

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, markuptools.Markup):
            result.append(mark)

    result = tuple(result)
    return result
