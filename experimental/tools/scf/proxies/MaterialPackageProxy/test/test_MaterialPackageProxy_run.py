import scf


def test_MaterialPackageProxy_run_01():
    '''Global materials: quit, back, studio, score & junk all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='m sargasso q')
    assert studio.ts == (6,)

    studio.run(user_input='m sargasso b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='m sargasso studio q')
    assert studio.ts == (8, (0, 6))

    # TODO: make this work by causing score backtracking to be ignored
    #studio.run(user_input='m sargasso score q')
    #assert studio.ts == (8, (4, 6))

    studio.run(user_input='m sargasso foo q')
    assert studio.ts == (8, (4, 6))


def test_MaterialPackageProxy_run_02():
    '''Global materials: breadcrumbs work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='m sargasso q')
    assert studio.transcript[-2][0] == 'Studio - materials - sargasso multipliers'


def test_MaterialPackageProxy_run_03():
    '''Score materials: quit, back, studio, score & junk all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='all las m 2 q')
    assert studio.ts == (10,)

    studio.run(user_input='all las m 2 b q')
    assert studio.ts == (12, (6, 10))

    studio.run(user_input='all las m 2 studio q')
    assert studio.ts == (12, (2, 10))

    studio.run(user_input='all las m 2 score q')
    assert studio.ts == (12, (4, 10))

    studio.run(user_input='all las m 2 foo q')
    assert studio.ts == (12, (8, 10))


def test_MaterialPackageProxy_run_04():
    '''Score materials: breadcrumbs work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='all las m black q')
    assert studio.transcript[-2][0] == 'Las manos mágicas - materials - black pcs'
