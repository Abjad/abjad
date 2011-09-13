from abjad.tools.spannertools.get_spanners_attached_to_component import get_spanners_attached_to_component


def report_as_string_format_contributions_of_all_spanners_attached_to_component(component, klass = None):
    r'''.. versionadded:: 1.1

    Report as string format contributions of all spanners attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> beam = spannertools.BeamSpanner(staff.leaves)
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> trill = spannertools.TrillSpanner(staff)
        abjad> f(staff)
        \new Staff {
            c'8 [ ( \startTrillSpan
            d'8
            e'8
            f'8 ] ) \stopTrillSpan
        }

    ::

        abjad> spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_component(staff[0])
        'BeamSpanner\n\t_right\n\t\t[\nSlurSpanner\n\t_right\n\t\t(\n'

    Return string.
    '''

    result = ''
    locations = ('_before', '_left', '_right', '_after')
    spanners = list(get_spanners_attached_to_component(component, klass))
    spanners.sort(lambda x, y: cmp(x.__class__.__name__, y.__class__.__name__))
    for spanner in spanners:
        result += '%s\n' % spanner.__class__.__name__
        for location in locations:
            contributions = getattr(spanner._format, location)(component)
            if contributions:
                result += '\t%s\n' % location
                for contribution in contributions:
                    result += '\t\t%s\n' % contribution
    return result
