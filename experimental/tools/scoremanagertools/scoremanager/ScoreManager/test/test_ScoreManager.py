from experimental import *


def test_ScoreManager_01():
    '''Main menu to mothballed scores.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='mb q')
    score_manager.transcript_signature == (4,)


def test_ScoreManager_02():
    '''Main menu to score menu to tags menu.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example tags q')
    assert score_manager.transcript_signature == (6,)


def test_ScoreManager_03():
    '''Main menu to svn menu.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='svn q')
    assert score_manager.transcript_signature == (4,)


def test_ScoreManager_04():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='q')
    assert score_manager.session.transcript[-2][0] == 'Scores - active scores'

    score_manager.run(user_input='svn q')
    assert score_manager.session.transcript[-2][0] == 'Scores - active scores - repository commands'

    score_manager.run(user_input='svn b q')
    assert score_manager.session.transcript[-2][0] == 'Scores - active scores'


def test_ScoreManager_05():
    '''Junk works.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='foo q')
    assert score_manager.transcript_signature == (4, (0, 2))

    score_manager.run(user_input='foo bar q')
    assert score_manager.transcript_signature == (6, (0, 2, 4))


def test_ScoreManager_06():
    '''Back is handled correctly.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='b q')
    assert score_manager.transcript_signature == (4, (0, 2))


def test_ScoreManager_07():
    '''Exec works.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='exec 2**30 q')

    assert score_manager.session.transcript[1] == ['> exec', '']
    assert score_manager.session.transcript[2] == ['XCF> 2**30']
    assert score_manager.session.transcript[3] == ['1073741824', '']
    assert score_manager.session.transcript[4] == ['> q', '']


def test_ScoreManager_08():
    '''Exec protects against senseless input.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='exec foo q')

    assert score_manager.session.transcript[1] == ['> exec', '']
    assert score_manager.session.transcript[2] == ['XCF> foo']
    assert score_manager.session.transcript[3] == ['Expression not executable.', '']
    assert score_manager.session.transcript[4] == ['> q', '']


def test_ScoreManager_09():
    '''Shared session.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()

    assert score_manager.session is score_manager.score_package_wrangler.session


def test_ScoreManager_10():
    '''Backtracking stu* shortcut.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='Mon perf home q')
    ts_1 = score_manager.transcript_signature

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='Mon perf home q')
    ts_2 = score_manager.transcript_signature

    assert ts_1 == ts_2


def test_ScoreManager_11():
    '''Backtracking sco* shortcut.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='Mon perf score q')
    ts_1 = score_manager.transcript_signature

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='Mon perf sco q')
    ts_2 = score_manager.transcript_signature

    assert ts_1 == ts_2
