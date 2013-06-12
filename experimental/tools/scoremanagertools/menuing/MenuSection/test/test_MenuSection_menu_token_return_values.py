from experimental import *


def test_MenuSection_menu_token_return_values_01():
    '''Menu entry return values equal menu tokens
    when menu tokens are strings.
    Always true, including for all four combinations 
    of the two settings tested here.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        is_numbered=True,
        is_modern=True,
        )
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(is_modern=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        return_value_attribute='display_string',
        is_numbered=True,
        )
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(is_modern=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies


def test_MenuSection_menu_token_return_values_02():
    '''Menu entry return values vary when menu entry 
    menu_tokens are tuples.
    You can explicitly demand a return value equal 
    either to the menu entry key or display_string.
    Note that menu_section numbering plays no role in this.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        return_value_attribute='key',
        is_numbered=True, 
        is_modern=True,
        )
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section.menu_token_return_values == ['add', 'rm', 'mod']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_keys

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        return_value_attribute='key',
        is_modern=True,
        )
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['add', 'rm', 'mod']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_keys

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        is_numbered=True, 
        is_modern=True,
        )
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['add something', 'delete something', 'modify something']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(is_modern=True)
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['add something', 'delete something', 'modify something']
    assert menu_section.menu_token_return_values == \
        menu_section.menu_token_bodies


def test_MenuSection_menu_token_return_values_03():
    '''Length-4 tuples include prepopulated return values.
    You must still set return_value_attribute to 'prepopulated'.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu.make_section(
        return_value_attribute='prepopulated',
        is_modern=True,
        )
    menu_section.append(('add something', 'add', None, 'return value A'))
    menu_section.append(('delete something', 'rm', None, 'return value B'))
    menu_section.append(('modify something', 'mod', None, 'return value C'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_return_values == \
        ['return value A', 'return value B', 'return value C']
