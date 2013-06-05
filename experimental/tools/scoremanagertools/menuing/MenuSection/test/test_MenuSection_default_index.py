from experimental import *
import py


def test_MenuSection_default_index_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(menu_tokens=menu_tokens)
    section.title = 'section'

    assert section.default_index is None
    assert py.test.raises(ValueError, 'section.default_index = -1')
    assert py.test.raises(ValueError, 'section.default_index = 99')

    section.default_index = 2
    assert section.default_index == 2
