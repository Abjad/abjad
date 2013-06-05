from experimental import *


def test_Menu_run_01():
    '''String menu_token defaults.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False, menu_tokens=menu_tokens)
    section_1.title = 'section'

    result = menu._run(user_input='foo')
    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == 'apple'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_02():
    '''String menu_token defaults.

    Bodies give same result as keys.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=False, menu_tokens=menu_tokens,
        return_value_attribute='body')
    section_1.title = 'section'

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == 'apple'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_03():
    '''Turning off keys does nothing to string menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False, menu_tokens=menu_tokens)
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == 'apple'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_04():
    '''Hidding suppresses output.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False, menu_tokens=menu_tokens)
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location', '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == 'apple'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_05():
    '''Numbered string menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=True, is_ranged=False, menu_tokens=menu_tokens)
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: apple',
      '     2: banana',
      '     3: cherry',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result == 'apple'

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == 'apple'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result is None


def test_Menu_run_06():
    '''Ranged string menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=True, menu_tokens=menu_tokens)
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app')
    assert result == ['apple']

    menu._session.reinitialize()
    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='app, che-ban')
    assert result == ['apple', 'cherry', 'banana']


def test_Menu_run_07():
    '''Default tuple menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(menu_tokens=menu_tokens, 
        is_keyed=True, return_value_attribute='key')
    section_1.title = 'section'
    
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'add'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'add'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_08():
    '''Default tuple menu_tokens.

    Bodies returned instead of keys.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section = menu.make_section(menu_tokens=menu_tokens, is_keyed=True, return_value_attribute='body')
    result = menu._run(user_input='foo')

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'first command'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'first command'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_09():
    '''Tuple menu_tokens with keys hidden from user.
    NB: User can not match on keys but key returned from menu to calling code.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='key')
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command',
      '     second command',
      '     third command',
      '']

    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'add'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_10():
    '''Tuple menu_tokens with keys hidden from user.
    NB: User can not match on keys but key returned from menu to calling code.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=False, is_hidden=False, is_numbered=False, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='body')
    section_1.title = 'section'

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'first command'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_11():
    '''Hidding suppresses output.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='key')
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location', '']

    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'add'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'add'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_12():
    '''Hidding suppresses output.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=True, is_numbered=False, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='body')
    section_1.title = 'section'

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'first command'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'first command'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_13():
    '''Tuple menu_tokens with numbering turned on.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='key')
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: first command (add)',
      '     2: second command (rm)',
      '     3: third command (mod)',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result == 'add'

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'add'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'add'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None



def test_Menu_run_14():
    '''Tuple menu_tokens with numbering turned on.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=False, is_numbered=True, is_ranged=False,
        menu_tokens=menu_tokens, return_value_attribute='body')
    section_1.title = 'section'

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result == 'first command'

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == 'first command'

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == 'first command'

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result is None


def test_Menu_run_15():
    '''Ranged tuple menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True,
        menu_tokens=menu_tokens, return_value_attribute='key')
    section_1.title = 'section'
    result = menu._run(user_input='foo')

    assert menu._session.transcript[-2][1] == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == ['add']

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == ['add']

    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result == ['add', 'mod', 'rm']

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result == ['add', 'mod', 'rm']

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result == ['add', 'mod', 'rm']


def test_Menu_run_16():
    '''Ranged tuple menu_tokens.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'first command'),
        ('rm', 'second command'),
        ('mod', 'third command'),
        ]
    section_1 = menu.make_section(
        is_keyed=True, is_hidden=False, is_numbered=False, is_ranged=True,
        menu_tokens=menu_tokens, return_value_attribute='body')
    section_1.title = 'section'

    menu._session.reinitialize()
    result = menu._run(user_input='foo')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='q')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='1')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add')
    assert result == ['first command']

    menu._session.reinitialize()
    result = menu._run(user_input='fir')
    assert result == ['first command']

    menu._session.reinitialize()
    result = menu._run(user_input='1, 3-2')
    assert result is None

    menu._session.reinitialize()
    result = menu._run(user_input='add, mod-rm')
    assert result == ['first command', 'third command', 'second command']

    menu._session.reinitialize()
    result = menu._run(user_input='fir, thi-sec')
    assert result == ['first command', 'third command', 'second command']

    menu._session.reinitialize()
    result = menu._run(user_input='fir, mod-sec')
    assert result == ['first command', 'third command', 'second command']
