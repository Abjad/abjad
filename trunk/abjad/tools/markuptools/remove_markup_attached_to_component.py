def remove_markup_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Remove markup attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff[:])
        >>> markuptools.Markup('foo')(staff[0])
        Markup(('foo',))(c'8)
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

        >>> markuptools.remove_markup_attached_to_component(staff[0])
        (Markup(('foo',)), Markup(('bar',)))

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Return tuple of zero or more markup objects.
    '''
    from abjad.tools import markuptools

    # get markup attached to component
    result = markuptools.get_markup_attached_to_component(component)

    # remove markup attached to component
    for mark in result:
        mark()

    # return removed markup
    result = tuple(result)
    return result
