import scf


def test_Session___repr___01():

    session = scf.core.Session(user_input='foo')
    assert repr(session) == "Session(initial_user_input='foo', user_input='foo')"
