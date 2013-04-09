import scftools


def test_Session_command_history_string_01():

    studio = scftools.studio.Studio()
    studio.run(user_input='foo bar blah q')
    assert studio.session.command_history_string == 'foo bar blah q'


def test_Session_command_history_string_02():

    studio = scftools.studio.Studio()
    studio.run(user_input='1 perf q')
    assert studio.session.command_history_string == '1 perf q'
