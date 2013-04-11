from experimental import *


def test_Studio_score_navigation_01():
    '''Score does nothing.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='score q')
    studio.ts == (4, (0, 2))


def test_Studio_score_navigation_02():
    '''Session-initial next and prev both work.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='next q')
    studio.ts == (4,)
    isinstance(studio.session.current_score_package_short_name, str)

    studio.run(user_input='prev q')
    studio.ts == (4,)
    isinstance(studio.session.current_score_package_short_name, str)


def test_Studio_score_navigation_03():
    '''Successive next.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='next next next q')
    studio.ts == (8, (1, 3, 5))
    isinstance(studio.session.current_score_package_short_name, str)


def test_Studio_score_navigation_04():
    '''Successive prev.
    '''

    studio = scftools.studio.Studio()
    studio.run(user_input='prev prev prev q')
    studio.ts == (8, (1, 3, 5))
    isinstance(studio.session.current_score_package_short_name, str)
