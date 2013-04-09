import scftools


def test_Studio_01():
    '''Main menu to mothballed scores.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='mb q')
    studio.ts == (4,)


def test_Studio_02():
    '''Main menu to score menu to tags menu.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='1 tags q')
    assert studio.ts == (6,)


def test_Studio_03():
    '''Main menu to svn menu.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='svn q')
    assert studio.ts == (4,)


def test_Studio_04():
    '''Main menu header is the same even after state change to secondary menu.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='q')
    assert studio.transcript[-2][0] == 'Studio - active scores'

    studio.run(user_input='svn q')
    assert studio.transcript[-2][0] == 'Studio - active scores - repository commands'

    studio.run(user_input='svn b q')
    assert studio.transcript[-2][0] == 'Studio - active scores'


def test_Studio_05():
    '''Junk works.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='foo q')
    assert studio.ts == (4, (0, 2))

    studio.run(user_input='foo bar q')
    assert studio.ts == (6, (0, 2, 4))


def test_Studio_06():
    '''Back is handled correctly.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='b q')
    assert studio.ts == (4, (0, 2))


def test_Studio_07():
    '''Exec works.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='exec 2**30 q')

    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> 2**30']
    assert studio.transcript[3] == ['1073741824', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_08():
    '''Exec protects against senseless input.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='exec foo q')

    assert studio.transcript[1] == ['SCF> exec', '']
    assert studio.transcript[2] == ['XCF> foo']
    assert studio.transcript[3] == ['Expression not executable.', '']
    assert studio.transcript[4] == ['SCF> q', '']


def test_Studio_09():
    '''Shared session.
    '''

    studio = scftools.studio.Studio()

    assert studio.session is studio.score_package_wrangler.session


def test_Studio_10():
    '''Backtracking stu* shortcut.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='Mon perf studio q')
    ts_1 = studio.ts

    studio = scftools.studio.Studio()
    studio.run(user_input='Mon perf stu q')
    ts_2 = studio.ts

    assert ts_1 == ts_2


def test_Studio_11():
    '''Backtracking sco* shortcut.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='Mon perf score q')
    ts_1 = studio.ts

    studio = scftools.studio.Studio()
    studio.run(user_input='Mon perf sco q')
    ts_2 = studio.ts

    assert ts_1 == ts_2
