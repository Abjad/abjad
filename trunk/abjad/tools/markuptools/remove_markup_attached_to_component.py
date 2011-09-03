from abjad.tools.markuptools.Markup import Markup
from abjad.tools.markuptools.get_markup_attached_to_component import get_markup_attached_to_component


def remove_markup_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Remove markup attached to `component`::

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

        abjad> markuptools.remove_markup_attached_to_component(staff[0])
        (Markup('foo'), Markup('bar'))

    ::

        abjad> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Return tuple of zero or more markup objects.
    '''

    # get markup attached to component
    result = get_markup_attached_to_component(component)

    # remove markup attached to component
    for mark in result:
        mark()

    # return removed markup
    result = tuple(result)
    return result
