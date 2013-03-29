import scf


def test_Studio_score_navigation_01():
    '''Score does nothing.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='score q')
    studio.ts == (4, (0, 2))


def test_Studio_score_navigation_02():
    '''Session-initial next and prev both work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='next q')
    studio.ts == (4,)
    assert studio.session.current_score_package_short_name == 'archipel'

    studio.run(user_input='prev q')
    studio.ts == (4,)
    assert studio.session.current_score_package_short_name == 'sekka'


def test_Studio_score_navigation_03():
    '''Successive next.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='next next next q')
    studio.ts == (8, (1, 3, 5))
    assert studio.session.current_score_package_short_name == 'cary'


def test_Studio_score_navigation_04():
    '''Successive prev.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='prev prev prev q')
    studio.ts == (8, (1, 3, 5))
    assert studio.session.current_score_package_short_name == 'recursif'
