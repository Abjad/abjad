from abjad.tools.markuptools.Markup import Markup


def get_markup_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get markup attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff[:])
        abjad> markuptools.Markup('foo')(staff[0])
        Markup('foo')
        abjad> markuptools.Markup('bar')(staff[0])
        Markup('bar')

    ::

        abjad> f(staff)
        \new Staff {
            c'8 - \markup { \column { foo bar } } (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> markuptools.get_markup_attached_to_component(staff[0])
        (Markup('foo'), Markup('bar'))

    Return tuple of zero or more markup objects.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, Markup):
            result.append(mark)

    result = tuple(result)
    return result
