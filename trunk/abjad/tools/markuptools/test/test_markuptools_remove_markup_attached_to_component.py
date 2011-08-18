from abjad import *


def test_markuptools_remove_markup_attached_to_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    slur = spannertools.SlurSpanner(staff.leaves)
    markup_1 = markuptools.Markup('foo')(staff[0])
    markup_2 = markuptools.Markup('bar')(staff[0])

    r'''
    \new Staff {
        c'8 - \markup { \column { foo bar } } (
        d'8
        e'8
        f'8 )
    }
    '''

    markup = markuptools.remove_markup_attached_to_component(staff[0])

    r'''
    \new Staff {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
