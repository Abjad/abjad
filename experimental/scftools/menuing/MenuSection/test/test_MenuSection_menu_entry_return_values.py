import scftools


def test_MenuSection_menu_entry_return_values_01():
    '''Menu entry return values equal menu entry tokens when menu entry tokens are strings.
    Always true, including for all four combinations of the two settings tested here.
    '''

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    section.return_value_attribute = 'body'
    assert section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    section.return_value_attribute = 'body'
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['apple', 'banana', 'cherry']
    assert section.menu_entry_return_values == section.menu_entry_bodies
    assert section.menu_entry_return_values == section.tokens


def test_MenuSection_menu_entry_return_values_02():
    '''Menu entry return values vary when menu entry tokens are tuples.
    You can explicitly demand a return value equal either to the menu entry key or body.
    Note that section numbering plays no role in this.
    '''

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add', 'rm', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add', 'rm', 'mod']
    assert section.menu_entry_return_values == section.menu_entry_keys

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    section.return_value_attribute = 'body'
    assert section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    section.return_value_attribute = 'body'
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_return_values == section.menu_entry_bodies


def test_MenuSection_menu_entry_return_values_03():
    '''Length-4 tuples include prepopulated return values.
    You must still set return_value_attribute to 'prepopulated'.
    '''

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.append(('add', 'add something', None, 'return value A'))
    section.append(('rm', 'delete something', None, 'return value B'))
    section.append(('mod', 'modify something', None, 'return value C'))
    section.return_value_attribute = 'prepopulated'
    assert not section.is_numbered
    assert section.menu_entry_return_values == ['return value A', 'return value B', 'return value C']
