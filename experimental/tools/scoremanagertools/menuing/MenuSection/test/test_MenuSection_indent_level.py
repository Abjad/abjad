from experimental import *


def test_MenuSection_indent_level_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    menu_section = menu.make_section(menu_tokens=menu_tokens)
    menu_section.title = 'section'

    assert menu_section.indent_level == 1
