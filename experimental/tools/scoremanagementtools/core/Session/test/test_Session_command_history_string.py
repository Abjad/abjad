from experimental import *


def test_Session_command_history_string_01():

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='foo bar blah q')
    assert studio.session.command_history_string == 'foo bar blah q'


def test_Session_command_history_string_02():

    studio = scoremanagementtools.studio.Studio()
    studio.run(user_input='example~score~i perf q')
    assert studio.session.command_history_string == 'example score i perf q'
