from experimental import *
import py


def test_MenuSection_default_index_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    menu_section = menu.make_section(menu_tokens=menu_tokens)
    menu_section.title = 'section'

    assert menu_section.default_index is None
    assert py.test.raises(ValueError, 'menu_section.default_index = -1')
    assert py.test.raises(ValueError, 'menu_section.default_index = 99')

    menu_section.default_index = 2
    assert menu_section.default_index == 2
