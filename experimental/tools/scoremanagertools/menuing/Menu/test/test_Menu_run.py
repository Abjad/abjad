from experimental import *


def test_Menu_run_01():
    '''String token defaults.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    result = section_1.extend(['apple', 'banana', 'cherry'])

    result = menu.run(user_input='foo')
    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == 'apple'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result is None

    '''Bodies give same result as keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == 'apple'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_02():
    '''Turning off keys does nothing to string tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == 'apple'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_03():
    '''Hidding suppresses output.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location', '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == 'apple'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_04():
    '''Numbered string tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False)
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: apple',
      '     2: banana',
      '     3: cherry',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result == 'apple'

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == 'apple'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_05():
    '''Ranged string tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True)
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app')
    assert result == ['apple']

    menu.session.reinitialize()
    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='app, che-ban')
    assert result == ['apple', 'cherry', 'banana']


def test_Menu_run_06():
    '''Default tuple tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    section_1 = menu.make_section()
    section_1.append(('add', 'first command'))
    section_1.append(('rm', 'second command'))
    section_1.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None

    '''Bodies returned instead of keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'first command'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'first command'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_07():
    '''Tuple tokens with keys hidden from user.
    NB: User can not match on keys but key returned from menu to calling code.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    section_1.append(('add', 'first command'))
    section_1.append(('rm', 'second command'))
    section_1.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command',
      '     second command',
      '     third command',
      '']

    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None

    '''Bodies returned instead of keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'first command'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_08():
    '''Hidding suppresses output.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False)
    section_1.title = 'section'
    section_1.append(('add', 'first command'))
    section_1.append(('rm', 'second command'))
    section_1.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location', '']

    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None

    '''Bodies returned instead of keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'first command'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'first command'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_09():
    '''Tuple tokens with numbering turned on.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False)
    section_1.title = 'section'
    section_1.append(('add', 'first command'))
    section_1.append(('rm', 'second command'))
    section_1.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: first command (add)',
      '     2: second command (rm)',
      '     3: third command (mod)',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'add'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'add'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None

    '''Bodies returned instead of keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result == 'first command'

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == 'first command'

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == 'first command'

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_10():
    '''Ranged tuple tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section(is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True)
    section_1.title = 'section'
    section_1.append(('add', 'first command'))
    section_1.append(('rm', 'second command'))
    section_1.append(('mod', 'third command'))
    result = menu.run(user_input='foo')

    assert menu.transcript[-2] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == ['add']

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == ['add']

    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result == ['add', 'mod', 'rm']

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result == ['add', 'mod', 'rm']

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result == ['add', 'mod', 'rm']

    '''Bodies returned instead of keys.'''

    section_1.return_value_attribute = 'body'

    menu.session.reinitialize()
    result = menu.run(user_input='foo')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='q')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='1')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add')
    assert result == ['first command']

    menu.session.reinitialize()
    result = menu.run(user_input='fir')
    assert result == ['first command']

    menu.session.reinitialize()
    result = menu.run(user_input='1, 3-2')
    assert result is None

    menu.session.reinitialize()
    result = menu.run(user_input='add, mod-rm')
    assert result == ['first command', 'third command', 'second command']

    menu.session.reinitialize()
    result = menu.run(user_input='fir, thi-sec')
    assert result == ['first command', 'third command', 'second command']

    menu.session.reinitialize()
    result = menu.run(user_input='fir, mod-sec')
    assert result == ['first command', 'third command', 'second command']
