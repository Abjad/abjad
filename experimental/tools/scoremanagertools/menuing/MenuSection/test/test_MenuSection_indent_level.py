from experimental import *


def test_MenuSection_indent_level_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(tokens=tokens)
    section.title = 'section'

    assert section.indent_level == 1
