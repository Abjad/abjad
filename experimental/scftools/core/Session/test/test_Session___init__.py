import scftools


def test_Session___init___01():
    '''Attributes assigned at initialization time.
    '''

    session = scftools.core.Session()

    assert session.initial_user_input is None
    assert session.breadcrumb_stack == []
    assert session.scores_to_show == 'active'
    assert session.user_input is None
