from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def report_as_string_format_contributions_of_spanners_attached_to_component(component, klass=None):
    r'''.. versionadded:: 1.1

    Report as string format contributions of all spanners attached to `component`::

        abjad> staff = Staff("c'8 [ ( d'8 e'8 f'8 ] )")
        abjad> trill = spannertools.TrillSpanner(staff)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> print spannertools.report_as_string_format_contributions_of_spanners_attached_to_component(staff[0])
        BeamSpanner
            _format_right_of_leaf
                [
        SlurSpanner
            _format_right_of_leaf
                (

    Return string.

    .. versionchanged:: 2.9
        renamed ``spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_component()`` to
        ``spannertools.report_as_string_format_contributions_of_spanners_attached_to_component()``.
    '''

    result = ''
    locations = ('_format_before_leaf', '_format_right_of_leaf', '_format_after_leaf')
    spanners = list(get_spanners_attached_to_component(component, klass))
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
