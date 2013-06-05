from experimental import *


def test_MenuSection_indent_level_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(menu_tokens=menu_tokens)
    section.title = 'section'

    assert section.indent_level == 1
