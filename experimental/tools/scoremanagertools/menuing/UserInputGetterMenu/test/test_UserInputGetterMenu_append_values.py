from experimental import *


def test_UserInputGetterMenu_append_values_01():

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_integer('attribute')
    assert getter._run(user_input='foo -99') == -99

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_integer_in_range('attribute', 1, 10)
    assert getter._run(user_input='foo -99 99 7') == 7

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    menu_section = scoremanagertools.menuing.MenuSection()
    menu_section.is_numbered = True
    menu_entries = ['apple', 'banana', 'cherry', 'durian', 'endive', 'fennel']
    menu_section.menu_entries = menu_entries
    getter.append_menu_section_range('attribute', menu_section)
    assert getter._run(user_input='fen-dur, app, che') == [6, 5, 4, 1, 3]

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_markup('attribute')
    assert getter._run(user_input='foo') == markuptools.Markup('foo')

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_named_chromatic_pitch('attribute')
    assert getter._run(user_input="cs'") == \
        pitchtools.NamedChromaticPitch("cs'")

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_string('attribute')
    assert getter._run(user_input='None -99 99 1-4 foo') == 'foo'

    getter = scoremanagertools.menuing.UserInputGetterMenu()
    getter.append_string_or_none('attribute')
    assert getter._run(user_input='-99 99 1-4 None') is None
