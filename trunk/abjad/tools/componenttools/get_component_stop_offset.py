def get_component_stop_offset(component):
    r'''.. versionadded:: 1.1

    Get `component` stop offset::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> componenttools.get_component_stop_offset(staff[1])
        Offset(1, 4)

    Return positive fraction.
    '''

    return component._offset.stop
