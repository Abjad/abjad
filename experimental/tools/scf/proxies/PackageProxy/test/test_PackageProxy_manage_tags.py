import scf


def test_PackageProxy_manage_tags_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 tags q')
    assert studio.ts == (6,)

    studio.run(user_input='1 tags b q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='1 tags studio q')
    assert studio.ts == (8, (0, 6))

    studio.run(user_input='1 tags score q')
    assert studio.ts == (8, (2, 6))

    studio.run(user_input='1 tags foo q')
    assert studio.ts == (8, (4, 6))
