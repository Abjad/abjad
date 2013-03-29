import scf


def test_Studio_manage_svn_01():
    '''Ignore score backtracking.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='svn sco q')
    assert studio.ts == (6, (2, 4))
