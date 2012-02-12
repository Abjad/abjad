def insert_component_and_do_not_fracture_crossing_spanners(container, i, component):
    r'''.. versionadded:: 2.0

    Insert `component` into `container` at index `i` and do not fracture crossing spanners::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> containertools.insert_component_and_do_not_fracture_crossing_spanners(staff, 1, Note("cs'8"))
        Staff{5}

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            cs'8
            d'8
            e'8
            f'8 ]
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.insert_and_do_not_fracture()`` to
        ``containertools.insert_component_and_do_not_fracture_crossing_spanners()``.
    '''

    # insert component into container at index i
    # to avoid pychecker slice assignment error
    #container[i:i] = [component]
    container.__setitem__(slice(i, i), [component])

    # return container
    return container
