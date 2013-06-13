from experimental import *


def test_MenuSection_indent_level_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section()
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'

    assert menu_section.indent_level == 1
