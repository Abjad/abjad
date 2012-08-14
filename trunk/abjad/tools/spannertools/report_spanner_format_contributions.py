def report_spanner_format_contributions(component, klass=None):
    r'''.. versionadded:: 1.1

    Report as string format contributions of all spanners attached to `component`::

        >>> staff = Staff("c'8 [ ( d'8 e'8 f'8 ] )")
        >>> trill = spannertools.TrillSpanner(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        >>> print spannertools.report_spanner_format_contributions(staff[0])
        BeamSpanner
            _format_right_of_leaf
                [
        SlurSpanner
            _format_right_of_leaf
                (

    Return string.
    '''
    from abjad.tools import spannertools

    result = ''
    locations = ('_format_before_leaf', '_format_right_of_leaf', '_format_after_leaf')
    spanners = list(spannertools.get_spanners_attached_to_component(component, klass))
    spanners.sort(lambda x, y: cmp(x._class_name, y._class_name))
    for spanner in spanners:
        result += '%s\n' % spanner._class_name
        for location in locations:
            contributions = getattr(spanner, location)(component)
            if contributions:
                result += '\t%s\n' % location
                for contribution in contributions:
                    result += '\t\t%s\n' % contribution
    return result
