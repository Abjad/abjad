import scf


def test_Menu_allow_ascii_access_to_unicode_key_01():

    studio = scf.studio.Studio()
    studio.run(user_input='Čáry q')
    assert studio.ts == (4,)

    studio.run(user_input='čáry q')
    assert studio.ts == (4,)

    studio.run(user_input='Cary q')
    assert studio.ts == (4,)

    studio.run(user_input='cary q')
    assert studio.ts == (4,)
