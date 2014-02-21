# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__run_01():
    r'''String menu_entry defaults.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'

    result = menu._run(pending_user_input='foo')
    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app')
    assert result == 'apple'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app, che-ban')
    assert result is None


def test_Menu__run_02():
    r'''Hidden menu section.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section(is_secondary=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location', '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app')
    assert result == 'apple'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app, che-ban')
    assert result is None


def test_Menu__run_03():
    r'''Numbered menu section.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section(is_numbered=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: apple',
      '     2: banana',
      '     3: cherry',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result == 'apple'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app')
    assert result == 'apple'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app, che-ban')
    assert result is None


def test_Menu__run_04():
    r'''Menu section with range selection turned on.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section(is_ranged=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     apple',
      '     banana',
      '     cherry',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app')
    assert result == ['apple']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='app, che-ban')
    assert result == ['apple', 'cherry', 'banana']


def test_Menu__run_05():
    r'''Keyed menu section with key returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'

    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == 'add'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == 'add'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result is None


def test_Menu__run_06():
    r'''Keyed menu section with display string returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    result = menu._run(pending_user_input='foo')

    menu._session._reinitialize()
    result = menu._run(pending_user_input='foo')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == 'first command'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == 'first command'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result is None


def test_Menu__run_07():
    r'''Hidden keyed menu section with key returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.is_secondary = True
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location', '']

    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == 'add'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == 'add'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result is None


def test_Menu__run_08():
    r'''Hidden keyed menu section with display string returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section(is_secondary=True)
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='foo')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == 'first command'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == 'first command'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result is None


def test_Menu__run_09():
    r'''Numbered keyed menu section with key returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.is_numbered = True 
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     1: first command (add)',
      '     2: second command (rm)',
      '     3: third command (mod)',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result == 'add'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == 'add'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == 'add'

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result is None


def test_Menu__run_10():
    r'''Ranged keyed menu section with with key returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.is_ranged = True
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'
    result = menu._run(pending_user_input='foo')

    assert menu._session.transcript.last_menu_lines == \
    ['Location',
      '',
      '     Section',
      '',
      '     first command (add)',
      '     second command (rm)',
      '     third command (mod)',
      '']
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == ['add']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == ['add']

    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result == ['add', 'mod', 'rm']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result == ['add', 'mod', 'rm']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result == ['add', 'mod', 'rm']


def test_Menu__run_11():
    r'''RK menu section with display string returned.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    menu_section = menu._make_section(is_ranged=True)
    menu_section.append(('first command', 'add'))
    menu_section.append(('second command', 'rm'))
    menu_section.append(('third command', 'mod'))
    menu_section.title = 'section'

    menu._session._reinitialize()
    result = menu._run(pending_user_input='foo')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='q')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add')
    assert result == ['first command']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir')
    assert result == ['first command']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='1, 3-2')
    assert result is None

    menu._session._reinitialize()
    result = menu._run(pending_user_input='add, mod-rm')
    assert result == ['first command', 'third command', 'second command']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, thi-sec')
    assert result == ['first command', 'third command', 'second command']

    menu._session._reinitialize()
    result = menu._run(pending_user_input='fir, mod-sec')
    assert result == ['first command', 'third command', 'second command']
